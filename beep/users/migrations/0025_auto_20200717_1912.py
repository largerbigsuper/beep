# Generated by Django 2.2.5 on 2020-07-17 19:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0024_auto_20200717_1910'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userbot',
            options={'verbose_name': '用户信息_机器人账号', 'verbose_name_plural': '用户信息_机器人账号'},
        ),
        migrations.AlterModelOptions(
            name='userinner',
            options={'verbose_name': '用户信息_内部运营人员使用账号', 'verbose_name_plural': '用户信息_内部运营人员使用账号'},
        ),
    ]