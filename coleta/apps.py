from django.apps import AppConfig

from coleta.traducoes import traduzir


class ColetaConfig(AppConfig):
  default_auto_field = 'django.db.models.BigAutoField'
  name = 'coleta'
  verbose_name = traduzir('Coleta')
