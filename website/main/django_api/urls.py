from django.urls import path, include
from rest_framework.routers import SimpleRouter

from . import views


router = SimpleRouter()
router.register('posts', views.PostViewSet, basename='psots')

urlpatterns = [
    path('', include('rest_framework.urls')),
    # path('posts/', views.PostApiVieww(), name='posts')
]

urlpatterns += router.urls
