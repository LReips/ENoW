from django.contrib import admin
from .models import *

class EstadoAdmin(admin.ModelAdmin):
  list_display = ('id', 'pais', 'nome')

class ProjetoLocalInteresse(admin.StackedInline):
  model = LocalInteresse

class ProjetoAdmin(admin.ModelAdmin):
  inlines = (ProjetoLocalInteresse,)
  list_display = ('id', 'nome')

class SiteNoticiaAdmin(admin.ModelAdmin):
  list_filter = ('tipo_paginacao', 'estado')
  list_display = ('id','nome','acessar_pagina_interna', 'tipo_paginacao')

class InitEstruturaNoticiaAdmin(admin.ModelAdmin):
  list_filter = ('site', )

class EstruturaNoticiaAdmin(admin.ModelAdmin):
  list_filter = ('campo', 'inicio_estrutura_noticia__site',)

class ConteudoNoticiaAdmin(admin.ModelAdmin):
  list_filter = ('site', )

admin.site.register(Estado, EstadoAdmin)
admin.site.register(Cidade)
admin.site.register(Projeto, ProjetoAdmin)
admin.site.register(SiteNoticia, SiteNoticiaAdmin)
admin.site.register(InitEstruturaNoticia, InitEstruturaNoticiaAdmin)
admin.site.register(EstruturaNoticia, EstruturaNoticiaAdmin)
admin.site.register(ConteudoNoticia, ConteudoNoticiaAdmin)

admin.site.register([PalavraChave, Campo])
