# Generated by Django 2.2.5 on 2019-11-24 02:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wechat', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='wxsubmessage',
            options={'ordering': ['-id'], 'verbose_name': '推送订阅消息', 'verbose_name_plural': '推送订阅消息'},
        ),
        migrations.AlterModelOptions(
            name='wxsubscription',
            options={'ordering': ['-id'], 'verbose_name': '用户订阅', 'verbose_name_plural': '用户订阅'},
        ),
        migrations.RemoveField(
            model_name='wxsubmessage',
            name='data',
        ),
        migrations.RemoveField(
            model_name='wxsubmessage',
            name='news',
        ),
    ]
