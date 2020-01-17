# Generated by Django 2.2.5 on 2020-01-07 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sku',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='产品名')),
                ('cover', models.ImageField(upload_to='', verbose_name='封面图')),
                ('point', models.PositiveIntegerField(default=0, verbose_name='所需积分')),
                ('detail', models.TextField(blank=True, default='', verbose_name='详情')),
                ('total_left', models.PositiveIntegerField(blank=True, default=0, verbose_name='总量')),
                ('total_sales', models.PositiveIntegerField(blank=True, default=0, verbose_name='销量')),
                ('status', models.PositiveSmallIntegerField(choices=[(0, '编辑中'), (1, '已上架'), (2, '已下架')], default=0, verbose_name='兑换商品状态')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('order_num', models.IntegerField(default=0, verbose_name='排序值[越小越靠前]')),
            ],
            options={
                'db_table': 'beep_sku',
                'ordering': ['order_num', '-create_at'],
            },
        ),
    ]