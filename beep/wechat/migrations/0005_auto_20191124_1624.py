# Generated by Django 2.2.5 on 2019-11-24 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wechat', '0004_auto_20191124_1622'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wxsubmessage',
            name='warn_msg',
            field=models.CharField(blank=True, default='Beep币扑不作为投资理财建议～', max_length=20, verbose_name='温馨提示'),
        ),
    ]
