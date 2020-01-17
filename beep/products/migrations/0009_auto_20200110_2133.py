# Generated by Django 2.2.5 on 2020-01-10 21:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0008_sku_sku_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='skuexchange',
            name='quantity',
            field=models.PositiveIntegerField(default=1, verbose_name='购买数量'),
        ),
        migrations.AddField(
            model_name='skuexchange',
            name='sku_property',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='products.SkuProperty', verbose_name='商品属性'),
        ),
        migrations.AlterField(
            model_name='skuproperty',
            name='sku',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sku_properties', to='products.Sku', verbose_name='商品'),
        ),
        migrations.CreateModel(
            name='SkuOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_num', models.CharField(db_index=True, max_length=100, unique=True)),
                ('point', models.PositiveIntegerField(default=0, verbose_name='消耗积分')),
                ('status', models.PositiveIntegerField(choices=[(0, '已提交'), (1, '审核通过'), (2, '审核通过，正在处理'), (3, '已完成'), (4, '审核拒绝')], default=0, verbose_name='申请状态')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '订单',
                'verbose_name_plural': '订单',
                'db_table': 'beep_sku_order',
                'ordering': ['-create_at'],
            },
        ),
        migrations.AddField(
            model_name='skuexchange',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='products.SkuOrder', verbose_name='订单'),
        ),
    ]