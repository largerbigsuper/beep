# Generated by Django 2.2.5 on 2020-07-18 23:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0016_auto_20200718_2241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='botsetting',
            name='desc',
            field=models.CharField(max_length=100, verbose_name='说明'),
        ),
        migrations.AlterField(
            model_name='botsetting',
            name='name',
            field=models.CharField(max_length=100, verbose_name='变量名'),
        ),
    ]