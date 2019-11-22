# Generated by Django 2.2.5 on 2019-11-21 13:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('activity', '0021_auto_20191120_2041'),
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan_datetime', models.DateTimeField(verbose_name='计划时间')),
                ('content', models.CharField(max_length=500, verbose_name='计划内容')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('activity', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='activity.Activity', verbose_name='活动')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'db_table': 'schedule',
                'unique_together': {('user', 'activity')},
                'index_together': {('user', 'plan_datetime')},
            },
        ),
    ]