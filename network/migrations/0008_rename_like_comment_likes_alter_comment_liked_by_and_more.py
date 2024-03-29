# Generated by Django 4.2.5 on 2023-12-21 08:57

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0007_alter_account_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='like',
            new_name='likes',
        ),
        migrations.AlterField(
            model_name='comment',
            name='liked_by',
            field=models.ManyToManyField(blank=True, null=True, related_name='liked_comments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='post',
            name='liked_by',
            field=models.ManyToManyField(blank=True, null=True, related_name='liked_posts', to=settings.AUTH_USER_MODEL),
        ),
    ]
