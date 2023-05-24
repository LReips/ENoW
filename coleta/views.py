from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from coleta.models import Projeto
from coletor_lib.coleta import Coleta

@login_required(login_url='/admin/login')
def index(request):
  context = {
    'projetos': Projeto.objects.all()
  }
  return render(request, 'coleta/index.html', context)

@login_required(login_url='/admin/login')
def executar_coleta(request, projeto_id, palavra_chave):
  coleta = Coleta(projeto_id, palavra_chave)
  coleta.executar()

  data = {'projeto': projeto_id, 'palavra_chave': palavra_chave}
  return JsonResponse(data)