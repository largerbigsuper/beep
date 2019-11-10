# Generated by Django 2.2.5 on 2019-11-07 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0006_auto_20191107_0718'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='hotsearch',
            options={'ordering': ['-task_id', '-update_at', '-frequency'], 'verbose_name': '热搜榜', 'verbose_name_plural': '热搜榜'},
        ),
        migrations.AlterField(
            model_name='hotsearch',
            name='create_at',
            field=models.DateTimeField(blank=True, verbose_name='产生时间'),
        ),
    ]