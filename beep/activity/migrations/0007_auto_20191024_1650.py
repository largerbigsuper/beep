# Generated by Django 2.2.5 on 2019-10-24 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0006_auto_20191024_1603'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='cover',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='封面图'),
        ),
    ]
