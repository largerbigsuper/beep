# Generated by Django 2.2.5 on 2020-07-16 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0011_auto_20200710_1521'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPlan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blog_id', models.IntegerField(verbose_name='博文id')),
                ('action', models.CharField(max_length=100, verbose_name='动作名')),
                ('current', models.IntegerField(verbose_name='当前完成量')),
                ('total', models.IntegerField(verbose_name='目标多少')),
                ('done', models.BooleanField(default=False, verbose_name='完成')),
            ],
            options={
                'verbose_name': '博文任务计划',
                'verbose_name_plural': '博文任务计划',
                'db_table': 'cms_blog_plan',
                'ordering': ['-id'],
            },
        ),
    ]