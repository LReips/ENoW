# Generated by Django 4.1.7 on 2023-04-04 18:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coleta', '0021_alter_conteudonoticia_ano_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Logs',
            new_name='Log',
        ),
    ]