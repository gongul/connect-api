# Generated by Django 3.1.3 on 2021-08-12 13:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20210812_1815'),
    ]

    operations = [
        migrations.RenameField(
            model_name='friend',
            old_name='friend_user_id',
            new_name='friend_user',
        ),
        migrations.RenameField(
            model_name='friend',
            old_name='user_id',
            new_name='user',
        ),
    ]