# Generated by Django 2.2.5 on 2019-10-24 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0005_auto_20191020_2014'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='activity',
            options={'ordering': ['-id'], 'verbose_name': '活动', 'verbose_name_plural': '活动'},
        ),
        migrations.AlterModelOptions(
            name='registration',
            options={'ordering': ['-create_at'], 'verbose_name': '活动报名', 'verbose_name_plural': '活动报名'},
        ),
        migrations.RemoveField(
            model_name='activity',
            name='area',
        ),
        migrations.AddField(
            model_name='activity',
            name='city_code',
            field=models.CharField(blank=True, max_length=40, null=True, verbose_name='市code'),
        ),
        migrations.AddField(
            model_name='activity',
            name='city_name',
            field=models.CharField(blank=True, max_length=40, null=True, verbose_name='市'),
        ),
        migrations.AddField(
            model_name='activity',
            name='district_code',
            field=models.CharField(blank=True, max_length=40, null=True, verbose_name='区code'),
        ),
        migrations.AddField(
            model_name='activity',
            name='district_name',
            field=models.CharField(blank=True, max_length=40, null=True, verbose_name='区'),
        ),
        migrations.AddField(
            model_name='activity',
            name='province_code',
            field=models.CharField(blank=True, max_length=40, null=True, verbose_name='省code'),
        ),
        migrations.AddField(
            model_name='activity',
            name='province_name',
            field=models.CharField(blank=True, max_length=40, null=True, verbose_name='省'),
        ),
    ]