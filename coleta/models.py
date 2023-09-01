from django.db import models

SIM_NAO_OPCAO = [('S', 'SIM'), ('N','NÃO')]

REGIOES_BRASIL = [
  ('NORTE', 'Região Norte'),
  ('NORDESTE', 'Região Nordeste'),
  ('CENTRO-OESTE', 'Região Centro-Oeste'),
  ('SUDESTE', 'Região Sudeste'),
  ('SUL', 'Região Sul')
]

class Estado(models.Model):
  ibge = models.IntegerField(unique=True)
  nome = models.CharField(max_length=255)
  uf = models.CharField(max_length=2, unique=True)
  regiao = models.CharField(max_length=15, choices=REGIOES_BRASIL)

  class Meta:
    ordering = ['uf']

  def __str__(self):
    return '{} - {}'.format(self.uf, self.nome)

class Cidade(models.Model):
  ibge = models.IntegerField(unique=True)
  nome = models.CharField(max_length=355)
  estado = models.ForeignKey(Estado, to_field="uf", db_column="uf", on_delete=models.DO_NOTHING)
  latitude = models.CharField(max_length=30, blank=True)
  longitude = models.CharField(max_length=30, blank=True)

  class Meta:
    ordering = ['id']

  def __str__(self):
    return '{} - {}'.format(self.id, self.nome)

class SiteNoticia(models.Model):
  TIPO_PAGINACAO = [
    ('', 'Sem paginação'),
    ('url', 'Url simples'),
    ('url_backend', 'Url via backend'),
    ('elemento_html', 'Elemento html')
  ]

  nome = models.CharField(max_length=255, null=False)
  url = models.CharField(max_length=255, null=False)
  estado = models.ForeignKey(Estado, to_field="uf", db_column="uf", on_delete=models.DO_NOTHING)
  pais = models.CharField(max_length=255, null=True, blank=True)
  acessar_pagina_interna = models.CharField(max_length=1, choices = SIM_NAO_OPCAO,null=False)
  tipo_paginacao = models.CharField(max_length=100, choices = TIPO_PAGINACAO, null=True, blank=True)
  json_args = models.TextField(null=True, blank=True)
  req_response = models.CharField(max_length=255, null=True, blank=True)

  class Meta:
    ordering = ['id']
    verbose_name_plural = 'Sites de notícias'

  def __str__(self):
    return '{} - {}'.format(self.id, self.nome) 

class PalavraChave(models.Model):
  palavra_chave = models.CharField(max_length=255, null=False)
  data_inicio = models.DateField(null=True, blank=True)

  class Meta:
    ordering = ['id']

  def __str__(self):
    return '{} - {}'.format(self.id, self.palavra_chave) 

class Campo(models.Model):
  tipo =  models.CharField(max_length=255, null=False, help_text="Cadastrar sem acentos")

  class Meta:
    ordering = ['id']

  def __str__(self):
    return '{} - {}'.format(self.id, self.tipo)

class InitEstruturaNoticia(models.Model):
  tag = models.CharField(max_length=255, null=False)
  caminho = models.CharField(max_length=255, null=True, blank=True)
  site = models.ForeignKey(SiteNoticia, on_delete=models.CASCADE)
  data_inicio = models.DateField(null=True, blank=True)

  class Meta:
    ordering = ['id']
    verbose_name_plural = 'Estrutura inicial de lista de notícias'

  def __str__(self):
    return 'Estrutura inicial de notícias {} | {}'.format(self.id, self.site.nome)

