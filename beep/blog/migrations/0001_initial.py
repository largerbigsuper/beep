# Generated by Django 2.2.5 on 2019-09-23 13:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields.json


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AtMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.PositiveSmallIntegerField(choices=[(0, '未读'), (0, '已读')], default=0, verbose_name='未|已读')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
            options={
                'db_table': 'at_messages',
                'ordering': ['-create_at'],
            },
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_anonymous', models.BooleanField(default=False, verbose_name='是否匿名')),
                ('content', models.TextField(verbose_name='内容')),
                ('img_list', django_extensions.db.fields.json.JSONField(default='[]', verbose_name='图片列表')),
                ('at_list', django_extensions.db.fields.json.JSONField(default='[]', verbose_name='at用户列表')),
                ('total_share', models.PositiveIntegerField(default=0, verbose_name='分享次数')),
                ('total_like', models.PositiveIntegerField(default=0, verbose_name='点赞次数')),
                ('total_comment', models.PositiveIntegerField(default=0, verbose_name='评论次数')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('at_users', models.ManyToManyField(related_name='blog_at_users_set', through='blog.AtMessage', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'blogs',
                'ordering': ['-update_at'],
            },
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, verbose_name='话题')),
                ('status', models.PositiveSmallIntegerField(choices=[(-1, '已屏蔽'), (0, '正常话题'), (1, '热门话题')], default=0, verbose_name='状态屏蔽|正常|热门')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
            options={
                'db_table': 'topics',
            },
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Blog', verbose_name='博客')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'db_table': 'user_blog_like',
                'ordering': ['-create_at'],
                'unique_together': {('user', 'blog')},
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(blank=True, max_length=200, null=True, verbose_name='评论正文')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('is_del', models.BooleanField(default=False, verbose_name='删除')),
                ('blog', models.ForeignKey(db_index=False, on_delete=django.db.models.deletion.CASCADE, to='blog.Blog')),
                ('reply_to', models.ForeignKey(blank=True, db_index=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='blog.Comment', verbose_name='回复消息id')),
                ('to_user', models.ForeignKey(db_index=False, on_delete=django.db.models.deletion.CASCADE, related_name='my_replys', to=settings.AUTH_USER_MODEL, verbose_name='被回复的人')),
                ('user', models.ForeignKey(db_index=False, on_delete=django.db.models.deletion.CASCADE, related_name='my_comments', to=settings.AUTH_USER_MODEL, verbose_name='评论人')),
            ],
            options={
                'verbose_name': '评论和回复管理',
                'verbose_name_plural': '评论和回复管理',
                'db_table': 'lv_comments',
                'ordering': ['-create_at'],
                'index_together': {('blog', 'user', 'reply_to', 'to_user')},
            },
        ),
        migrations.CreateModel(
            name='BlogShare',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Blog', verbose_name='博客')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'db_table': 'user_blog_share',
                'unique_together': {('user', 'blog')},
            },
        ),
        migrations.AddField(
            model_name='blog',
            name='comments',
            field=models.ManyToManyField(related_name='blog_comments_set', through='blog.Comment', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='blog',
            name='likes',
            field=models.ManyToManyField(related_name='blog_likes_set', through='blog.Like', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='blog',
            name='shares',
            field=models.ManyToManyField(related_name='blog_shares_set', through='blog.BlogShare', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='blog',
            name='topic',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='blogs', to='blog.Topic', verbose_name='话题'),
        ),
        migrations.AddField(
            model_name='blog',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='作者'),
        ),
        migrations.AddField(
            model_name='atmessage',
            name='blog',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Blog', verbose_name='博文'),
        ),
        migrations.AddField(
            model_name='atmessage',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='被@用户'),
        ),
    ]
