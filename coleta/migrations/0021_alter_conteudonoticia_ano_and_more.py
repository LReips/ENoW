# Generated by Django 4.1.7 on 2023-04-04 18:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coleta', '0020_alter_campo_options_alter_estruturanoticia_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conteudonoticia',
            name='ano',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='conteudonoticia',
            name='caminho_img_local',
            field=models.CharField(blank=True, max_length=355, null=True),
        ),
        migrations.AlterField(
            model_name='conteudonoticia',
            name='conteudo',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='conteudonoticia',
            name='data_formatada',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='conteudonoticia',
            name='descricao',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='conteudonoticia',
            name='dia',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='conteudonoticia',
            name='id_coleta',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='conteudonoticia',
            name='imagem',
            field=models.CharField(blank=True, max_length=355, null=True),
        ),
        migrations.AlterField(
            model_name='conteudonoticia',
            name='localizacao',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='conteudonoticia',
            name='mes',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='conteudonoticia',
            name='url',
            field=models.CharField(blank=True, max_length=355, null=True),
        ),
        migrations.CreateModel(
            name='Logs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_coleta', models.CharField(blank=True, max_length=100, null=True)),
                ('url', models.CharField(blank=True, max_length=355, null=True)),
                ('titulo', models.CharField(blank=True, max_length=355, null=True)),
                ('erro', models.TextField(blank=True, null=True)),
                ('inserido_em', models.DateTimeField(auto_now_add=True)),
                ('conteudo_noticia', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='coleta.conteudonoticia')),
                ('palavra_chave', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='coleta.palavrachave')),
                ('projeto', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='coleta.projeto')),
                ('site', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='coleta.sitenoticia')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
    ]