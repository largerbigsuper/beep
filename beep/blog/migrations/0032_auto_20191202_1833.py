# Generated by Django 2.2.5 on 2019-12-02 18:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0031_auto_20191126_2130'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blog',
            options={'ordering': ['is_delete', '-create_at'], 'verbose_name': '文章&博文', 'verbose_name_plural': '文章&博文'},
        ),
    ]