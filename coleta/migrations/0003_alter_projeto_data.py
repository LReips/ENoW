# Generated by Django 4.1.7 on 2023-03-19 00:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coleta', '0002_alter_projeto_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projeto',
            name='data',
            field=models.DateField(null=True),
        ),
    ]