# Generated by Django 2.2.5 on 2019-12-10 17:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wechat_callback', '0015_auto_20191210_1549'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='wxgroup',
            unique_together={('room_wxid', 'bot_wxid')},
        ),
        migrations.RemoveField(
            model_name='wxgroup',
            name='wxid',
        ),
    ]
