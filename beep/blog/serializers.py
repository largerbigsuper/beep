from django.db.models import F
from rest_framework import serializers

from beep.users.serializers import UserBaseSerializer

from .models import (Topic, mm_Topic, Blog, AtMessage, mm_AtMessage,
                     Comment, mm_Comment, Like, BlogShare)


class TopicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Topic
        fields = ('id', 'name', 'status', 'create_at')
        read_only_fields = ['status']

class BaseBlogSerializer(serializers.ModelSerializer):
    
    topic = TopicSerializer(read_only=True)
    topic_str = serializers.CharField(write_only=True, allow_blank=True)
    img_list = serializers.ListField()
    at_list = serializers.ListField()

class BlogCreateSerializer(BaseBlogSerializer):

    class Meta:
        model = Blog
        fields = ('id', 'topic', 'topic_str', 'is_anonymous',
                  'content', 'img_list', 'at_list', 'total_share',
                  'total_like', 'total_comment', 'update_at')
        read_only_fields = ('total_share', 'total_like', 'total_comment')

    def create(self, validated_data):
        # deal topic
        topic_str = validated_data.pop('topic_str')
        topic = None
        if topic_str:
            topic_data = {
                'name': topic_str
            }
            topic, _ = mm_Topic.get_or_create(**topic_data)

        at_list = validated_data['at_list']
        instance = self.Meta.model(
            user=self.context['request'].user, **validated_data)
        instance.topic = topic
        instance.save()
        # deal at message
        at_message_list = []
        for user_info in at_list:
            msg = AtMessage(blog=instance, user_id=user_info['id'])
            at_message_list.append(msg)
        mm_AtMessage.bulk_create(at_message_list)

        return instance


class BlogListSerialzier(BaseBlogSerializer):
    """博文列表
    """

    user = UserBaseSerializer()

    class Meta:
        model = Blog
        fields = ('id', 'user', 'topic', 'is_anonymous',
                  'content', 'img_list', 'at_list', 'total_share',
                  'total_like', 'total_comment', 'update_at')
        read_only_fields = ('total_share', 'total_like', 'total_comment')


class AtMessageSerializer(serializers.ModelSerializer):

    blog = BlogListSerialzier()

    class Meta:
        model = AtMessage
        fields = ('id', 'blog', 'status', 'create_at')

class CommentBaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('id', 'text')

class CommentCreateSerializer(serializers.ModelSerializer):
    """创建评论
    """
    class Meta:
        model = Comment
        fields = ('id', 'blog', 'reply_to', 'text')
    
    def create(self, validated_data):
        request = self.context['request']
        blog = validated_data['blog']
        blog.total_comment = F('total_comment') + 1
        blog.save()
        reply_to = validated_data['reply_to']
        if reply_to:
            to_user = reply_to.user
        else:
            to_user = request.user
        instance = Comment(user=request.user, to_user=to_user, **validated_data)
        instance.save()
        return instance

class CommentListSerializer(serializers.ModelSerializer):
    """评论列表
    """

    user = UserBaseSerializer()
    to_user = UserBaseSerializer()

    class Meta:
        model = Comment
        fields = ('id', 'user', 'to_user', 'reply_to', 'text', 'create_at')


class LikeCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = ('id', 'blog', 'create_at')
    
    def create(self, validated_data):
        blog = validated_data['blog']
        blog.total_like = F('total_like') + 1
        blog.save()
        instance = self.Meta.model(user=self.context['request'].user, **validated_data)
        instance.save()
        return instance


class LikeListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = ('id', 'user', 'create_at')


class MyLikeListSerializer(serializers.ModelSerializer):
    
    blog = BlogListSerialzier()
    class Meta:
        model = Like
        fields = ('id', 'blog', 'create_at')

