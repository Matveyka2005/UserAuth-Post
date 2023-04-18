from django.urls import path 
from . import views


urlpatterns = [
    path('create-post', views.create_post, name='create_post'),
    path('sign-up/', views.sign_up , name='sign_up'),
    path('home/', views.home, name='home'),
    path('', views.home, name='home'),
]
