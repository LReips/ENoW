from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from .services import (Coleta)
from coleta.models import (Projeto, PalavraChave)

@login_required(login_url='/admin/login')
def index(request):
  context = {
    'projetos': Projeto.objects.all(),
    'idioma': settings.LANGUAGE_CODE
  }
  return render(request, 'coleta/index.html', context)

@login_required(login_url='/admin/login')
def executar_coleta(request, projeto_id, palavra_chave_id):
  projeto = Projeto.objects.get(pk=projeto_id)
  palavra_chave = None
  if palavra_chave_id != 0:
    palavra_chave = PalavraChave.objects.get(pk=palavra_chave_id)

  coleta = Coleta(projeto, palavra_chave)
  coleta.temporizador()

  status = 200
  if coleta.executar() is False:
    status = 400

  tempo = coleta.temporizador()
  return JsonResponse({"tempo": tempo}, status=status)