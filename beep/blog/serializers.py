import re
import json

from django.db.models import F
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from beep.users.serializers import UserBaseSerializer
from beep.users.models import mm_RelationShip, mm_User
from .models import (Topic, mm_Topic, Blog, mm_Blog, AtMessage, mm_AtMessage,
                     Comment, mm_Comment, Like, mm_Like, BlogShare)

from utils.wexin_api import WeiXinOpenApi


class TopicSerializer(serializers.ModelSerializer):

    user = UserBaseSerializer(read_only=True)
    class Meta:
        model = Topic
        fields = ('id', 'name', 'status', 'create_at',
                  'cover', 'total_view', 'total_comment', 'user', 'topic_type', 'detail', 'sub_name', 'total_blog')
        read_only_fields = ['status', 'total_view', 'total_comment', 'user', 'total_blog']
    
    def create(self, validated_data):
        request = self.context['request']
        if request.user.is_staff:
            instance = self.Meta.model(user=request.user, **validated_data)
            instance.save()
            return instance




blog_base_fields = ['id', 'topic', 'is_anonymous', 'content', 'img_list', 'at_list', 'forward_blog',
                    'total_share', 'total_like', 'total_comment', 'total_view', 'total_forward',
                    'update_at', 'video', 'is_top', 'title', 'cover', 'activity', 'origin_blog']

blog_readonly_fields = ['total_share', 'total_like', 'total_comment', 'total_view', 'total_forward']


class BaseBlogSerializer(serializers.ModelSerializer):

    topic = TopicSerializer(read_only=True)
    img_list = serializers.ListField()
    at_list = serializers.ListField()
    user = UserBaseSerializer(read_only=True)

    class Meta:
        model = Blog
        fields = blog_base_fields + ['user']

class BlogSimpleSerializer(BaseBlogSerializer):
    
    origin_blog = BaseBlogSerializer()
    class Meta:
        model = Blog
        fields = blog_base_fields + ['user']

class BlogCreateSerializer(BaseBlogSerializer):

    topic_str = serializers.CharField(write_only=True, allow_blank=True, required=False)
    cover_url = serializers.CharField(write_only=True, allow_blank=True, required=False)

    class Meta:
        model = Blog
        fields = blog_base_fields + ['topic_str'] + ['cover_url']
        read_only_fields = blog_readonly_fields

    def create(self, validated_data):
        """
        发微博 @功能 格式：@xxx 文本信息
        """
        # 图片列表，content，视频为空的话不允许创建博文
        blank_check_fileds = ['content', 'img_list', 'at_list', 'title', 'cover_url']
        blank_fields = []
        for key in blank_check_fileds:
            value = validated_data.get(key)
            if not value:
                blank_fields.append(key)
        if len(blank_check_fileds) == len(blank_fields):
            error_msg = '{}参数至少填一项'.format(blank_fields)
            raise ValidationError(error_msg)
        # 微信内容校验
        WeiXinOpenApi().check_content(validated_data)
        user = self.context['request'].user
        # deal topic
        cover_url = validated_data.pop('cover_url', None)
        topic_str = validated_data.pop('topic_str', None)
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
        validated_data['cover'] = cover_url
        instance = self.Meta.model(user=user, **validated_data)
        instance.topic = topic
        instance.save()
        # 更新博文数量
        if topic:
            mm_Topic.update_data(topic.id, 'total_blog')
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
    origin_blog = BlogSimpleSerializer()

    def get_is_like(self, obj):
        """是否点赞
        """
        user = self.context['request'].user
        if not user.is_authenticated:
            return 0
        if not hasattr(user, '_likes'):
            user._likes = mm_Like.blogs().filter(user=user).values_list('blog_id', flat=True)
        return 1 if obj.id in user._likes else 0
        
    class Meta:
        model = Blog
        fields = blog_base_fields + ['user', 'is_like', 'origin_blog']
        read_only_fields = blog_readonly_fields



class AtMessageSerializer(serializers.ModelSerializer):

    blog = BlogListSerialzier()
    user = UserBaseSerializer(read_only=True)

    class Meta:
        model = AtMessage
        fields = ('id', 'blog', 'status', 'create_at', 'user')


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
            to_user = blog.user
        instance = Comment(user=request.user,
                           to_user=to_user, **validated_data)
        instance.save()
        return instance


class CommentListSerializer(serializers.ModelSerializer):
    """评论列表
    """

    user = UserBaseSerializer()
    to_user = UserBaseSerializer()
    # blog = BlogSimpleSerializer()

    class Meta:
        model = Comment
        fields = ('id', 'user', 'to_user', 'reply_to', 'text', 'create_at', 'parent', 'total_like')

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

    blog = BlogListSerialzier()
    user = UserBaseSerializer()

    class Meta:
        model = Like
        fields = ('id', 'user', 'create_at', 'blog')


class MyLikeListSerializer(serializers.ModelSerializer):

    blog = BlogListSerialzier()

    class Meta:
        model = Like
        fields = ('id', 'blog', 'create_at')
