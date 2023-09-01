import os
import pathlib
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import calendar
import time
import uuid
import random

from datetime import datetime

from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from newspaper import Article
from .models import *

class Coleta:
  t_ini = None
  projeto = None
  palavra_chave_user = None
  id_coleta = calendar.timegm(time.gmtime())

  site_atual = None
  palavra_chave_atual = None
  temp_site_url_atual = ""

  def __init__(self, projeto, palavra_chave_user):
    self.projeto = projeto
    self.palavra_chave_user = palavra_chave_user

  def temporizador(self):
    if self.t_ini is None:
      self.t_ini = datetime.now()
    else:
      t_fim = datetime.now()
      diff = t_fim - self.t_ini

      return {
        "inicio": self.t_ini.strftime("%H:%M:%S"),
        "fim": t_fim.strftime("%H:%M:%S"),
        "diff_segundos": diff.total_seconds(),
        "diff_minutos": diff.total_seconds() / 60
      }

  def registrar_erro(self, erro = '', titulo = '', conteudo_noticia = None):
    log = Log.objects.create(
      id_coleta = self.id_coleta, projeto = self.projeto,
      palavra_chave = self.palavra_chave_atual, site = self.site_atual,
      url = self.temp_site_url_atual, erro = erro,
      titulo = titulo, conteudo_noticia = conteudo_noticia
    )

  def converter_json(self, json_string):
    try:
      return json.loads(json_string)
    except ValueError as e:
      return False
  
  def deletar_pasta_imagens_vazias(self):
    p_imagens = os.path.join(pathlib.Path().resolve(), "imagens_coletor")
    if os.path.exists(p_imagens):
      for pasta in os.listdir(p_imagens):
        if len(os.listdir(os.path.join(p_imagens, pasta))) == 0:
          os.rmdir(os.path.join(p_imagens, pasta))
  
  def processar_noticia(self, noticia_obj, noticia, estrutura):
    campo = str(estrutura.campo.tipo).lower()
    possui_caminho = str(estrutura.caminho) == '' or estrutura.caminho is None

    dado_coletado = None
    if (possui_caminho):
      dado_coletado = noticia.find(str(estrutura.tag))
    else:
      dado_coletado = noticia.find(str(estrutura.tag), attrs={str(estrutura.caminho)})

    if dado_coletado is not None and estrutura.subtag != '' and estrutura.subtag is not None:
      if (str(estrutura.subtag_caminho) == '' or estrutura.subtag_caminho is None):
        dado_coletado = dado_coletado.find(str(estrutura.subtag))
      else:
        dado_coletado = dado_coletado.find(str(estrutura.subtag), attrs={str(estrutura.subtag_caminho)})

    if(campo == 'titulo'):
      if dado_coletado is not None:
        noticia_obj.noticia.titulo = dado_coletado.text.strip()
    elif(campo == 'url'):
      if dado_coletado is not None:
        noticia_obj.noticia.url = dado_coletado['href']

        if noticia_obj.noticia.url != "":
          if noticia_obj.noticia.url.startswith("/"):
            noticia_obj.noticia.url = self.site_atual.url.split('.br')[0] + '.br' + noticia_obj.noticia.url
    elif(campo == 'data_formatada'):
      if dado_coletado is not None:
        noticia_obj.noticia.data_formatada = dado_coletado.text.strip()
    elif(campo == 'descricao'):
      if dado_coletado is not None:
        noticia_obj.noticia.descricao = dado_coletado.text.strip()
    elif(campo == 'dia'):
      if dado_coletado is not None:
        noticia_obj.noticia.dia = dado_coletado.text.strip()
    elif(campo == 'mes'):
      if dado_coletado is not None:
        noticia_obj.noticia.mes = dado_coletado.text.strip()
    elif(campo == 'ano'):
      if dado_coletado is not None:
        noticia_obj.noticia.ano = dado_coletado.text.strip()
    elif(campo == 'localizacao'):
      if dado_coletado is not None:
        noticia_obj.noticia.localizacao = dado_coletado.text.strip()
    elif(campo == 'imagem'):
      if(dado_coletado):
        noticia_obj.salvar_imagem(dado_coletado)

  def coletar_noticias_site(self, conteudo_site):
    #Buscando a estrutura da lista de noticias
    init_estruturas = InitEstruturaNoticia.objects.filter(site=self.site_atual)
    for init_estrutura in init_estruturas:

      #Buscando as noticias
      if init_estrutura.caminho is None:
        lista_noticias = conteudo_site.findAll(str(init_estrutura.tag))
      else:
        lista_noticias = conteudo_site.findAll(str(init_estrutura.tag), attrs={str(init_estrutura.caminho)})

      #Buscando as estruturas de noticias (titulo, descricao) da lista de noticia
      lista_estruturas = EstruturaNoticia.objects.filter(inicio_estrutura_noticia=init_estrutura)
      if len(lista_noticias) == 0 or lista_noticias is None:
        return False

      for noticia in lista_noticias:

        #Objeto que reterá os dados da noticia
        noticia_obj = NoticiaColeta(
          id_coleta=self.id_coleta, projeto=self.projeto, 
          site=self.site_atual, init_estrutura=init_estrutura,
          palavra_chave = self.palavra_chave_atual
        )

        #Com a noticia encontrada, puxar os dados de titulo, decricao, url, imagem para salvar
        for lst_estrutura in lista_estruturas:
          self.processar_noticia(noticia_obj, noticia, lst_estrutura)

        if noticia_obj.noticia.titulo == '' or noticia_obj.noticia.titulo is None:
          continue

        #Acessando a pagina da noticia
        if noticia_obj.noticia.url != "" and self.site_atual.acessar_pagina_interna == 'S':
          try:
            article = Article(noticia_obj.noticia.url, language="pt")
            article.download()
            article.parse()
            noticia_obj.noticia.conteudo = article.text
            if article.publish_date is not None or article.publish_date != "" and noticia_obj.noticia.data_formatada is None:
              noticia_obj.noticia.data_formatada = article.publish_date

            if noticia_obj.noticia.descricao is None or noticia_obj.noticia.descricao == '':
              noticia_obj.noticia.descricao = article.summary

            if noticia_obj.salvou_imagem is False:
              noticia_obj.salvar_imagem(article.top_image)
          except:
            pass
            #Não faça nada

        #Caso a imagem não tenha sido salva, apenas registre a situação e continue
        if noticia_obj.salvou_imagem is False and (noticia_obj.noticia.imagem is not None and noticia_obj.noticia.imagem != ""):
          self.registrar_erro('Erro da imagem: {}'.format(noticia_obj.erro_imagem), noticia_obj.noticia.titulo)
        
        noticia_obj.salvar_noticia()
    return True

  def paginacao_elemento_html(self):
    temp_site_url = self.site_atual.url.format(palavra_chave = self.palavra_chave_atual.palavra_chave)
    json_args = json.loads(self.site_atual.json_args)
    marcador_final = json_args["marcador_final"]

    paginacao = 1
    while True:
      #Requisitando o html do site
      response = requests.get(str(temp_site_url), headers={"User-Agent": "XY"})

      #Verificando se o site não respondeu a requisição corretamente
      if int(response.status_code) in range(400,599):
        raise requests.exceptions.RequestException
      
      #Convertando o html para objeto manipulavel
      conteudo_site = BeautifulSoup(response.content, 'html.parser')
      if self.coletar_noticias_site(conteudo_site) is False:
        if paginacao == 1:
          print("NOTICIAS NAO ENCONTRADAS", self.site_atual.nome)
          self.registrar_erro('Site sem notícias')
          break
        else:
          break

      #Pegando a proxima url baseado na paginação
      tag_paginacao = conteudo_site.findAll(json_args['tag'], json_args['attr'])
      if len(tag_paginacao) == 0:
        self.registrar_erro('Erro na paginação, loop: ' + str(paginacao))
        break

      if json_args['subtag'] != "":
        tag_paginacao_subtag = tag_paginacao[-1].findAll(json_args['subtag'], json_args['subtag_attr'])
        if len(tag_paginacao_subtag) == 0 or (len(tag_paginacao) == 1 and paginacao > 1 and marcador_final == 'tag') or (len(tag_paginacao_subtag) == 1 and paginacao > 1 and marcador_final == 'subtag'):
          break
        else:
          temp_site_url = tag_paginacao_subtag[-1]['href']
      else:
        temp_site_url = tag_paginacao[-1]['href']

      paginacao = paginacao + 1

  def paginacao_url(self):
    paginacao = 1

    while True:
      #print(paginacao)
      temp_site_url = self.site_atual.url.format(
        palavra_chave = self.palavra_chave_atual.palavra_chave, pagina = paginacao
      )
      
      #Requisitando o html do site
      response = requests.get(str(temp_site_url), headers={"User-Agent": "XY"})

      #Verificando se o site não respondeu a requisição corretamente
      if int(response.status_code) in range(400,599):
        if paginacao > 1:
          break
        else:
          raise requests.exceptions.RequestException
      
      #Convertando o html para objeto manipulavel
      conteudo_site = BeautifulSoup(response.content, 'html.parser')
      if self.coletar_noticias_site(conteudo_site) is False:
        if paginacao == 1:
          print("NOTICIAS NAO ENCONTRADAS", self.site_atual.nome)
          self.registrar_erro('Site sem notícias')
          break
        else:
          break
      paginacao = paginacao + 1

  def paginacao_url_backend(self):
    paginacao = 1
    temp_site_url = self.site_atual.url
    
    #Substituindo o termo {palavra_chave} na url generica do site pela palavra chave do projeto atual
    if (self.site_atual.json_args == '' or self.site_atual.json_args is None):
      return

    json_args = json.loads(self.site_atual.json_args)
    json_args[json_args["parametro_query"]] = self.palavra_chave_atual.palavra_chave
    if "page" in json_args:
      paginacao = int(json_args["page"])

    while True:
      if json_args["tipo"] == "POST":
        json_args[json_args["parametro_pagina"]] = paginacao
        response = requests.post(str(temp_site_url), data=json_args, headers={"User-Agent": "XY"})
      else:
        print("APENAS TIPO POST VIA URL BACKEND")
        raise requests.exceptions.RequestException

      if int(response.status_code) in range(400,599) and paginacao > 1:
        break
      elif int(response.status_code) in range(400,599) and paginacao == 1:
        raise requests.exceptions.RequestException
      
      html_raw = response.content
      resp_json = self.converter_json(response.content) 

      if resp_json is False and paginacao == 1:
        raise requests.exceptions.RequestException

      if self.site_atual.req_response != "" and self.site_atual.req_response not in resp_json:
        break
      else:
        html_raw = resp_json[self.site_atual.req_response]

      conteudo_site = BeautifulSoup(html_raw, 'html.parser')
      if self.coletar_noticias_site(conteudo_site) is False:
        if paginacao == 1:
          raise requests.exceptions.RequestException
        else:
          break

      paginacao = paginacao + 1

  def sem_paginacao(self):
    temp_site_url = self.site_atual.url.format(palavra_chave = self.palavra_chave_atual)
    response = requests.get(str(temp_site_url), headers={"User-Agent": "XY"})

    #Verificando se o site não respondeu a requisição corretamente
    if int(response.status_code) in range(400,599):
      raise requests.exceptions.RequestException
    
    #Convertando o html para objeto manipulavel
    conteudo_site = BeautifulSoup(response.content, 'html.parser')
    self.coletar_noticias_site(conteudo_site)

  def executar(self):
    resultado = True
    #Resgatando os sites vinculados ao projeto 
    sites = self.projeto.sites.all()

    #Resgatando as palavras_chaves vinculadas ao projeto (caso uma tenha sido fornecida, utilizar apenas ela)
    if self.palavra_chave_user is None:
      palavras_chaves = self.projeto.palavras_chaves.all()
    else:
      palavras_chaves = [self.palavra_chave_user]
   
    for site in sites:
      self.site_atual = site

      for palavra_chave in palavras_chaves:
        self.palavra_chave_atual = palavra_chave

        try:
          print("Coletando: " + self.site_atual.nome + " | " + palavra_chave.palavra_chave)

          if site.tipo_paginacao == 'elemento_html':
            self.paginacao_elemento_html()
          elif site.tipo_paginacao == 'url_backend':
            self.paginacao_url_backend()
          elif site.tipo_paginacao == 'url':
            self.paginacao_url()
          else:
            self.sem_paginacao()
        except requests.exceptions.RequestException as e:
          resultado = False
          self.registrar_erro('Erro no requesição da lista de noticias')
      
    self.deletar_pasta_imagens_vazias()
    return resultado

