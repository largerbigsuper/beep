from rest_framework import serializers

from beep.users.serializers import UserBaseSerializer

from .models import (Topic, mm_Topic, Blog, AtMessage, mm_AtMessage,
                     Comment, mm_Comment, BlogLike, BlogShare)


class TopicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Topic
        fields = ('id', 'name', 'status', 'create_at')
        read_only_fields = ['status']

class BaseBlogSerializer(serializers.ModelSerializer):
    
    topic = TopicSerializer()
    img_list = serializers.ListField()
    at_list = serializers.ListField()

class MyBlogSerializer(BaseBlogSerializer):

    class Meta:
        model = Blog
        fields = ('id', 'topic', 'is_anonymous',
                  'content', 'img_list', 'at_list', 'total_share',
                  'total_like', 'total_comment', 'update_at')

    def create(self, validated_data):
        # deal topic
        topic_data = validated_data.pop('topic')
        at_list = validated_data['at_list']
        topic, _ = mm_Topic.get_or_create(**topic_data)
        instance = self.Meta.model(
            author=self.context['request'].user, **validated_data)
        instance.topic = topic
        instance.save()
        # deal at message
        at_message_list = []
        for user_info in at_list:
            msg = AtMessage(blog=instance, user_id=user_info['id'])
            at_message_list.append(msg)
        mm_AtMessage.bulk_create(at_message_list)

        return instance


class BlogSerialzier(BaseBlogSerializer):
    """博文列表
    """

    author = UserBaseSerializer()

    class Meta:
        model = Blog
        fields = ('id', 'author', 'topic', 'is_anonymous',
                  'content', 'img_list', 'at_list', 'total_share',
                  'total_like', 'total_comment', 'update_at')


class AtMessageSerializer(serializers.ModelSerializer):

    blog = BlogSerialzier()

    class Meta:
        model = AtMessage
        fields = ('id', 'blog', 'status', 'create_at')


class CommentCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('id', 'reply_to', 'text')


class CommentSerializer(serializers.ModelSerializer):

    user = UserBaseSerializer()
    to_user = UserBaseSerializer()

    class Meta:
        model = Comment
        fields = ('id', 'user', 'to_user', 'reply_to', 'text', 'create_at')

class RecivedCommentSerializer(serializers.ModelSerializer):
    """收到的评论
    """

    user = UserBaseSerializer()

    class Meta:
        model = Comment
        fields = ('id', 'user', 'text', 'create_at')



class BlogLikeSerializer(serializers.ModelSerializer):

    blog = BlogSerialzier()

    class Meta:
        model = BlogLike
        fields = ('id', 'blog', 'create_at')
