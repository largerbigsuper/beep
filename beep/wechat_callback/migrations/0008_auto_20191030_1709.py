# Generated by Django 2.2.5 on 2019-10-30 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wechat_callback', '0007_auto_20191030_1658'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wxmessage',
            name='msg_timestamp',
            field=models.BigIntegerField(default=0, verbose_name='时间戳'),
        ),
    ]
