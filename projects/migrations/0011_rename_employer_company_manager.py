# Generated by Django 3.2.16 on 2024-01-08 17:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0010_auto_20240108_1945'),
    ]

    operations = [
        migrations.RenameField(
            model_name='company',
            old_name='employer',
            new_name='manager',
        ),
    ]