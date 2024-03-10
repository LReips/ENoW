from django.db import models 

from coleta.models import (Projeto, ConteudoNoticia)
from coleta.traducoes import traduzir

class NoticiaProcessada(models.Model):
  noticia = models.ForeignKey(ConteudoNoticia, on_delete=models.CASCADE, verbose_name=traduzir('Notícia'))
  estado = models.TextField(null=True, verbose_name=traduzir('Estado'))
  cidade = models.TextField(null=True, verbose_name=traduzir('Cidade'))
  localizacao = models.TextField(null=True, verbose_name=traduzir('Localização'))
  palavras_chaves = models.TextField(verbose_name='Palavras-chaves')
  
  class Meta:
    ordering = ['id']
    verbose_name_plural = traduzir('Notícias processadas')

  def __str__(self):
    return 'Processamento: {} | Noticia: {} - {}'.format(self.id, self.noticia.id, self.noticia.titulo)

class ResultadoProcessamento(models.Model):
  id_processamento = models.CharField(max_length=30, verbose_name=traduzir('Execution ID'))
  criado_em = models.DateTimeField(auto_now_add=True, verbose_name=traduzir('Criado em'))
  projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, verbose_name=traduzir('Projeto'))
  acuracia = models.DecimalField(max_digits=10, decimal_places=4, null=True, verbose_name=traduzir('Acurácia'))
  precisao = models.DecimalField(max_digits=10, decimal_places=4, null=True, verbose_name=traduzir('Precisão'))
  recall = models.DecimalField(max_digits=10, decimal_places=4, null=True)
  f1_score = models.DecimalField(max_digits=10, decimal_places=4, null=True)
  vp = models.IntegerField(null=True, verbose_name=traduzir('Verdadeiro positivo (VP)'))
  vn = models.IntegerField(null=True, verbose_name=traduzir('Verdadeiro negativo (VN)'))
  fp = models.IntegerField(null=True, verbose_name=traduzir('Falso positivo (FP)'))
  fn = models.IntegerField(null=True, verbose_name=traduzir('Falso negativo (FN)'))

  class Meta:
    ordering = ['id_processamento', 'criado_em']
    verbose_name_plural = traduzir('Resultado do processamento')

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
  projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, null=True, verbose_name=traduzir('Projeto'))
  processamento = models.ForeignKey(ResultadoProcessamento, on_delete=models.CASCADE, null=True, verbose_name=traduzir('Execution'))
  modelo = models.CharField(max_length=30, verbose_name=traduzir('Modelo'))
  acuracia = models.DecimalField(max_digits=10, decimal_places=4, null=True, verbose_name=traduzir('Acurácia'))
  precisao = models.DecimalField(max_digits=10, decimal_places=4, null=True, verbose_name=traduzir('Precisão'))
  recall = models.DecimalField(max_digits=10, decimal_places=4, null=True)
  f1_score = models.DecimalField(max_digits=10, decimal_places=4, null=True)
  qtd_noticias = models.IntegerField(null=True, verbose_name=traduzir('Quantidade de notícias'))
  vp = models.IntegerField(null=True, verbose_name=traduzir('Verdadeiro positivo (VP)'))
  vn = models.IntegerField(null=True, verbose_name=traduzir('Verdadeiro negativo (VN)'))
  fp = models.IntegerField(null=True, verbose_name=traduzir('Falso positivo (FP)'))
  fn = models.IntegerField(null=True, verbose_name=traduzir('Falso negativo (FN)'))
  matriz_confusao = models.TextField(null=True, verbose_name=traduzir('Matriz de confusão'))

  class Meta:
    ordering = ['processamento', 'projeto']
    verbose_name_plural = traduzir('Classificação de modelos')