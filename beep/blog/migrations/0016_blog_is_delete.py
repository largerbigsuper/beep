# Generated by Django 2.2.5 on 2019-10-26 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0015_blog_activity'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='is_delete',
            field=models.BooleanField(default=False, verbose_name='是否删除'),
        ),
    ]