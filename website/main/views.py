from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect

from .forms import RegisterForm, PostForm
from .models import Post

# USER LOGIN реализовано по дефолту, все что нужно было - создать шаблон


@login_required(login_url=reverse_lazy('login'))
def home(request):
    posts = Post.objects.all().select_related('author')
    
    if request.method == 'POST':
        post_id = request.POST.get("post-id")
        if post_id:
            post = Post.objects.get(pk=post_id).select_related('author')
            if post and post.author == request.user:
                post.delete()
            
    return render(request, 'main/home.html', {'posts': posts})



@login_required(login_url=reverse_lazy('login'))
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

