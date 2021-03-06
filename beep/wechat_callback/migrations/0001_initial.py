# Generated by Django 2.2.5 on 2019-10-28 05:18

from django.db import migrations, models
import django_extensions.db.fields.json


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WxGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('head_img', models.CharField(blank=True, max_length=200, null=True, verbose_name='头像的url地址')),
                ('member_count', models.PositiveIntegerField(default=0, verbose_name='该群成员总数')),
                ('member_nickname_list', django_extensions.db.fields.json.JSONField(default='[]', verbose_name='成员昵称列表')),
                ('member_wxid_list', django_extensions.db.fields.json.JSONField(default='[]', verbose_name='当前群的成员wxid的列表')),
                ('name', models.CharField(blank=True, max_length=200, null=True, verbose_name='群名称')),
                ('owner_wxid', models.CharField(blank=True, max_length=200, null=True, verbose_name='群主wxid')),
                ('room_wxid', models.CharField(blank=True, max_length=200, null=True, verbose_name='群wxid')),
                ('wxid', models.CharField(max_length=200, verbose_name='wxid')),
            ],
            options={
                'db_table': 'wx_group',
            },
        ),
        migrations.CreateModel(
            name='WxUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wxid', models.CharField(max_length=200, unique=True, verbose_name='wxid')),
                ('wx_alias', models.CharField(blank=True, max_length=200, null=True, verbose_name='微信号')),
                ('nickname', models.CharField(blank=True, max_length=200, null=True, verbose_name='微信昵称')),
                ('remark_name', models.CharField(blank=True, max_length=200, null=True, verbose_name='好友备注')),
                ('head_img', models.CharField(blank=True, max_length=200, null=True, verbose_name='头像的url地址')),
                ('sex', models.PositiveSmallIntegerField(default=1, verbose_name='性别:1男，2女')),
                ('country', models.CharField(blank=True, max_length=200, null=True, verbose_name='祖国')),
                ('province', models.CharField(blank=True, max_length=200, null=True, verbose_name='省份')),
                ('city', models.CharField(blank=True, max_length=200, null=True, verbose_name='城市')),
            ],
            options={
                'db_table': 'wx_user',
            },
        ),
    ]
