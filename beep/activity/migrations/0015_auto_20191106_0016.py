# Generated by Django 2.2.5 on 2019-11-05 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0014_auto_20191102_0239'),
    ]

    operations = [
        migrations.AddField(
            model_name='rewardplan',
            name='task_id',
            field=models.CharField(blank=True, db_index=True, max_length=120, null=True, verbose_name='定时任务id'),
        ),
        migrations.AddField(
            model_name='rewardplan',
            name='task_result',
            field=models.CharField(blank=True, max_length=120, null=True, verbose_name='任务结果'),
        ),
    ]