# Generated by Django 2.2.5 on 2019-11-06 22:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0024_auto_20191107_0023'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='total_search',
            field=models.PositiveIntegerField(default=0, verbose_name='搜索次数'),
        ),
    ]