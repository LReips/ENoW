from django.db import models

from coleta.traducoes import traduzir

SIM_NAO_OPCAO = [('S', traduzir('SIM')), ('N',traduzir('NÃO'))]

REGIOES_BRASIL = [
  ('NORTE', 'Região Norte'),
  ('NORDESTE', 'Região Nordeste'),
  ('CENTRO-OESTE', 'Região Centro-Oeste'),
  ('SUDESTE', 'Região Sudeste'),
  ('SUL', 'Região Sul')
]

class Estado(models.Model):
  ibge = models.IntegerField(unique=True, verbose_name=traduzir("Código do IBGE"))
  nome = models.CharField(max_length=255, verbose_name=traduzir("Nome"))
  uf = models.CharField(max_length=2, unique=True, verbose_name=traduzir("UF"))
  regiao = models.CharField(max_length=15, choices=REGIOES_BRASIL, null=True, blank=True, verbose_name=traduzir("Região"), help_text=traduzir("Apenas Brasil"))
  pais = models.CharField(max_length=255, null=True, verbose_name=traduzir("País"))

  class Meta:
    ordering = ['uf']
    verbose_name_plural = traduzir('Estados')

  def __str__(self):
    return '{} - {}'.format(self.uf, self.nome)

class Cidade(models.Model):
  ibge = models.IntegerField(unique=True, verbose_name=traduzir("Código do IBGE"))
  nome = models.CharField(max_length=355, verbose_name=traduzir("Nome"))
  estado = models.ForeignKey(Estado, to_field="uf", db_column="uf", on_delete=models.DO_NOTHING, verbose_name=traduzir("Estado"))
  latitude = models.CharField(max_length=30, blank=True)
  longitude = models.CharField(max_length=30, blank=True)

  class Meta:
    ordering = ['id']
    verbose_name_plural = traduzir('Cidades')

  def __str__(self):
    return '{} - {}'.format(self.id, self.nome)

class SiteNoticia(models.Model):
  TIPO_PAGINACAO = [
    ('', traduzir('Sem paginação')),
    ('url', traduzir('Url simples')),
    ('url_backend', traduzir('Url via backend')),
    ('elemento_html', traduzir('Elemento html'))
  ]

  nome = models.CharField(max_length=255, null=False, verbose_name=traduzir("Nome"))
  url = models.CharField(max_length=255, null=False)
  estado = models.ForeignKey(Estado, to_field="uf", db_column="uf", on_delete=models.DO_NOTHING, null=True, blank=True, verbose_name=traduzir("Estado"))
  acessar_pagina_interna = models.CharField(max_length=1, choices = SIM_NAO_OPCAO,null=False, verbose_name=traduzir("Acessar página interna"))
  tipo_paginacao = models.CharField(max_length=100, choices = TIPO_PAGINACAO, null=True, blank=True, verbose_name=traduzir("Tipo de paginação"))
  json_args = models.TextField(null=True, blank=True)
  req_response = models.CharField(max_length=255, null=True, blank=True)

  class Meta:
    ordering = ['id']
    verbose_name_plural = traduzir('Sites de notícias')

  def __str__(self):
    return '{} - {}'.format(self.id, self.nome) 

class PalavraChave(models.Model):
  palavra_chave = models.CharField(max_length=255, null=False, verbose_name=traduzir('Palavra-chave'))
  data_inicio = models.DateField(null=True, blank=True, verbose_name=traduzir('Data de Início'))

  class Meta:
    ordering = ['id']
    verbose_name_plural = traduzir('Palavras-chaves')

  def __str__(self):
    return '{} - {}'.format(self.id, self.palavra_chave) 

class Campo(models.Model):
  tipo =  models.CharField(max_length=255, null=False, help_text=traduzir("Cadastrar sem acentos"), verbose_name=traduzir('Tipo'))

  class Meta:
    ordering = ['id']
    verbose_name_plural = traduzir('Campos')

  def __str__(self):
    return '{} - {}'.format(self.id, self.tipo)

class InitEstruturaNoticia(models.Model):
  tag = models.CharField(max_length=255, null=False)
  caminho = models.CharField(max_length=255, null=True, blank=True, verbose_name=traduzir('Caminho'))
  site = models.ForeignKey(SiteNoticia, on_delete=models.CASCADE)
  data_inicio = models.DateField(null=True, blank=True, verbose_name=traduzir('Data de Início'))

  class Meta:
    ordering = ['id']
    verbose_name_plural = traduzir('Estrutura inicial de lista de notícias')

  def __str__(self):
    return traduzir('Estrutura inicial de notícias') + ' {} | {}'.format(self.id, self.site.nome)

class EstruturaNoticia(models.Model):
  TIPO_PAGINA_OPCAO = [
    ('lista', traduzir('Atributo na lista de notícias'))
  ]
  
  tag = models.CharField(max_length=255, null=False)
  caminho = models.CharField(max_length=255, null=True, blank=True, verbose_name=traduzir('Caminho'))
  data_inicio = models.DateField(null=True, blank=True, verbose_name=traduzir('Data de Início'))
  inicio_estrutura_noticia = models.ForeignKey(InitEstruturaNoticia, on_delete=models.CASCADE, verbose_name=traduzir('Estrutura Inicial'))
  tipo_pagina = models.CharField(max_length=100, null=False, choices=TIPO_PAGINA_OPCAO, verbose_name=traduzir('Tipo de página'))
  campo = models.ForeignKey(Campo, on_delete=models.CASCADE, verbose_name=traduzir('Campo'))
  subtag = models.CharField(max_length=255, null=True, blank=True)
  subtag_caminho = models.CharField(max_length=255, null=True, blank=True, verbose_name=traduzir('Caminho para a subtag'))

  class Meta:
    ordering = ['id']
    verbose_name_plural = traduzir('Estrutura de lista de notícias')

  def __str__(self):
    return traduzir('Estrutura de notícia') + ' {} - {} | {}'.format(self.id, self.campo.tipo, self.inicio_estrutura_noticia.site.nome)