class NoticiaColeta:
  noticia = None
  palavra_chave = None
  salvou_imagem = False
  erro_imagem = ''

  lista_meses = {}
  
  def __init__(self, *args, **kwargs):
    self.noticia = ConteudoNoticia()
    self.noticia.id_coleta = kwargs['id_coleta']
    self.noticia.projeto = kwargs['projeto']
    self.palavra_chave = kwargs['palavra_chave']
    self.noticia.site = kwargs['site']
    self.noticia.inicio_estrutura_noticia = kwargs['init_estrutura']
  
  def formatar_datas(self):
    data_formatada = str(self.noticia.data_formatada).lower()
    try:
      if '-' in data_formatada:
        temp = data_formatada.split(' ')[0].split('-')
        self.noticia.dia = temp[2]
        self.noticia.mes = temp[1]
        self.noticia.ano = temp[0]
      elif '/' in data_formatada:
        temp = data_formatada.split(' ')[0].split('/')
        self.noticia.dia = temp[0]
        self.noticia.mes = temp[1]
        self.noticia.ano = temp[2]
      elif '.' in data_formatada:
        temp = data_formatada.split(' ')[0].split('.')
        self.noticia.dia = temp[0]
        self.noticia.mes = self.lista_meses.index(temp[1])
        self.noticia.ano = temp[2]
    except Exception as e:
      pass

  def salvar_noticia(self):
    self.formatar_datas()
    """
      As regras abaixo só valem para as notícias do mesmo site e projeto que possuam o mesmo título.
      1. Caso a notícia não exista, o programa irá salva-la normalmente
      2. Se a notícia exister, verificar se a palavra-chave atual ja foi usada, caso sim, não salvar
      3. Se for uma nova palavra-chave e a notícia ja existir, apenas inserir na tabela um registro na tabela de palavras-chaves com noticia
      4. Caso a notícia exista, em ambos os casos 2 e 3, a imagem salvada na pasta local será deletada da execução atual
    """
    filtros = {"titulo": self.noticia.titulo, "site": self.noticia.site, "projeto": self.noticia.projeto}
    noticia = ConteudoNoticia.objects.filter(**filtros)
    if len(noticia) == 0:
      #noticia não existe, salvar os dados e palavra-chave
      self.noticia.save()
      self.noticia.palavras_chaves.add(self.palavra_chave)
    else:
      #noticia ja existe, verificar se a palavra-chave ja existe
      filtros['palavras_chaves__in'] = [self.palavra_chave]
      if (len(ConteudoNoticia.objects.filter(**filtros)) == 0):
        #nova palavra-chave, inserir o vinculo da palavra-chave com a noticia existente
        noticia[0].palavras_chaves.add(self.palavra_chave)
  
  def salvar_imagem(self, imagem):
    pasta = os.path.join(pathlib.Path().resolve(), "imagens_coletor", str(self.noticia.id_coleta))
    if not os.path.exists(pasta):
      os.makedirs(pasta)

    caminho_img = os.path.join(pasta, str(random.randint(0, 10)) + uuid.uuid4().hex + '.jpg')

    try:
      if type(imagem) is str:
        self.noticia.imagem = imagem
      else:
        self.noticia.imagem = imagem.get("src") or imagem.get("data-src")

      if self.noticia.imagem.startswith('//'):
        self.noticia.imagem = 'https:' + self.imagem

      img_data = requests.get(self.noticia.imagem, headers={"User-Agent": "XY"}).content

      with open(caminho_img, 'wb') as handler:
        handler.write(img_data)

      self.noticia.caminho_img_local = caminho_img
      self.salvou_imagem = True
    except Exception as err:
      if os.path.exists(caminho_img):
        os.remove(caminho_img)
      self.noticia.imagem = ''
      self.noticia.caminho_img_local = ''
      self.erro_imagem = err
      self.salvou_imagem = False

  def deletar_imagem(self):
    if self.noticia.caminho_img_local is not None and self.noticia.caminho_img_local != "":
     if os.path.exists(self.caminho_img_local):
        os.remove(self.caminho_img_local)

