# Generated by Django 2.2.5 on 2019-10-13 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_user_desc'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='total_blog',
            field=models.PositiveIntegerField(default=0, verbose_name='博文数量'),
        ),
        migrations.AddField(
            model_name='user',
            name='total_followers',
            field=models.PositiveIntegerField(default=0, verbose_name='粉丝数量'),
        ),
        migrations.AddField(
            model_name='user',
            name='total_following',
            field=models.PositiveIntegerField(default=0, verbose_name='关注数量'),
        ),
    ]
