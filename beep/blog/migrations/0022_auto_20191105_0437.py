# Generated by Django 2.2.5 on 2019-11-04 20:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0021_auto_20191102_2358'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blog',
            options={'ordering': ['is_delete', '-create_at'], 'verbose_name': '博文', 'verbose_name_plural': '博文'},
        ),
    ]
