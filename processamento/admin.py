from django.contrib import admin
from .models import *

class NoticiaProcessadaAdmin(admin.ModelAdmin):
  list_filter = ('noticia__projeto', )
  list_display = ('id', 'noticia', 'get_dia', 'get_mes', 'get_ano', 'estado', 'cidade', 'localizacao', 'palavras_chaves')

  @admin.display(ordering='noticia__dia', description='DIA')
  def get_dia(self, obj):
    return obj.noticia.dia

  @admin.display(ordering='noticia__mes', description='MÊS')
  def get_mes(self, obj):
    return obj.noticia.mes

  @admin.display(ordering='noticia__ano', description='ANO')
  def get_ano(self, obj):
    return obj.noticia.ano

  def has_add_permission(self, request, obj=None):
    return False
  
  def has_change_permission(self, request, obj=None):
    return False
  
class ClassificacaoModeloInline(admin.StackedInline):
  extra = 0
  model = ClassificacaoModelo

#class NoticiaReferenciaProcessamentoInline(admin.StackedInline):
#  extra = 0
#  model = NoticiaReferenciaProcessamento

class ResultadoProcessamentoAdmin(admin.ModelAdmin):
  inlines = (ClassificacaoModeloInline, )
  list_filter = ('projeto', )
  list_display = ('id_processamento', 'criado_em', 'projeto', 'acuracia', 'precisao', 'recall', 'f1_score')

admin.site.register(NoticiaProcessada, NoticiaProcessadaAdmin)
admin.site.register(ResultadoProcessamento, ResultadoProcessamentoAdmin)
