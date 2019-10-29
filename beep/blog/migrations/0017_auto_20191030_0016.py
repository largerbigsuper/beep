# Generated by Django 2.2.5 on 2019-10-29 16:16

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django_extensions.db.fields.json


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0016_blog_is_delete'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='at_list',
            field=django_extensions.db.fields.json.JSONField(blank=True, default='[]', verbose_name='at用户列表'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='at_users',
            field=models.ManyToManyField(blank=True, related_name='blog_at_users_set', through='blog.AtMessage', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='blog',
            name='content',
            field=ckeditor_uploader.fields.RichTextUploadingField(verbose_name='内容'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='cover',
            field=models.ImageField(blank=True, max_length=200, null=True, upload_to='', verbose_name='文章封面图'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='img_list',
            field=django_extensions.db.fields.json.JSONField(blank=True, default='[]', verbose_name='图片列表'),
        ),
    ]
