# Generated by Django 2.2.5 on 2020-01-10 14:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_skuexchange_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='SkuPropertyName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=20, unique=True, verbose_name='熟悉名称')),
            ],
            options={
                'verbose_name': '产品属性名',
                'verbose_name_plural': '产品属性名',
                'db_table': 'beep_sku_property_name',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='SkuType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=20, unique=True, verbose_name='类型')),
            ],
            options={
                'verbose_name': '产品类型',
                'verbose_name_plural': '产品类型',
                'db_table': 'beep_sku_type',
                'ordering': ['-id'],
            },
        ),
        migrations.AlterModelOptions(
            name='sku',
            options={'ordering': ['order_num', '-create_at'], 'verbose_name': '兑换商品', 'verbose_name_plural': '兑换商品'},
        ),
        migrations.AlterModelOptions(
            name='skuexchange',
            options={'ordering': ['-create_at'], 'verbose_name': '兑换申请', 'verbose_name_plural': '兑换申请'},
        ),
        migrations.AlterField(
            model_name='sku',
            name='order_num',
            field=models.IntegerField(default=10000, verbose_name='排序值[越小越靠前]'),
        ),
        migrations.CreateModel(
            name='SkuProperty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('property_name_1', models.CharField(max_length=20, verbose_name='属性名')),
                ('property_value_1', models.CharField(max_length=20, verbose_name='属性值')),
                ('property_name_2', models.CharField(max_length=20, verbose_name='属性名2')),
                ('property_value_2', models.CharField(max_length=20, verbose_name='属性值2')),
                ('property_name_3', models.CharField(max_length=20, verbose_name='属性名3')),
                ('property_value_3', models.CharField(max_length=20, verbose_name='属性值3')),
                ('total_left', models.PositiveIntegerField(blank=True, default=0, verbose_name='总量')),
                ('total_sales', models.PositiveIntegerField(blank=True, default=0, verbose_name='销量')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('sku', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Sku', verbose_name='产品')),
            ],
            options={
                'verbose_name': '产品属性',
                'verbose_name_plural': '产品属性',
                'db_table': 'beep_sku_property',
                'ordering': ['-id'],
            },
        ),
    ]