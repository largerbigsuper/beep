# Generated by Django 2.2.5 on 2019-11-01 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0010_auto_20191030_0022'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='ask_allowed',
            field=models.BooleanField(default=False, verbose_name='是否可以提问'),
        ),
    ]
