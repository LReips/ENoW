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

class NoticiaParecida(models.Model):
  projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE)
  noticia_processada_a = models.ForeignKey(NoticiaProcessada, on_delete=models.CASCADE, related_name="noticia_processada_a")
  noticia_processada_b = models.ForeignKey(NoticiaProcessada, on_delete=models.CASCADE, related_name="noticia_processada_b")

  def existe(self):
    return len(NoticiaParecida.objects.filter(
      models.Q(noticia_processada_a=self.noticia_processada_a, noticia_processada_b=self.noticia_processada_b) 
      | models.Q(noticia_processada_a=self.noticia_processada_b, noticia_processada_b=self.noticia_processada_a)
    )) != 0

  class Meta:
    unique_together = ('noticia_processada_a', 'noticia_processada_b')
    ordering = ['id']
    verbose_name_plural = 'Notícias parecidas'

class ProcessamentoSbert(models.Model):
  projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE)
  noticia = models.ForeignKey(ConteudoNoticia, on_delete=models.CASCADE, related_name="noticia_testada")
  noticia_referencia = models.ForeignKey(ConteudoNoticia, on_delete=models.SET_NULL, related_name="noticia_referencia",null=True)
  pontuacao = models.DecimalField(max_digits=10, decimal_places=4)
  criado_em = models.DateTimeField(auto_now_add=True)

  class Meta:
    unique_together = ('noticia', 'noticia_referencia')
    ordering = ['projeto', 'noticia', 'noticia_referencia']
    verbose_name_plural = 'Processamento SBERT de notícias'

class ResultadoProcessamento(models.Model):
  id_processamento = models.CharField(max_length=30)
  criado_em = models.DateTimeField(auto_now_add=True)
  projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE)
  
  limiar = models.DecimalField(max_digits=10, decimal_places=4, null=True)
  margem = models.DecimalField(max_digits=10, decimal_places=4, null=True)
  media_diff_quadrada = models.DecimalField(max_digits=10, decimal_places=4, null=True)
  desvio_padrao = models.DecimalField(max_digits=10, decimal_places=4, null=True)
  limiar_ajustado = models.DecimalField(max_digits=10, decimal_places=4, null=True)

  acuracia = models.DecimalField(max_digits=10, decimal_places=4, null=True)
  precisao = models.DecimalField(max_digits=10, decimal_places=4, null=True)
  recall = models.DecimalField(max_digits=10, decimal_places=4, null=True)
  f1_score = models.DecimalField(max_digits=10, decimal_places=4, null=True)
  
  noticias_referencias = models.ManyToManyField(ConteudoNoticia)

  class Meta:
    ordering = ['id_processamento', 'criado_em']

class ClassificacaoModelo(models.Model):
  processamento = models.ForeignKey(ResultadoProcessamento, on_delete=models.CASCADE)
  modelo = models.CharField(max_length=30)
  acuracia = models.DecimalField(max_digits=10, decimal_places=4, null=True)
  precisao = models.DecimalField(max_digits=10, decimal_places=4, null=True)
  recall = models.DecimalField(max_digits=10, decimal_places=4, null=True)
  f1_score = models.DecimalField(max_digits=10, decimal_places=4, null=True)
  tipo_metrica = models.CharField(max_length=15, choices=[('REAL', 'Rótulos reais (manuais)'), ('CALCULADA', 'Rótulos calculados')], null=True)

  class Meta:
    ordering = ['processamento']