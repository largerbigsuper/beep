# Generated by Django 2.2.5 on 2020-01-07 19:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cfg', '0002_actionpointcfg'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='actionpointcfg',
            options={'ordering': ['code'], 'verbose_name': '用户行为积分配置', 'verbose_name_plural': '用户行为积分配置'},
        ),
    ]