# Generated by Django 2.2.5 on 2019-10-20 12:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0004_auto_20191013_2126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='area',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='common.Area', verbose_name='区域'),
        ),
    ]
