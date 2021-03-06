# Generated by Django 2.2.5 on 2019-11-06 16:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0023_auto_20191106_2351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='activity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='activity.Activity', verbose_name='活动'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='forward_blog',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='forward_blogs', to='blog.Blog', verbose_name='转发blog_id'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='origin_blog',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='origin_blogs', to='blog.Blog', verbose_name='转发原始blog_id'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='topic',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='blogs', to='blog.Topic', verbose_name='话题'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='parent',
            field=models.ForeignKey(blank=True, db_index=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reply_group', to='blog.Comment', verbose_name='回复消息的一级id'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='reply_to',
            field=models.ForeignKey(blank=True, db_index=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reply_real', to='blog.Comment', verbose_name='回复消息id'),
        ),
    ]
