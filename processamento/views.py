import os
from django.conf import settings

from django.http import (JsonResponse,HttpResponse, Http404)
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from .services import *

@require_http_methods(["POST"])
@login_required(login_url='/admin/login')
def gravar_noticias_view(request):
  obj = ProcessamentoSrv()
  resultado, status = obj.gravar_noticias(request.body)
  return JsonResponse(resultado, safe=False, json_dumps_params={'ensure_ascii': False}, status=status)

@require_http_methods(["POST"])
@login_required(login_url='/admin/login')
def executar_processamento_view(request, id):
  obj = ProcessamentoSrv()
  resultado, status = obj.executar_processamento(id, request.body)
  return JsonResponse(resultado, safe=False, json_dumps_params={'ensure_ascii': False}, status=status)

@require_http_methods(["GET"])
@login_required(login_url='/admin/login')
def carregar_historico_view(request, id):
  obj = ProcessamentoSrv()
  id_processamento = None
  
  if 'id_processamento' in request.GET:
    id_processamento = request.GET['id_processamento']

  resultado, status = obj.carregar_historico(id, id_processamento)
  return JsonResponse(resultado, safe=False, json_dumps_params={'ensure_ascii': False}, status=status)

@require_http_methods(["GET"])
@login_required(login_url='/admin/login')
def carregar_noticias_view(request, id):
  obj = ProcessamentoSrv()

  filtrar_noticias = request.GET['filtrar_noticias']
  id_processamento = request.GET['id_processamento']

  resultado, status = obj.buscar_noticias(id, id_processamento, filtrar_noticias)
  return JsonResponse(resultado, safe=False, json_dumps_params={'ensure_ascii': False}, status=status)

@require_http_methods(["DELETE"])
@login_required(login_url='/admin/login')
def deletar_noticia_view(request, id):
  obj = ProcessamentoSrv()
  resultado, status = obj.deletar_noticia_processada(id)
  return JsonResponse(resultado, safe=False, json_dumps_params={'ensure_ascii': False}, status=status)

@require_http_methods(["GET"])
@login_required(login_url='/admin/login')
def download_view(request):
  try:
    file_path = os.path.join(settings.BASE_DIR, 'temp', request.GET['arquivo'])
    if os.path.exists(file_path):
      with open(file_path, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
        response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
        return response
    return JsonResponse({"erro":"Arquivo não encontrado!"}, safe=False, status=400)
  except Exception as e:
    return JsonResponse({"erro":str(e)}, safe=False, status=400)
  