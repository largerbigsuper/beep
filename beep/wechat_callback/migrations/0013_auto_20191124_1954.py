# Generated by Django 2.2.5 on 2019-11-24 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wechat_callback', '0012_auto_20191107_0400'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wxmessage',
            name='bot_wxid',
            field=models.CharField(blank=True, db_index=True, max_length=200, null=True, verbose_name='bot_wxid'),
        ),
        migrations.AlterField(
            model_name='wxmessage',
            name='msg_type',
            field=models.CharField(blank=True, db_index=True, max_length=200, null=True, verbose_name='类型'),
        ),
        migrations.AlterField(
            model_name='wxmessage',
            name='room_wxid',
            field=models.CharField(blank=True, db_index=True, max_length=200, null=True, verbose_name='群wxid'),
        ),
        migrations.AlterField(
            model_name='wxmessage',
            name='user_id',
            field=models.IntegerField(blank=True, db_index=True, default=0, verbose_name='平台用户user_id'),
        ),
        migrations.AlterField(
            model_name='wxmessage',
            name='user_type',
            field=models.IntegerField(blank=True, db_index=True, default=0, verbose_name='用户类型：0:微信用户， 1:平台用户, 2:系统消息'),
        ),
    ]