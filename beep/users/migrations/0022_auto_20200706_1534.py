# Generated by Django 2.2.5 on 2020-07-06 15:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0021_user_is_bot'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='relationship',
            unique_together=set(),
        ),
        migrations.AlterIndexTogether(
            name='relationship',
            index_together=set(),
        ),
    ]
