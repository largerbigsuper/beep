# Generated by Django 2.2.5 on 2019-10-24 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0007_auto_20191024_2013'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='blog_id',
            field=models.IntegerField(blank=True, null=True, verbose_name='博文id'),
        ),
    ]