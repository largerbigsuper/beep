# Generated by Django 2.2.5 on 2020-01-07 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_skuexchange_point'),
    ]

    operations = [
        migrations.AddField(
            model_name='skuexchange',
            name='status',
            field=models.PositiveIntegerField(choices=[(0, '已提交'), (1, '审核通过'), (2, '审核拒绝')], default=0, verbose_name='申请状态'),
        ),
    ]