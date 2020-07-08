# Generated by Django 2.2.5 on 2020-07-06 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0008_auto_20200705_1803'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='botactionlog',
            name='activity',
        ),
        migrations.RemoveField(
            model_name='botactionlog',
            name='blog',
        ),
        migrations.AddField(
            model_name='botactionlog',
            name='rid',
            field=models.PositiveIntegerField(default=0, verbose_name='资源id'),
        ),
        migrations.AlterField(
            model_name='botactionlog',
            name='action',
            field=models.PositiveSmallIntegerField(choices=[(0, '博文评论'), (1, '博文点赞'), (2, '博文转发'), (3, '活动评论'), (4, '关注用户')], default=0, verbose_name='行为'),
        ),
    ]
