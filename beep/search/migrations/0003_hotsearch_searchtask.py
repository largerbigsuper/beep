# Generated by Django 2.2.5 on 2019-11-06 20:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0002_auto_20191101_2223'),
    ]

    operations = [
        migrations.CreateModel(
            name='SearchTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(blank=True, verbose_name='开始时间')),
                ('end_at', models.DateTimeField(blank=True, verbose_name='开始时间')),
                ('slug', models.CharField(db_index=True, max_length=120, unique=True, verbose_name='任务id')),
            ],
            options={
                'db_table': 'search_task',
            },
        ),
        migrations.CreateModel(
            name='HotSearch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyword', models.CharField(max_length=40, verbose_name='检索内容')),
                ('frequency', models.PositiveIntegerField(default=1, verbose_name='检索次数')),
                ('create_at', models.DateField(blank=True, verbose_name='产生时间')),
                ('update_at', models.DateTimeField(blank=True, verbose_name='更新时间')),
                ('is_top', models.BooleanField(default=False, verbose_name='置顶')),
                ('lable_type', models.PositiveIntegerField(choices=[(0, '普通'), (1, '热'), (2, '新'), (3, '荐')], default=0, verbose_name='热|新|荐')),
                ('task', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='search.SearchTask', verbose_name='计算任务')),
            ],
            options={
                'verbose_name': '热搜榜',
                'verbose_name_plural': '热搜榜',
                'db_table': 'hot_search',
                'ordering': ['-update_at', '-frequency'],
                'unique_together': {('keyword', 'update_at')},
            },
        ),
    ]
