# Generated by Django 2.2.5 on 2019-10-24 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_blog_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='cover',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='文章封面图'),
        ),
    ]