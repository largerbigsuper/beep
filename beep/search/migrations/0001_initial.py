# Generated by Django 2.2.5 on 2019-09-25 12:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SearchKeyWord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyword', models.CharField(max_length=40, verbose_name='关键字')),
                ('frequency', models.PositiveIntegerField(default=1, verbose_name='检索次数')),
                ('create_date', models.DateField(auto_now_add=True, verbose_name='记录时间')),
            ],
            options={
                'db_table': 'search_keyword',
                'ordering': ['-create_date', '-frequency'],
                'unique_together': {('keyword', 'create_date')},
            },
        ),
        migrations.CreateModel(
            name='SearchHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=200, verbose_name='内容')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='记录时间')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'db_table': 'search_history',
                'ordering': ['-create_at'],
            },
        ),
    ]
