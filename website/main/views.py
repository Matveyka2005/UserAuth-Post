from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User, Group

from .forms import RegisterForm, PostForm
from .models import Post

# USER LOGIN реализовано по дефолту, все что нужно было - создать шаблон


@login_required(login_url=reverse_lazy('login'))
def home(request):
    posts = Post.objects.all().select_related('author')
    
    if request.method == 'POST':
        post_id = request.POST.get("post-id")
        user_id = request.POST.get("user-id")
        
        if post_id:
            post = Post.objects.select_related('author').get(pk=post_id)
            if post and (post.author == request.user or request.user.has_perm("main.delete_post")):
                post.delete()
        elif user_id:
            user = User.objects.filter(pk=user_id).first()
            if user and request.user.is_staff:
                try:
                    group = Group.objects.get(name='default')
                    group.user_set.remove(user)
                except Exception as e:
                    pass
                
                try:
                    group = Group.objects.get(name='mod')
                    group.user_set.remove(user)
                except Exception as e:
                    pass 
    return render(request, 'main/home.html', {'posts': posts})



@login_required(login_url=reverse_lazy('login'))
@permission_required("main.add_post", login_url=reverse_lazy('login'),
                     raise_exception=True)
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return HttpResponseRedirect(reverse_lazy('home'))
        else:
            form = PostForm()
            return render(request, 'main/create_post.html', {'form': form})
    else:
        form = PostForm()
        return render(request, 'main/create_post.html', {'form': form})
            

def sign_up(request):
    if request.user.is_authenticated:
        return render(request, 'registration/error-sign-up.html')
    else:
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                user = form.save(commit=True)
                login(request, user)
                return HttpResponseRedirect(reverse_lazy('home'))
        else: 
            form = RegisterForm()
            
        return render(request, 'registration/sign-up.html', {'form': form})

