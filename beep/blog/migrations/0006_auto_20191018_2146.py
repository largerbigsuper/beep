# Generated by Django 2.2.5 on 2019-10-18 13:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20191014_2139'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='forward_blog',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='forward_blogs', to='blog.Blog', verbose_name='转发blog_id'),
        ),
        migrations.AddField(
            model_name='blog',
            name='origin_blog',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='origin_blogs', to='blog.Blog', verbose_name='转发原始blog_id'),
        ),
    ]