class EstruturaNoticia(models.Model):
  TIPO_PAGINA_OPCAO = [
    ('lista', 'Atributo na lista de notícias')
  ]
  
  tag = models.CharField(max_length=255, null=False)
  caminho = models.CharField(max_length=255, null=True, blank=True)
  data_inicio = models.DateField(null=True, blank=True)
  inicio_estrutura_noticia = models.ForeignKey(InitEstruturaNoticia, on_delete=models.CASCADE)
  tipo_pagina = models.CharField(max_length=100, null=False, choices=TIPO_PAGINA_OPCAO)
  campo = models.ForeignKey(Campo, on_delete=models.CASCADE)
  subtag = models.CharField(max_length=255, null=True, blank=True)
  subtag_caminho = models.CharField(max_length=255, null=True, blank=True)

  class Meta:
    ordering = ['id']
    verbose_name_plural = 'Estrutura de lista de notícias'

  def __str__(self):
    return 'Estrutura de notícia {} - {} | {}'.format(self.id, self.campo.tipo, self.inicio_estrutura_noticia.site.nome)

class Projeto(models.Model):
  nome = models.CharField(max_length=255, null=False)
  data_inicio = models.DateField(null=True, blank=True)
  ativo = models.CharField(max_length=1, choices = SIM_NAO_OPCAO,null=False)

  sites = models.ManyToManyField(SiteNoticia, blank=True)
  palavras_chaves = models.ManyToManyField(PalavraChave, blank=True)

  class Meta:
    ordering = ['id']

  def __str__(self):
    return '{} - {}'.format(self.id, self.nome)

class ConteudoNoticia(models.Model):
  titulo = models.CharField(max_length=300, null=False, blank=True)
  descricao = models.TextField(null=True, blank=True)
  conteudo = models.TextField(null=True, blank=True)
  dia = models.CharField(max_length=20,null=True, blank=True)
  mes = models.CharField(max_length=20,null=True, blank=True)
  ano = models.CharField(max_length=20,null=True, blank=True)
  data_formatada = models.CharField(max_length=100,null=True, blank=True)
  estado = models.ForeignKey(Estado, to_field="uf", db_column="estado", on_delete=models.DO_NOTHING, null=True)
  cidade = models.ForeignKey(Cidade, to_field="ibge", db_column="cidade", on_delete=models.DO_NOTHING, null=True)
  imagem = models.CharField(max_length=355,null=True, blank=True)
  url = models.CharField(max_length=355,null=True, blank=True)
  caminho_img_local = models.CharField(max_length=355,null=True, blank=True)
  id_coleta = models.CharField(max_length=100,null=True, blank=True)
  data_coleta = models.DateTimeField(auto_now_add=True)
  
  inicio_estrutura_noticia = models.ForeignKey(InitEstruturaNoticia, on_delete=models.CASCADE)
  site = models.ForeignKey(SiteNoticia, on_delete=models.CASCADE)
  projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE)

  palavras_chaves = models.ManyToManyField(PalavraChave, "palavra_por_noticia")

  class Meta:
    ordering = ['id']
    verbose_name_plural = 'Notícias coletadas'

  def __str__(self):
    return '{} - {} | {} | {}'.format(self.id, self.titulo, self.site.nome, self.projeto.nome)

class Log(models.Model):
  id_coleta = models.CharField(max_length=100,null=True, blank=True)
  url = models.CharField(max_length=355,null=True, blank=True)
  titulo = models.CharField(max_length=355,null=True, blank=True)
  erro = models.TextField(null=True, blank=True)
  inserido_em = models.DateTimeField(auto_now_add=True)
  
  conteudo_noticia = models.ForeignKey(ConteudoNoticia, null=True, on_delete=models.CASCADE)
  site = models.ForeignKey(SiteNoticia, null=True, on_delete=models.CASCADE)
  projeto = models.ForeignKey(Projeto, null=True, on_delete=models.CASCADE)
  palavra_chave = models.ForeignKey(PalavraChave, null=True, on_delete=models.CASCADE)

  class Meta:
    ordering = ['id']

  def __str__(self):
    titulo = 'Sem notícia'
    if self.conteudo_noticia is not None:
      titulo = self.conteudo_noticia.titulo
    return '{} - {} | {} | {}'.format(self.id, titulo, self.site.nome, self.projeto.nome)

class LocalInteresse(models.Model):
  projeto = models.OneToOneField(Projeto, on_delete=models.CASCADE, related_name="local_interessante")
  sentenca = models.TextField(help_text='Separado por virgula')