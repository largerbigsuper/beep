# Generated by Django 2.2.5 on 2019-12-09 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0029_auto_20191205_2121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='live_address',
            field=models.CharField(blank=True, max_length=200, verbose_name='直播地址|微信群名'),
        ),
    ]