# Generated by Django 4.1.7 on 2024-03-10 20:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Campo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(help_text='Without accents', max_length=255, verbose_name='Type')),
            ],
            options={
                'verbose_name_plural': 'Fields',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Cidade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ibge', models.IntegerField(unique=True, verbose_name='Unique ID')),
                ('nome', models.CharField(max_length=355, verbose_name='Name')),
                ('latitude', models.CharField(blank=True, max_length=30)),
                ('longitude', models.CharField(blank=True, max_length=30)),
            ],
            options={
                'verbose_name_plural': 'Cities',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='ConteudoNoticia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(blank=True, max_length=300, verbose_name='Title')),
                ('descricao', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('conteudo', models.TextField(blank=True, null=True, verbose_name='Content')),
                ('dia', models.CharField(blank=True, max_length=20, null=True, verbose_name='Day')),
                ('mes', models.CharField(blank=True, max_length=20, null=True, verbose_name='Month')),
                ('ano', models.CharField(blank=True, max_length=20, null=True, verbose_name='Year')),
                ('data_formatada', models.CharField(blank=True, max_length=100, null=True, verbose_name='News date')),
                ('imagem', models.CharField(blank=True, max_length=355, null=True, verbose_name='Image')),
                ('url', models.CharField(blank=True, max_length=355, null=True)),
                ('caminho_img_local', models.CharField(blank=True, max_length=355, null=True, verbose_name='Image local path')),
                ('id_coleta', models.CharField(blank=True, max_length=100, null=True)),
                ('data_coleta', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('cidade', models.ForeignKey(db_column='cidade', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='coleta.cidade', to_field='ibge', verbose_name='City')),
            ],
            options={
                'verbose_name_plural': 'Recorded news',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Estado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ibge', models.IntegerField(unique=True, verbose_name='Unique ID')),
                ('nome', models.CharField(max_length=255, verbose_name='Name')),
                ('uf', models.CharField(max_length=2, unique=True, verbose_name='Short name')),
                ('regiao', models.CharField(blank=True, choices=[('NORTE', 'Região Norte'), ('NORDESTE', 'Região Nordeste'), ('CENTRO-OESTE', 'Região Centro-Oeste'), ('SUDESTE', 'Região Sudeste'), ('SUL', 'Região Sul')], help_text='Brazil only', max_length=15, null=True, verbose_name='Region')),
                ('pais', models.CharField(max_length=255, null=True, verbose_name='Country')),
            ],
            options={
                'verbose_name_plural': 'Country States',
                'ordering': ['uf'],
            },
        ),
        migrations.CreateModel(
            name='PalavraChave',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('palavra_chave', models.CharField(max_length=255, verbose_name='Keywords')),
                ('data_inicio', models.DateField(blank=True, null=True, verbose_name='Start date')),
            ],
            options={
                'verbose_name_plural': 'keywords',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='SiteNoticia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255, verbose_name='Name')),
                ('url', models.CharField(max_length=255)),
                ('acessar_pagina_interna', models.CharField(choices=[('S', 'Yes'), ('N', 'No')], max_length=1, verbose_name='access the internal url')),
                ('tipo_paginacao', models.CharField(blank=True, choices=[('', 'No pagination'), ('url', 'Pagination by url'), ('url_backend', 'Pagination by backend request'), ('elemento_html', 'Pagination by html tag')], max_length=100, null=True, verbose_name='Pagination type')),
                ('json_args', models.TextField(blank=True, null=True)),
                ('req_response', models.CharField(blank=True, max_length=255, null=True)),
                ('estado', models.ForeignKey(blank=True, db_column='uf', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='coleta.estado', to_field='uf', verbose_name='State')),
            ],
            options={
                'verbose_name_plural': 'News websites',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Projeto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255, verbose_name='Name')),
                ('data_inicio', models.DateField(blank=True, null=True, verbose_name='Start date')),
                ('ativo', models.CharField(choices=[('S', 'Yes'), ('N', 'No')], max_length=1, verbose_name='Active')),
                ('palavras_chaves', models.ManyToManyField(blank=True, to='coleta.palavrachave', verbose_name='keywords')),
                ('sites', models.ManyToManyField(blank=True, to='coleta.sitenoticia')),
            ],
            options={
                'verbose_name_plural': 'Project',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_coleta', models.CharField(blank=True, max_length=100, null=True)),
                ('url', models.CharField(blank=True, max_length=355, null=True)),
                ('titulo', models.CharField(blank=True, max_length=355, null=True, verbose_name='Title')),
                ('erro', models.TextField(blank=True, null=True, verbose_name='Error')),
                ('inserido_em', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('conteudo_noticia', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='coleta.conteudonoticia', verbose_name='Nóticia')),
                ('palavra_chave', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='coleta.palavrachave', verbose_name='Keywords')),
                ('projeto', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='coleta.projeto', verbose_name='Project')),
                ('site', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='coleta.sitenoticia')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='LocalInteresse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sentenca', models.TextField(help_text='Separated by comma', verbose_name='phrase')),
                ('projeto', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='local_interessante', to='coleta.projeto')),
            ],
        ),
        migrations.CreateModel(
            name='InitEstruturaNoticia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=255)),
                ('caminho', models.CharField(blank=True, max_length=255, null=True, verbose_name='Path')),
                ('data_inicio', models.DateField(blank=True, null=True, verbose_name='Start date')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coleta.sitenoticia')),
            ],
            options={
                'verbose_name_plural': 'Initial structure for the news websites (html)',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='EstruturaNoticia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=255)),
                ('caminho', models.CharField(blank=True, max_length=255, null=True, verbose_name='Path')),
                ('data_inicio', models.DateField(blank=True, null=True, verbose_name='Start date')),
                ('tipo_pagina', models.CharField(choices=[('lista', 'Attribute in news list')], max_length=100, verbose_name='Page type')),
                ('subtag', models.CharField(blank=True, max_length=255, null=True)),
                ('subtag_caminho', models.CharField(blank=True, max_length=255, null=True, verbose_name='Subtag Path')),
                ('campo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coleta.campo', verbose_name='Field')),
                ('inicio_estrutura_noticia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coleta.initestruturanoticia', verbose_name='Initial structure')),
            ],
            options={
                'verbose_name_plural': 'News list structure (html)',
                'ordering': ['id'],
            },
        ),
        migrations.AddField(
            model_name='conteudonoticia',
            name='estado',
            field=models.ForeignKey(db_column='estado', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='coleta.estado', to_field='uf', verbose_name='State'),
        ),
        migrations.AddField(
            model_name='conteudonoticia',
            name='inicio_estrutura_noticia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coleta.initestruturanoticia', verbose_name='Initial structure'),
        ),
        migrations.AddField(
            model_name='conteudonoticia',
            name='palavras_chaves',
            field=models.ManyToManyField(related_name='palavra_por_noticia', to='coleta.palavrachave', verbose_name='keywords'),
        ),
        migrations.AddField(
            model_name='conteudonoticia',
            name='projeto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coleta.projeto', verbose_name='Project'),
        ),
        migrations.AddField(
            model_name='conteudonoticia',
            name='site',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coleta.sitenoticia'),
        ),
        migrations.AddField(
            model_name='cidade',
            name='estado',
            field=models.ForeignKey(db_column='uf', on_delete=django.db.models.deletion.DO_NOTHING, to='coleta.estado', to_field='uf', verbose_name='State'),
        ),
    ]
