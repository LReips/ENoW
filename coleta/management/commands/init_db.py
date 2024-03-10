import environ
import os

from django.conf import settings
from django.contrib.auth import get_user_model  
from django.core.management.base import BaseCommand
from django.db import connection

from coleta.models import Estado

User = get_user_model()  

class Command(BaseCommand):

  def criar_superusuario(self):
    env = environ.Env()

    username = env('DJANGO_SUPERUSER_USERNAME')
    email = env('DJANGO_SUPERUSER_EMAIL')
    password = env('DJANGO_SUPERUSER_PASSWORD')

    try:  
      if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username, email, password)
    except Exception as e:  
      print(f"Um erro aconteceu ao criar o superusuário: {e}")

  def importar_script(self):
    try:
      if not Estado.objects.all().exists():
        with open(os.path.join(settings.BASE_DIR, 'script.sql'), 'rb') as f:
          with connection.cursor() as c:
            for l in f:
              if l.rstrip() != '':
                c.execute(l)

    except Exception as e:
      print(f"Um erro aconteceu ao cadastrar os dados iniciais (sites de noticia/estruturas): {e}")

  def handle(self, *args, **options):  
    self.criar_superusuario()
    self.importar_script()