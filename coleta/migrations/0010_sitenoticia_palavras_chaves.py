# Generated by Django 4.1.7 on 2023-03-19 23:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coleta', '0009_sitenoticia_json_args'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitenoticia',
            name='palavras_chaves',
            field=models.ManyToManyField(to='coleta.palavrachave'),
        ),
    ]
