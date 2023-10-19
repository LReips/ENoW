from django.db import models 

from coleta.models import (Projeto, ConteudoNoticia)

class NoticiaProcessada(models.Model):
  noticia = models.ForeignKey(ConteudoNoticia, on_delete=models.CASCADE)
  estado = models.TextField(null=True)
  cidade = models.TextField(null=True)
  localizacao = models.TextField(null=True)
  palavras_chaves = models.TextField()
  
  class Meta:
    ordering = ['id']
    verbose_name_plural = 'Notícias processadas'

  def __str__(self):
    return 'Processamento: {} | Noticia: {} - {}'.format(self.id, self.noticia.id, self.noticia.titulo)

class ResultadoProcessamento(models.Model):
  id_processamento = models.CharField(max_length=30)
  criado_em = models.DateTimeField(auto_now_add=True)
  projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE)
  acuracia = models.DecimalField(max_digits=10, decimal_places=4, null=True)
  precisao = models.DecimalField(max_digits=10, decimal_places=4, null=True)
  recall = models.DecimalField(max_digits=10, decimal_places=4, null=True)
  f1_score = models.DecimalField(max_digits=10, decimal_places=4, null=True)
  vp = models.IntegerField(null=True)
  vn = models.IntegerField(null=True)
  fp = models.IntegerField(null=True)
  fn = models.IntegerField(null=True)

  class Meta:
    ordering = ['id_processamento', 'criado_em']

class NoticiaReferenciaProcessamento(models.Model):
  processamento = models.ForeignKey(ResultadoProcessamento, on_delete=models.CASCADE)
  noticia = models.ForeignKey(ConteudoNoticia, on_delete=models.DO_NOTHING)
  noticia_real = models.CharField(max_length=3, choices=[('S', 'Sim'), ( 'N', 'Não')])

class NoticiaResultadoProcessamento(models.Model):
  processamento = models.ForeignKey(ResultadoProcessamento, on_delete=models.CASCADE)
  noticia = models.ForeignKey(ConteudoNoticia, on_delete=models.DO_NOTHING)
  rotulo_real = models.CharField(max_length=10)
  rotulo_calculado = models.CharField(max_length=10)
  pontuacao_real = models.DecimalField(max_digits=10, decimal_places=4, null=True)
  pontuacao_nao_real = models.DecimalField(max_digits=10, decimal_places=4, null=True)
  classificadores = models.TextField(max_length=200, null=True, blank=True)

class ClassificacaoModelo(models.Model):
  projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, null=True)
  processamento = models.ForeignKey(ResultadoProcessamento, on_delete=models.CASCADE, null=True)
  modelo = models.CharField(max_length=30)
  acuracia = models.DecimalField(max_digits=10, decimal_places=4, null=True)
  precisao = models.DecimalField(max_digits=10, decimal_places=4, null=True)
  recall = models.DecimalField(max_digits=10, decimal_places=4, null=True)
  f1_score = models.DecimalField(max_digits=10, decimal_places=4, null=True)
  qtd_noticias = models.IntegerField(null=True)
  vp = models.IntegerField(null=True)
  vn = models.IntegerField(null=True)
  fp = models.IntegerField(null=True)
  fn = models.IntegerField(null=True)
  matriz_confusao = models.TextField(null=True)

  class Meta:
    ordering = ['processamento', 'projeto']