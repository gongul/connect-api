# Generated by Django 3.1.3 on 2021-07-28 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='verifying_number',
            field=models.CharField(blank=True, max_length=6, null=True, verbose_name='인증번호'),
        ),
    ]
