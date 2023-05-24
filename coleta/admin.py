from django.contrib import admin
from .models import Projeto, PalavraChave, SiteNoticia, Campo, InitEstruturaNoticia, EstruturaNoticia, ConteudoNoticia, Log

class SiteNoticiaAdmin(admin.ModelAdmin):
  list_filter = ('tipo_paginacao', )
  list_display = ('id','nome','acessar_pagina_interna')

class InitEstruturaNoticiaAdmin(admin.ModelAdmin):
  list_filter = ('site', )

class EstruturaNoticiaAdmin(admin.ModelAdmin):
  list_filter = ('campo', 'inicio_estrutura_noticia__site',)

class ConteudoNoticiaAdmin(admin.ModelAdmin):
  list_filter = ('projeto', 'site')

admin.site.register(SiteNoticia, SiteNoticiaAdmin)
admin.site.register(InitEstruturaNoticia, InitEstruturaNoticiaAdmin)
admin.site.register(EstruturaNoticia, EstruturaNoticiaAdmin)
admin.site.register(ConteudoNoticia, ConteudoNoticiaAdmin)

admin.site.register([Projeto, PalavraChave, Campo])