# Generated by Django 2.2.5 on 2019-11-06 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20191105_0040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar_url',
            field=models.ImageField(upload_to='', verbose_name='头像'),
        ),
    ]