# Generated by Django 2.2.5 on 2019-11-11 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0017_auto_20191108_1424'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='summary_id',
            field=models.IntegerField(blank=True, null=True, verbose_name='总结博文id'),
        ),
    ]
