from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings

if settings.LANGUAGE_CODE == 'pt-br':
  admin.site.site_header = 'Administração | Coleta de Notícias'

urlpatterns = [
  path('admin/', admin.site.urls),
  path('coleta/', include('coleta.urls')),
  path('processamento/', include('processamento.urls')),
  path('dashboard/', include('dashboard.urls')),
  path('', RedirectView.as_view(url='coleta', permanent=False))
]