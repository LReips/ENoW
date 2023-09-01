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

from processamento.models import ProcessamentoSbert
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

  #Buscando as noticias possivelmente duplicadas (via a noticia processada)
  noticias_duplicadas = NoticiaProcessada.objects.select_related().filter(
    Q(noticia_processada_a__isnull=False) | Q(noticia_processada_b__isnull=False), noticia__projeto=projeto
  )
  
  return chaves, noticias_processadas, noticias_duplicadas

def buscar_noticias_grafico(projeto):
  processamento_sbert = ProcessamentoSbert.objects.select_related().filter(projeto=projeto)

  rotulos = []
  if str(projeto.id) in ROTULOS_NOTICIAS:
    rotulos = ROTULOS_NOTICIAS[str(projeto.id)]

  dados_prep = {}
  for processamento in processamento_sbert:
    noticia = processamento.noticia
    noticia_referencia = processamento.noticia_referencia
    pontuacao = '{:.2f}'.format(processamento.pontuacao)

    rotulo = 'falsas'
    if str(noticia.id) in rotulos:
      if rotulos[str(noticia.id)] == 1:
        rotulo = 'reais'

    if noticia_referencia.id not in dados_prep:
      dados_prep[noticia_referencia.id] = {
        'reais': {}, 'falsas': {}, 'ref_id': noticia_referencia.id, 
        'noticia_referencia': '{} | {} - {}'.format(noticia_referencia.site.nome, noticia_referencia.id, noticia_referencia.titulo)
      }
    
    if pontuacao not in dados_prep[noticia_referencia.id][rotulo]:
      dados_prep[noticia_referencia.id][rotulo][pontuacao] = 0

    dados_prep[noticia_referencia.id][rotulo][pontuacao] += 1

  return [dados_prep[d] for d in dados_prep]