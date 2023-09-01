from django.urls import path

from .views import *

app_name = 'dashboard'
urlpatterns = [
  path('projeto/<int:projeto_id>', projeto_view, name='projeto'),
  path('projeto/<int:projeto_id>/processamento', processamento_view, name='processamento'),
  path('projeto/<int:projeto_id>/graficos', graficos_view, name='graficos'),
  path('projeto/<int:projeto_id>/pontuacoes', pontuacoes_view, name='pontuacoes')
]