# -*- coding: utf-8 -*-
import os
import pathlib
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import environ

import mysql.connector
from mysql.connector import errorcode
import calendar
import time

from newspaper import Article

from . import defines
from . import noticia as Noticia

#Execução via CMD
#import defines
#from classes.noticia import Noticia

env = environ.Env()
environ.Env.read_env(os.path.join(pathlib.Path().resolve(), '.env'))

class Coleta:
  projeto_id = None
  conn = None
  cursor = None
  id_coleta = calendar.timegm(time.gmtime())
  palavra_chave_user = 0
  db_config = {
    'database': env('DB'),
    'user': env('DB_USER'),
    'password': env('DB_PASS'),
    'host': env('DB_HOST'),
    'port': env('DB_PORT'),
    'charset': 'utf8mb4'
  }

  def __init__(self, projeto_id, palavra_chave_user):
    self.projeto_id = projeto_id
    self.palavra_chave_user = palavra_chave_user

  def conexao_bd(self):
    config_db = self.db_config

    try:
      conn = mysql.connector.connect(**config_db)
      return conn
    except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Conexão não realizada.")
      elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Base de dados não encontrada.")
      else:
        print(err)
    return None

  def deletar_pasta_imagens_vazias(self):
    #os.path.join(pathlib.Path().resolve(), "imagens", str(self.id_coleta))
    p_imagens = os.path.join(pathlib.Path().resolve(), "imagens_coletor")
    for pasta in os.listdir(p_imagens):
      if len(os.listdir(os.path.join(p_imagens, pasta))) == 0:
        os.rmdir(os.path.join(p_imagens, pasta))

  def registrar_erro(self, site_id = None, projeto_id = None, url = '', palavra_chave = None,  erro = '', titulo = '', conteudo_noticia_id = None):
    sql = (defines.INSERE_LOG_SQL)
    args = (str(self.id_coleta), projeto_id, site_id, str(url), palavra_chave, str(erro), str(titulo), conteudo_noticia_id)
    self.cursor.execute(sql, args)
    self.conn.commit()

  def salvar_noticia(self, noticia_obj):    
    args = noticia_obj.retornar_args()
    self.cursor.execute((defines.INSERE_NOTICIA_SQL), args)
    self.conn.commit()

    noticia_obj.id = self.cursor.lastrowid

  def inserir_palavra_chave_noticia(self, noticia_id, palavra_chave_id):
    self.cursor.execute((defines.INSERE_NOTICIA_PALAVRA_CHAVE_SQL), (palavra_chave_id, noticia_id))
    self.conn.commit()

  def noticia_existe(self, titulo, site_id, projeto_id, palavra_chave_id): 
    args = (palavra_chave_id, str(site_id), str(titulo), str(projeto_id))
    self.cursor.execute((defines.VERIFICAR_NOTICIA_EXISTE), args)
    return self.cursor.fetchall()

  def processar_noticia(self, noticia_obj, noticia, estrutura):
    campo = str(estrutura[1]).lower()
    possui_caminho = str(estrutura[3]) == '' or estrutura[3] is None

    dado_coletado = None
    if (possui_caminho):
      dado_coletado = noticia.find(str(estrutura[2]))
    else:
      dado_coletado = noticia.find(str(estrutura[2]), attrs={str(estrutura[3])})

    if dado_coletado is not None and estrutura[4] != '' and estrutura[4] is not None:
      if (str(estrutura[5]) == '' or estrutura[5] is None):
        dado_coletado = dado_coletado.find(str(estrutura[4]))
      else:
        dado_coletado = dado_coletado.find(str(estrutura[4]), attrs={str(estrutura[5])})

    if(campo == 'titulo'):
      if dado_coletado is not None:
        noticia_obj.titulo = dado_coletado.text.strip()
    elif(campo == 'url'):
      if dado_coletado is not None:
        noticia_obj.url = dado_coletado['href']
    elif(campo == 'data_formatada'):
      if dado_coletado is not None:
        noticia_obj.data_formatada = dado_coletado.text.strip() 
    elif(campo == 'descricao'):
      if dado_coletado is not None:
        noticia_obj.descricao = dado_coletado.text.strip()
    elif(campo == 'dia'):
      if dado_coletado is not None:
        noticia_obj.dia = dado_coletado.text.strip()
    elif(campo == 'mes'):
      if dado_coletado is not None:
        noticia_obj.mes = dado_coletado.text.strip()
    elif(campo == 'ano'):
      if dado_coletado is not None:
        noticia_obj.ano = dado_coletado.text.strip()
    elif(campo == 'localizacao'):
      if dado_coletado is not None:
        noticia_obj.localizacao = dado_coletado.text.strip()
    elif(campo == 'imagem'):
      if(dado_coletado):
        noticia_obj.salvar_imagem(dado_coletado)

  def coletar_noticias_site(self, site_id, conteudo_site, projeto_id, acessar_pagina_interna, palavra_chave_id):
    #Pegando a estrutura inicial
    self.cursor.execute((defines.INICIO_ESTRUTURA_SQL), (site_id,))
    inicio_estruturas = self.cursor.fetchall()

    for init_estrutura in inicio_estruturas:
      init_estrutura_id = init_estrutura[0]
      init_estrutura_tag = init_estrutura[1]
      init_estrutura_caminho = init_estrutura[2]

      if init_estrutura_caminho is None:
        lista_noticias = conteudo_site.findAll(str(init_estrutura_tag))
      else:
        lista_noticias = conteudo_site.findAll(str(init_estrutura_tag), attrs={str(init_estrutura_caminho)})
 
      for noticia in lista_noticias:
        #Buscando as estruturas (campos) da noticia da lista de noticias
        sql = (defines.ESTRUTURAS_SQL)
        self.cursor.execute(sql, (init_estrutura_id, 'lista'))
        lista_estruturas = self.cursor.fetchall()

        #Buscando as estruturas (campos) da página de noticias
        sql = (defines.ESTRUTURAS_SQL)
        self.cursor.execute(sql, (init_estrutura_id, 'pagina'))
        lista_estruturas_pagina = self.cursor.fetchall()

        #Objeto que reterá os dados da noticia
        noticia_obj = Noticia.Noticia()
        noticia_obj.estrutura_noticia_id = init_estrutura_id
        noticia_obj.pagjornal_id = site_id
        noticia_obj.id_coleta = self.id_coleta
        noticia_obj.projeto_id = projeto_id

        #Pegando os dados da noticia na sua forma externa (pagina de lista de noticias)
        for lst_estrutura in lista_estruturas:
          self.processar_noticia(noticia_obj, noticia, lst_estrutura)

        #Acessando a pagina da noticia
        if noticia_obj.url != "" and acessar_pagina_interna == 'S':
          try:
            article = Article(noticia_obj.url)
            article.download()
            article.parse()
            noticia_obj.conteudo = article.text
            if article.publish_date is not None or article.publish_date != "":
              noticia_obj.data_formatada = article.publish_date

            if noticia_obj.salvou_imagem is False:
              noticia_obj.salvar_imagem(article.top_image)
          except:
            pass
            #Não faça nada

        #Caso a imagem não tenha sido salva, apenas registre a situação e continue
        if noticia_obj.salvou_imagem is False and (noticia_obj.imagem is not None and noticia_obj.imagem != ""):
          self.registrar_erro(site_id = site_id, projeto_id = projeto_id, 
                              erro = 'Erro da imagem: {}'.format(noticia_obj.erro_imagem), 
                              titulo = noticia_obj.titulo, conteudo_noticia_id = noticia_obj.id)

        """
          As regras abaixo só valem para as notícias do mesmo site, do mesmo projeto que possuam o mesmo título.
          1. Caso a notícia não exista, o programa irá salva-la normalmente
          2. Se a notícia exister, verificar se a palavra-chave atual ja foi usada, caso sim, não salvar novamente
          3. Se for uma nova palavra-chave e a notícia ja existir, apenas inserir na tabela um registro na tabela de palavras-chaves com noticia
          4. Caso a notícia exista, em ambos os casos 2 e 3, a imagem salvada na pasta local deve ser deletada da execução atual
        """
        noticia_bd = self.noticia_existe(noticia_obj.titulo, site_id, projeto_id, palavra_chave_id)

        if len(noticia_bd) == 0:
          self.salvar_noticia(noticia_obj)
          self.inserir_palavra_chave_noticia(noticia_obj.id, palavra_chave_id)
        else:
          noticia_obj.deletar_imagem()

          #Caso seja uma nova palavra-chave
          if noticia_bd[0][2] == 'N':
            self.inserir_palavra_chave_noticia(noticia_bd[0][0], palavra_chave_id)

  def converter_json(self, json_string):
    try:
      return json.loads(json_string)
    except ValueError as e:
      return False

  def paginacao_elemento_html(self, site_id, site_url, projeto_id, acessar_pagina_interna, palavra_chave, json_args_string, palavra_chave_id): 
    temp_site_url = site_url.format(palavra_chave = palavra_chave)
    json_args = json.loads(json_args_string)
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
      self.coletar_noticias_site(site_id, conteudo_site, projeto_id, acessar_pagina_interna, palavra_chave_id)

      #Pegando a proxima url baseado na paginação
      tag_paginacao = conteudo_site.findAll(json_args['tag'], json_args['attr'])
      if len(tag_paginacao) == 0:
        self.registrar_erro(site_id, projeto_id, temp_site_url, palavra_chave_id, 'Erro na paginação, loop: ' + str(paginacao))
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
  
  def paginacao_url_backend(self, site_id, site_url, projeto_id, acessar_pagina_interna, palavra_chave, json_args_string, req_response, palavra_chave_id):
    paginacao = 1
    temp_site_url = site_url
    
    #Substituindo o termo {palavra_chave} na url generica do site pela palavra chave do projeto atual
    json_args = json.loads(json_args_string)
    json_args[json_args["parametro_query"]] = palavra_chave
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

      if req_response != "" and req_response not in resp_json:
        break
      else:
        html_raw = resp_json[req_response]

      conteudo_site = BeautifulSoup(html_raw, 'html.parser')
      self.coletar_noticias_site(site_id, conteudo_site, projeto_id, acessar_pagina_interna, palavra_chave_id)

      paginacao = paginacao + 1

  def sem_paginacao(self, site_id, site_url, palavra_chave, projeto_id, acessar_pagina_interna, palavra_chave_id):
    temp_site_url = site_url.format(palavra_chave = palavra_chave)
    response = requests.get(str(temp_site_url), headers={"User-Agent": "XY"})

    #Verificando se o site não respondeu a requisição corretamente
    if int(response.status_code) in range(400,599):
      raise requests.exceptions.RequestException
    
    #Convertando o html para objeto manipulavel
    conteudo_site = BeautifulSoup(response.content, 'html.parser')
    self.coletar_noticias_site(site_id, conteudo_site, projeto_id, acessar_pagina_interna, palavra_chave_id)

  def paginacao_url(self, site_id, site_url, projeto_id, acessar_pagina_interna, palavra_chave, palavra_chave_id):
    paginacao = 1

    print('PAGINANDO URL', site_id)
    while True:
      temp_site_url = site_url.format(palavra_chave = palavra_chave, pagina = paginacao)
      
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
      self.coletar_noticias_site(site_id, conteudo_site, projeto_id, acessar_pagina_interna, palavra_chave_id)
      paginacao = paginacao + 1

  def executar(self):
    #Iniciando a conexão
    self.conn = self.conexao_bd()
    if self.conn is None:
      print('Conexão não detectada')
      return False

    self.cursor = self.conn.cursor()

    #Buscando os sites de noticias
    self.cursor.execute((defines.SITES_SQL), (self.projeto_id, self.palavra_chave_user, self.palavra_chave_user))
    sites = self.cursor.fetchall()
  
    for site in sites:
      site_id = site[0]
      site_url = site[1]
      palavra_chave = site[2]
      acessar_pagina_interna = site[4]
      tipo_paginacao = site[5]
      json_args_string = site[6]
      req_response = site[7]
      palavra_chave_id = site[8]
      
      if tipo_paginacao == 'url' or tipo_paginacao == 'url_backend':
        temp_site_url = site_url
      else: 
        temp_site_url = site_url.format(palavra_chave = palavra_chave)

      try:
        if tipo_paginacao == 'elemento_html':
          self.paginacao_elemento_html(site_id, site_url, self.projeto_id, acessar_pagina_interna, palavra_chave, json_args_string, palavra_chave_id)
        elif tipo_paginacao == 'url_backend':
          self.paginacao_url_backend(site_id, site_url, self.projeto_id, acessar_pagina_interna, palavra_chave, json_args_string, req_response, palavra_chave_id)
        elif tipo_paginacao == 'url':
          self.paginacao_url(site_id, site_url, self.projeto_id, acessar_pagina_interna, palavra_chave, palavra_chave_id)
        else:
          self.sem_paginacao(site_id, site_url, palavra_chave, self.projeto_id, acessar_pagina_interna, palavra_chave_id)
          
      except requests.exceptions.RequestException as e:
        self.registrar_erro(site_id, self.projeto_id, temp_site_url, palavra_chave_id, 'Erro no requesição da lista de noticias')
      finally:
        self.conn.commit()

    #Fechando a conexão
    self.cursor.close()
    self.conn.close()

    #Deletando pastas vazias (sem imagens)
    self.deletar_pasta_imagens_vazias()