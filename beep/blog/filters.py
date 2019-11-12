from django_filters import rest_framework as filters
from django_filters.rest_framework import OrderingFilter

from .models import Comment, Like, Blog, Topic


class CommentFilter(filters.FilterSet):
    class Meta:
        model = Comment
        fields = {
            'blog_id': ['exact'],
            'parent_id': ['exact'],
        }

class LikeFilter(filters.FilterSet):

    class Meta:
        model = Like

        fields = {
            'blog_id': ['exact'],
            'user_id': ['exact'],
        }


class BlogFilter(filters.FilterSet):

    # o = OrderingFilter(
    #     fields={
    #         'score': 'score',
    #     },
    # )
    class Meta:
        model = Blog
        fields = {
            'user': ['exact'],
            'user__name': ['exact'],
            'topic_id': ['exact'],
            'topic__name': ['exact', 'icontains'],
            'content': ['icontains']
        }


class TopicFilter(filters.FilterSet):

    class Meta:
        model = Topic
        fields = {
            'name': ['exact'],
            'status': ['exact'],
            'user': ['exact'],
            'topic_type': ['exact'],
        }
