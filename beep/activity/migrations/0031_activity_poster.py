# Generated by Django 2.2.5 on 2019-12-13 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0030_auto_20191209_1422'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='poster',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='海报'),
        ),
    ]
