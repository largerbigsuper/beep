# Generated by Django 2.2.5 on 2019-10-20 04:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_auto_20191018_2348'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='detail',
            field=models.TextField(blank=True, verbose_name='详情'),
        ),
        migrations.AddField(
            model_name='topic',
            name='topic_type',
            field=models.PositiveSmallIntegerField(choices=[(0, '话题'), (1, '专题榜'), (2, '新人榜')], default=0, verbose_name='话题|专题榜|新人榜'),
        ),
    ]
