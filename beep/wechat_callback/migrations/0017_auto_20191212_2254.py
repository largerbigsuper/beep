# Generated by Django 2.2.5 on 2019-12-12 22:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wechat_callback', '0016_auto_20191210_1733'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wxgroup',
            name='room_wxid',
            field=models.CharField(blank=True, db_index=True, max_length=200, null=True, verbose_name='群wxid'),
        ),
    ]
