# Generated by Django 2.2.5 on 2020-07-05 13:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0031_activity_poster'),
        ('blog', '0032_auto_20191202_1833'),
        ('bot', '0005_botactionstatsonblog'),
    ]

    operations = [
        migrations.CreateModel(
            name='BotActionLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.PositiveSmallIntegerField(choices=[(0, '博文评论'), (1, '博文点赞'), (2, '博文转发'), (3, '活动评论')], default=0, verbose_name='行为')),
                ('total', models.PositiveIntegerField(default=0, verbose_name='次数')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('activity', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='activity.Activity', verbose_name='活动')),
                ('blog', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.Blog', verbose_name='博文')),
                ('bot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bot.Bot', verbose_name='机器人')),
            ],
            options={
                'verbose_name': '机器人操作日志',
                'verbose_name_plural': '机器人操作日志',
                'db_table': 'cms_bot_action_log',
                'ordering': ['-id'],
            },
        ),
    ]
