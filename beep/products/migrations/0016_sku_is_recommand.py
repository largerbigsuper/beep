# Generated by Django 2.2.5 on 2020-01-14 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0015_auto_20200112_2245'),
    ]

    operations = [
        migrations.AddField(
            model_name='sku',
            name='is_recommand',
            field=models.BooleanField(blank=True, default=False, verbose_name='推荐'),
        ),
    ]
