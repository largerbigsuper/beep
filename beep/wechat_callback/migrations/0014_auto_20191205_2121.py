# Generated by Django 2.2.5 on 2019-12-05 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wechat_callback', '0013_auto_20191124_1954'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wxuser',
            name='wxid',
            field=models.CharField(db_index=True, max_length=200, unique=True, verbose_name='wxid'),
        ),
        migrations.AlterUniqueTogether(
            name='wxuser',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='wxuser',
            name='bot_wxid',
        ),
    ]