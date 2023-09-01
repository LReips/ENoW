from django.urls import path

from . import views

app_name = 'coleta'
urlpatterns = [
  path('', views.index, name='index'),
  path('executar_coleta/<int:projeto_id>/<int:palavra_chave_id>', views.executar_coleta, name='executar_coleta')
]