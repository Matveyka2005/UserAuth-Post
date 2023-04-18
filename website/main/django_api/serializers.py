from rest_framework import serializers
from django.contrib.auth.models import User

from ..models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("author", "title", "description", "created_at", "updated_at")