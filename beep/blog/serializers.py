import re

from django.db.models import F
from rest_framework import serializers

from beep.users.serializers import UserBaseSerializer
from beep.users.models import mm_RelationShip, mm_User
from .models import (Topic, mm_Topic, Blog, mm_Blog, AtMessage, mm_AtMessage,
                     Comment, mm_Comment, Like, mm_Like, BlogShare)



class TopicSerializer(serializers.ModelSerializer):

    user = UserBaseSerializer(read_only=True)
    class Meta:
        model = Topic
        fields = ('id', 'name', 'status', 'create_at',
                  'cover', 'total_view', 'total_comment', 'user', 'topic_type', 'detail')
        read_only_fields = ['status', 'total_view', 'total_comment', 'user']
    
    def create(self, validated_data):
        request = self.context['request']
        if request.user.is_staff:
            instance = self.Meta.model(user=request.user, **validated_data)
            instance.save()
            return instance


class BaseBlogSerializer(serializers.ModelSerializer):

    topic = TopicSerializer(read_only=True)
    topic_str = serializers.CharField(write_only=True, allow_blank=True)
    img_list = serializers.ListField()
    at_list = serializers.ListField()
    user = UserBaseSerializer(read_only=True)


class BlogSimpleSerializer(BaseBlogSerializer):
    class Meta:
        model = Blog
        fields = ('id', 'user', 'topic', 'is_anonymous',
                  'content', 'img_list', 'at_list',
                  'total_share', 'total_like', 'total_comment', 'total_view',
                  'update_at', 'video', 'is_top', 'title')

class BlogCreateSerializer(BaseBlogSerializer):

    class Meta:
        model = Blog
        fields = ('id', 'topic', 'topic_str', 'is_anonymous',
                  'content', 'img_list', 'at_list',
                  'total_share', 'total_like', 'total_comment', 'total_view',
                  'update_at', 'forward_blog', 'total_forward', 'video', 'is_top', 'title')
        read_only_fields = ('total_share', 'total_like',
                            'total_comment', 'total_view', 'total_forward')

    def create(self, validated_data):
        """
        发微博 @功能 格式：@xxx 文本信息
        """
        user = self.context['request'].user
        # deal topic
        topic_str = validated_data.pop('topic_str')
        topic = None
        if topic_str:
            topic_data = {
                'name': topic_str
            }
            topic, _ = mm_Topic.get_or_create(**topic_data)

        forward_blog = validated_data.get('forward_blog')
        if forward_blog:
            if forward_blog.origin_blog_id:
                origin_blog_id = forward_blog.origin_blog_id
            else:
                origin_blog_id = forward_blog.id
            validated_data['forward_blog_id'] = forward_blog.id
            validated_data['origin_blog_id'] = origin_blog_id
        # 处理@功能
        # 若是转发功能，以 `//` 符号区分
        content = validated_data['content'].split('//')[0]
        names = re.findall(r"@(\S+)", content)
        at_list = mm_User.get_users(names)
        validated_data['at_list'] = at_list
        instance = self.Meta.model(user=user, **validated_data)
        instance.topic = topic
        instance.save()
        # deal at message
        at_message_list = []
        for user_info in at_list:
            msg = AtMessage(blog=instance, user_id=user_info['id'])
            at_message_list.append(msg)
        mm_AtMessage.bulk_create(at_message_list)
        mm_User.update_data(user.id, 'total_blog')
        # 更新转发
        if forward_blog:
            mm_Blog.update_data(forward_blog.id, 'total_forward')


        return instance


class BlogListSerialzier(BaseBlogSerializer):
    """博文列表
    """

    user = UserBaseSerializer()
    is_like = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()
    origin_blog = BlogSimpleSerializer()

    def get_is_like(self, obj):
        """是否点赞
        """
        user = self.context['request'].user
        if not user.is_authenticated:
            return 0
        if not hasattr(self, '_likes'):
            self._likes = mm_Like.blogs().filter(user=user).values_list('blog_id', flat=True)
        return 1 if obj.id in self._likes else 0

    def get_is_following(self, obj):
        """用户关系
        """
        user = self.context['request'].user
        if not user.is_authenticated:
            return 0
        if not hasattr(self, '_relations'):
            self._relations = mm_RelationShip.filter(user=user).values_list('following_id', flat=True)
        return 1 if obj.user_id in self._relations else 0

    class Meta:
        model = Blog
        fields = ('id', 'user', 'topic', 'is_anonymous',
                  'content', 'img_list', 'at_list',
                  'total_share', 'total_like', 'total_comment', 'total_view',
                  'update_at', 'is_like', 'is_following', 'origin_blog', 'total_forward', 'video', 'is_top', 'title')
        read_only_fields = ('total_share', 'total_like',
                            'total_comment', 'total_view')



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
        if blog.topic:
            blog.topic.total_comment = F('total_comment') + 1
            blog.topic.save()
        reply_to = validated_data['reply_to']
        if reply_to:
            to_user = reply_to.user
            if reply_to.parent_id:
                validated_data['parent_id'] = reply_to.parent_id
            else:
                validated_data['parent_id'] = reply_to.id
        else:
            to_user = request.user
        instance = Comment(user=request.user,
                           to_user=to_user, **validated_data)
        instance.save()
        return instance


class CommentListSerializer(serializers.ModelSerializer):
    """评论列表
    """

    user = UserBaseSerializer()
    to_user = UserBaseSerializer()

    class Meta:
        model = Comment
        fields = ('id', 'user', 'to_user', 'reply_to', 'text', 'create_at', 'parent', 'total_like')

class CommentDetailSerializer(CommentListSerializer):

    blog = BlogSimpleSerializer()
    
    class Meta:
        model = Comment
        fields = ('id', 'user', 'to_user', 'reply_to', 'text', 'create_at', 'parent', 'blog', 'total_like')


class LikeCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = ('id', 'blog', 'create_at')

    def create(self, validated_data):
        blog = validated_data['blog']
        mm_Blog.update_data(blog.id, 'total_like')
        instance = self.Meta.model(
            user=self.context['request'].user, **validated_data)
        instance.save()
        return instance

class CommentLikeCreateSerializer(serializers.ModelSerializer):
    """评论点赞
    """
    class Meta:
        model = Like
        fields = ('id', 'comment', 'create_at')

    def create(self, validated_data):
        commet = validated_data['comment']
        validated_data['blog'] = commet.blog
        mm_Blog.update_data(commet.id, 'total_like')
        instance = self.Meta.model(
            user=self.context['request'].user, **validated_data)
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
