# Generated by Django 2.2.5 on 2019-10-30 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wechat_callback', '0006_auto_20191030_1651'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wxmessage',
            name='emoji_url',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='表情'),
        ),
        migrations.AlterField(
            model_name='wxmessage',
            name='link_img_url',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='链接所列图地址'),
        ),
        migrations.AlterField(
            model_name='wxmessage',
            name='link_url',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='链接'),
        ),
        migrations.AlterField(
            model_name='wxmessage',
            name='msg',
            field=models.TextField(blank=True, null=True, verbose_name='文本内容'),
        ),
        migrations.AlterField(
            model_name='wxmessage',
            name='raw_msg',
            field=models.TextField(blank=True, null=True, verbose_name='微信原始消息'),
        ),
    ]