class Projeto(models.Model):
  nome = models.CharField(max_length=255, null=False, verbose_name=traduzir('Nome'))
  data_inicio = models.DateField(null=True, blank=True, verbose_name=traduzir('Data de início'))
  ativo = models.CharField(max_length=1, choices = SIM_NAO_OPCAO,null=False, verbose_name=traduzir('Ativo'))

  sites = models.ManyToManyField(SiteNoticia, blank=True)
  palavras_chaves = models.ManyToManyField(PalavraChave, blank=True, verbose_name=traduzir('Palavras-chaves'))

  class Meta:
    ordering = ['id']
    verbose_name_plural = traduzir('Projeto')

  def __str__(self):
    return '{} - {}'.format(self.id, self.nome)

class ConteudoNoticia(models.Model):
  titulo = models.CharField(max_length=300, null=False, blank=True, verbose_name=traduzir('Título'))
  descricao = models.TextField(null=True, blank=True, verbose_name=traduzir('Descrição'))
  conteudo = models.TextField(null=True, blank=True, verbose_name=traduzir('Conteúdo'))
  dia = models.CharField(max_length=20,null=True, blank=True, verbose_name=traduzir('Dia'))
  mes = models.CharField(max_length=20,null=True, blank=True, verbose_name=traduzir('Mês'))
  ano = models.CharField(max_length=20,null=True, blank=True, verbose_name=traduzir('Ano'))
  data_formatada = models.CharField(max_length=100,null=True, blank=True, verbose_name=traduzir('Data da notícia'))
  estado = models.ForeignKey(Estado, to_field="uf", db_column="estado", on_delete=models.DO_NOTHING, null=True, verbose_name=traduzir('Estado'))
  cidade = models.ForeignKey(Cidade, to_field="ibge", db_column="cidade", on_delete=models.DO_NOTHING, null=True, verbose_name=traduzir('Cidade'))
  imagem = models.CharField(max_length=355,null=True, blank=True, verbose_name=traduzir('Imagem'))
  url = models.CharField(max_length=355,null=True, blank=True)
  caminho_img_local = models.CharField(max_length=355,null=True, blank=True, verbose_name=traduzir('Caminho da imagem'))
  id_coleta = models.CharField(max_length=100,null=True, blank=True)
  data_coleta = models.DateTimeField(auto_now_add=True, verbose_name=traduzir('Data da coleta'))
  
  inicio_estrutura_noticia = models.ForeignKey(InitEstruturaNoticia, on_delete=models.CASCADE, verbose_name=traduzir('Estrutura inicial'))
  site = models.ForeignKey(SiteNoticia, on_delete=models.CASCADE)
  projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, verbose_name=traduzir('Projeto'))

  palavras_chaves = models.ManyToManyField(PalavraChave, "palavra_por_noticia", verbose_name=traduzir('Palavras-chaves'))

  class Meta:
    ordering = ['id']
    verbose_name_plural = traduzir('Notícias coletadas')

  def __str__(self):
    return '{} - {} | {} | {}'.format(self.id, self.titulo, self.site.nome, self.projeto.nome)

class Log(models.Model):
  id_coleta = models.CharField(max_length=100,null=True, blank=True)
  url = models.CharField(max_length=355,null=True, blank=True)
  titulo = models.CharField(max_length=355,null=True, blank=True, verbose_name=traduzir('Título'))
  erro = models.TextField(null=True, blank=True, verbose_name=traduzir('Erro'))
  inserido_em = models.DateTimeField(auto_now_add=True, verbose_name=traduzir('Inserido em'))
  
  conteudo_noticia = models.ForeignKey(ConteudoNoticia, null=True, on_delete=models.CASCADE, verbose_name=traduzir('Nóticia'))
  site = models.ForeignKey(SiteNoticia, null=True, on_delete=models.CASCADE)
  projeto = models.ForeignKey(Projeto, null=True, on_delete=models.CASCADE, verbose_name=traduzir('Projeto'))
  palavra_chave = models.ForeignKey(PalavraChave, null=True, on_delete=models.CASCADE, verbose_name=traduzir('Palavra-chave'))

  class Meta:
    ordering = ['id']

  def __str__(self):
    titulo = traduzir('Sem notícia')
    if self.conteudo_noticia is not None:
      titulo = self.conteudo_noticia.titulo
    return '{} - {} | {} | {}'.format(self.id, titulo, self.site.nome, self.projeto.nome)

class LocalInteresse(models.Model):
  projeto = models.OneToOneField(Projeto, on_delete=models.CASCADE, related_name="local_interessante")
  sentenca = models.TextField(help_text=traduzir('Separado por virgula'), verbose_name=traduzir('Sentença'))
