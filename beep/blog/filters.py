from django_filters import rest_framework as filters

from .models import Comment, Like, Blog


class CommentFilter(filters.FilterSet):
    class Meta:
        model = Comment
        fields = {
            'blog_id': ['exact'],
        }

class LikeFilter(filters.FilterSet):

    class Meta:
        model = Like

        fields = {
            'blog_id': ['exact'],
        }


class BlogFilter(filters.FilterSet):

    class Meta:
        model = Blog
        fields = {
            'user': ['exact'],
            'topic_id': ['exact'],
            'topic__name': ['icontains'],
            'content': ['icontains']
        }

