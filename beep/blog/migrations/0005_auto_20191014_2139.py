# Generated by Django 2.2.5 on 2019-10-14 13:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0004_auto_20191009_1544'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='total_like',
            field=models.PositiveIntegerField(default=0, verbose_name='点赞数量'),
        ),
        migrations.AddField(
            model_name='like',
            name='comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.Comment', verbose_name='评论'),
        ),
        migrations.AlterUniqueTogether(
            name='like',
            unique_together={('user', 'blog', 'comment')},
        ),
    ]