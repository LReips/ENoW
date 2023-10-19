import os
import pathlib
import random
import uuid
import csv

from django.db.models import (
  Count, Subquery, Q
)

from coleta.models import (
  ConteudoNoticia
)

from processamento.models import (
  NoticiaProcessada
)

from processamento.services import ROTULOS_NOTICIAS

def buscar_dados_projeto(projeto):
  chaves = []
  
  #Agrupando palavras-chaves, sites e qtd de noticias
  for palavra_chave in projeto.palavras_chaves.all():
    chave_obj = {
      "id": palavra_chave.id,
      "chave": palavra_chave.palavra_chave,
      "sites": []
    }

    for site in projeto.sites.all():
      site_obj = {
        "site": site.nome,
        "noticias": ConteudoNoticia.objects.filter(projeto=projeto, site=site, palavras_chaves=palavra_chave).count()
      }

      chave_obj['sites'].append(site_obj)

    chaves.append(chave_obj)

  #Buscando as noticias processadas (filtradas como sendo de fato o objeto de busca do projeto)
  noticias_processadas = NoticiaProcessada.objects.select_related().filter(
    noticia__projeto=projeto
  )
  
  return chaves, noticias_processadas
