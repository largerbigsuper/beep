# Generated by Django 2.2.5 on 2019-11-23 16:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0025_wxform'),
    ]

    operations = [
        migrations.AddField(
            model_name='wxform',
            name='create_at',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='wxform',
            name='activity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='activity.Activity', verbose_name='活动'),
        ),
        migrations.AlterField(
            model_name='wxform',
            name='published',
            field=models.BooleanField(blank=True, default=False, verbose_name='已推送'),
        ),
    ]