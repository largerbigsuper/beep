from django_filters import rest_framework as filters

from .models import Comment, BlogLike

class CommentFilter(filters.FilterSet):
    class Meta:
        model = Comment
        fields = {
            'blog_id': ['exact'],
        }

class LikeFilter(filters.FilterSet):

    class Meta:
        model = BlogLike
        fields = {
            'blog_id': ['exact'],
        }

