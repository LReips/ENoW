from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from coleta.models import (
  Projeto, ConteudoNoticia
)

from .services import *

@login_required(login_url='/admin/login')
def projeto_view(request, projeto_id):
  projeto = Projeto.objects.get(pk=projeto_id)
  chaves, noticias_processadas = buscar_dados_projeto(projeto)
  context = {
    "projeto": projeto,
    "chaves": chaves,
    "noticias_processadas": noticias_processadas
  }
  return render(request, 'dashboard/projeto.html', context)

@login_required(login_url='/admin/login')
def processamento_view(request, projeto_id):
  projeto = Projeto.objects.get(pk=projeto_id)
  context = {
    "projeto": projeto,
    "noticias": ConteudoNoticia.objects.filter(projeto=projeto)
  }
  return render(request, 'dashboard/processamento.html', context)
