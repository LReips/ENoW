# Generated by Django 4.1.7 on 2023-09-25 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('processamento', '0004_alter_classificacaomodelo_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='classificacaomodelo',
            name='fn',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='classificacaomodelo',
            name='fp',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='classificacaomodelo',
            name='matriz_confusao',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='classificacaomodelo',
            name='vn',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='classificacaomodelo',
            name='vp',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='resultadoprocessamento',
            name='fn',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='resultadoprocessamento',
            name='fp',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='resultadoprocessamento',
            name='vn',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='resultadoprocessamento',
            name='vp',
            field=models.IntegerField(null=True),
        ),
    ]
