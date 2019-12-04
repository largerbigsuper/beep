# Generated by Django 2.2.5 on 2019-12-02 18:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('blog', '0032_auto_20191202_1833'),
        ('search', '0008_auto_20191117_2311'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ad_type', models.PositiveSmallIntegerField(choices=[(0, '博文关注'), (1, '博文热门'), (2, '热搜榜'), (3, '图文链接')], default=3, verbose_name='广告类型')),
                ('order_num', models.PositiveIntegerField(default=1, verbose_name='排列位置')),
                ('image', models.ImageField(blank=True, null=True, upload_to='', verbose_name='广告封面')),
                ('link', models.CharField(blank=True, default='', max_length=200, verbose_name='广告链接')),
                ('module_type', models.PositiveSmallIntegerField(choices=[(0, '未设置'), (1, '首页'), (2, '热搜'), (3, '快讯'), (4, '博文详情'), (5, '专题详情'), (6, '活动详情'), (7, '热搜详情'), (8, '快讯详情')], db_index=True, default=0, verbose_name='显示模块')),
                ('position_type', models.PositiveSmallIntegerField(choices=[(0, '未设置'), (1, '主位置'), (2, '侧边栏')], db_index=True, default=0, verbose_name='显示位置')),
                ('start_at', models.DateTimeField(verbose_name='生效时间')),
                ('expired_at', models.DateTimeField(verbose_name='结束时间')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('status', models.PositiveSmallIntegerField(choices=[(0, '编辑中'), (1, '已发布'), (2, '已撤回')], default=0, verbose_name='状态')),
                ('mark', models.CharField(default='', max_length=120, verbose_name='备注')),
                ('blog', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.Blog', verbose_name='博文')),
                ('hotSearch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='search.HotSearch', verbose_name='热搜')),
            ],
            options={
                'verbose_name': '广告',
                'verbose_name_plural': '广告',
                'db_table': 'beep_ad',
                'ordering': ['-expired_at'],
            },
        ),
    ]