from django.urls import path

from . import views

app_name = 'processamento'
urlpatterns = [
  path('buscar_noticias/<int:id>', views.carregar_noticias_view, name='carregar_noticias'),
  path('executar_processamento/<int:id>', views.executar_processamento_view, name='executar_processamento'),
  path('carregar_historico/<int:id>', views.carregar_historico_view, name='carregar_historico'),
  path('deletar_noticia/<int:id>', views.deletar_noticia_view, name='deletar_noticia_processada'),
  path('download', views.download_view, name="download"),
  path('testes', views.teste_view)
]