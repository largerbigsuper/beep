# Generated by Django 2.2.5 on 2020-07-02 20:56

from django.db import migrations, models
import django_extensions.db.fields.json


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BotAvatar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=400, verbose_name='内容')),
                ('used', models.BooleanField(default=False, verbose_name='已使用')),
            ],
            options={
                'verbose_name': '机器人头像',
                'verbose_name_plural': '机器人头像',
                'db_table': 'cms_bot_avatar',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='BotBuilder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desc', models.CharField(max_length=100, verbose_name='描述')),
                ('total', models.PositiveIntegerField(default=1, verbose_name='生成机器人个数')),
                ('done', models.BooleanField(default=False, verbose_name='执行成功')),
                ('results', django_extensions.db.fields.json.JSONField(default=[], verbose_name='机器人列表')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '生成机器人生成',
                'verbose_name_plural': '生成机器人生成',
                'db_table': 'cms_bot_builder',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='BotName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=400, verbose_name='内容')),
                ('used', models.BooleanField(default=False, verbose_name='已使用')),
            ],
            options={
                'verbose_name': '机器人名子',
                'verbose_name_plural': '机器人名子',
                'db_table': 'cms_bot_name',
                'ordering': ['-id'],
            },
        ),
        migrations.AlterField(
            model_name='bot',
            name='is_on',
            field=models.BooleanField(default=True, verbose_name='使用中'),
        ),
    ]
