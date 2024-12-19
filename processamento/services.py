#Importações python
from datetime import datetime
import decimal
import json
import csv
import os
import time
import numpy as np
import math
import base64
from io import BytesIO

#Importações libs
import matplotlib
import seaborn as sns
import pandas as pd
import spacy
from spacy_wordnet.wordnet_annotator import WordnetAnnotator 

import nlpaug.augmenter.word as naw
from sklearn.feature_extraction.text import TfidfVectorizer,TfidfTransformer,CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, mean_squared_error
from imblearn.over_sampling import RandomOverSampler, SMOTE, ADASYN
from sklearn.metrics.pairwise import cosine_similarity
from scipy import sparse
import nltk


#Importações django 
from django.conf import settings
from django.db.models import Q, Avg
from django.db import transaction

#Importações apps
from coleta.models import (Projeto, ConteudoNoticia)
from coleta.traducoes import traduzir
from .models import *

#Separado por projeto
ROTULOS_NOTICIAS = {}

class Temporizador:
  def __init__(self):
    self.t_ini = datetime.now()

  def finalizar(self):
    t_fim = datetime.now()
    diff = t_fim - self.t_ini

    return {
      "inicio": self.t_ini.strftime("%H:%M:%S"),
      "fim": t_fim.strftime("%H:%M:%S"),
      "diff_segundos": diff.total_seconds(),
      "diff_minutos": diff.total_seconds() / 60
    }

class Classificador:

  def __init__(self):
    self.nlp_spacy = spacy.load('pt_core_news_lg')
    if 'spacy_wordnet' not in self.nlp_spacy.pipe_names:
      nltk.download('wordnet')
      nltk.download('omw')
      self.nlp_spacy.add_pipe("spacy_wordnet")
  
  def noneToStr(self, val):
    if val is None:
      return ''
    return val
  
  def limpar(self, texto):
    texto = texto.replace('\xa0','')
    texto = texto.replace('"',"'")
    texto = texto.replace("\n", " ")
    texto = texto.translate ({ord(c): "" for c in "!@#$%^&*()[]{};:,./<>?\|`“°ªº~=_+"})
    texto = texto.lower()
    return ''.join(texto.strip().lower().replace('"',"'").splitlines())

  def ajustar_texto(self, frase):
    #Removendo quebra de linhas
    frase = self.limpar(frase)
    doc = self.nlp_spacy(frase)

    filtrado = []
    for token in doc:
      if not token.is_stop and token.text.strip() not in ["","'",'"'] and not token.text.isnumeric():
        filtrado.append(token.lemma_)

    return ' '.join(filtrado)

  def executar_classificacao_modelos(self, dados_teste):
    #Adicionando dados

    # Criar um DataFrame a partir dos dados
    df = pd.DataFrame(dados_teste)

    # Vetorização usando TF-IDF
    tfidf_vectorizer = TfidfVectorizer(max_df=0.8, min_df=0.1)
    tfidf_matrix = tfidf_vectorizer.fit_transform(df['texto'])

    # Tratamento de palavras raras ou frequentes
    vocab = tfidf_vectorizer.get_feature_names_out()
    df_tfidf = pd.DataFrame(tfidf_matrix.toarray(), columns=vocab)

    # Tratamento de dados ausentes (usando substituição por zero como exemplo)
    df_tfidf.fillna(0, inplace=True)

    # Codificação de rótulos
    label_encoder = LabelEncoder()
    df['encoded_label'] = label_encoder.fit_transform(df['label'])

    # Divisão em treino, validação e teste (60%, 30%, 10%)
    X_train, X_temp, y_train, y_temp = train_test_split(df_tfidf, df['encoded_label'], test_size=0.4, random_state=42)
    X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.25, random_state=42)

    # Criando uma instância do oversampler (SMOTE)
    # Aplicando SMOTE aos dados de treinamento
    oversampler_smote = SMOTE(random_state=42)
    X_resampled, y_resampled = oversampler_smote.fit_resample(X_train, y_train)

    # Balanceamento de classes usando RandomOverSampler
    #oversampler = RandomOverSampler(random_state=42)
    #X_resampled, y_resampled = oversampler.fit_resample(X_train, y_train)

    # Lista de modelos
    models = [
      ("Naive Bayes", MultinomialNB()),
      ("Random Forest", RandomForestClassifier()),
      ("MLP", MLPClassifier())
    ]

    resultados = []

    # Treinamento e avaliação dos modelos
    for name, model in models:
      model.fit(X_resampled, y_resampled)
      y_pred = model.predict(X_val)

      accuracy = accuracy_score(y_val, y_pred)
      precision = precision_score(y_val, y_pred)
      recall = recall_score(y_val, y_pred)
      f1 = f1_score(y_val, y_pred)

      res = {
        "modelo": name,
        "acuracia": f"{accuracy:.4f}",
        "precisao": f"{precision:.4f}",
        "recall": f"{recall:.4f}",
        "f1_score": f"{f1:.4f}"
      }

      matplotlib.use('agg')

      # Matriz de confusão
      cm = confusion_matrix(y_val, y_pred)
      fig = matplotlib.pyplot.figure(figsize=(8, 6))
      sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=label_encoder.classes_, yticklabels=label_encoder.classes_)
      matplotlib.pyplot.title(  f"{ traduzir('Matriz de Confusão - Modelo') } {name}")
      matplotlib.pyplot.xlabel(traduzir("Previsão"))
      matplotlib.pyplot.ylabel("Real")

      tmpfile = BytesIO()
      fig.savefig(tmpfile, format='png')
      encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')

      imagem = 'data:image/png;base64,{}'.format(encoded)
      res['imagem'] = imagem
      
      resultados.append(res)
    
    return resultados

  def executar_classificacao_modelos2(self, dados_treino, dados_teste):
     #Adicionando dados

    # Criar um DataFrame a partir dos dados
    df_treino = pd.DataFrame(dados_treino)
    df_teste = pd.DataFrame(dados_teste)

    # Vetorização usando TF-IDF
    tfidf_vectorizer = TfidfVectorizer(max_df=0.8, min_df=0.1)
    tfidf_matrix_treino = tfidf_vectorizer.fit_transform(df_treino['texto'])
    tfidf_matrix_teste = tfidf_vectorizer.transform(df_teste['texto'])

    # Tratamento de palavras raras ou frequentes
    vocab = tfidf_vectorizer.get_feature_names_out()
    df_tfidf_treino = pd.DataFrame(tfidf_matrix_treino.toarray(), columns=vocab)
    df_tfidf_teste = pd.DataFrame(tfidf_matrix_teste.toarray(), columns=vocab)

    # Tratamento de dados ausentes (usando substituição por zero como exemplo)
    #df_tfidf_treino.fillna(0, inplace=True)
    #df_tfidf_teste.fillna(0, inplace=True)

    # Codificação de rótulos
    label_encoder = LabelEncoder()
    df_treino['encoded_label'] = label_encoder.fit_transform(df_treino['label'])

    # Lista de modelos
    models = [
      ("Naive Bayes", MultinomialNB()),
      ("Random Forest", RandomForestClassifier()),
      ("MLP", MLPClassifier())
    ]

    resultados = {}
    modelos_nomes = []

    #Treinamento e avaliação dos modelos
    for name, model in models:
      model.fit(df_tfidf_treino, df_treino['label'])
      y_pred = model.predict(df_tfidf_teste)

      modelos_nomes.append(name)

      if name not in resultados:
        resultados[name] = []

      resultados[name] = y_pred

    return resultados, modelos_nomes

  def calcular_tfidf(self, dados_limpos, dados_reais_treino, dados_falsos_treino):

    #Preparando os dados
    dados_reais = {'texto': []}
    dados_nao_reais = {'texto': []}

    for dado in dados_reais_treino:
      dados_reais['texto'].append(dado)
    
    for dado in dados_falsos_treino:
      dados_nao_reais['texto'].append(dado)

    for dado in dados_limpos:
      dados_reais['texto'].append(dado)
      dados_nao_reais['texto'].append(dado)

    idx_ult_real = len(dados_reais_treino)
    idx_ult_nao_real = len(dados_falsos_treino)

    tf_idf = TfidfVectorizer()
    reais_tfidf = tf_idf.fit_transform(dados_reais['texto'])
    nao_reais_tfidf = tf_idf.fit_transform(dados_nao_reais['texto'])

    #Calculando o cosseno e pegando apenas os dados adicionais (demais noticias)
    reais = cosine_similarity(reais_tfidf)[idx_ult_real:]
    nao_reais = cosine_similarity(nao_reais_tfidf)[idx_ult_nao_real:]

    noticias_classificadas = []
    pontuacoes = []
    for i in range(len(dados_limpos)):
      real_coseno = 0
      nao_real_coseno = 0
      
      #para cada noticia buscar o cosseno calculado de cada noticia de referencia
      for r in reais[i][:idx_ult_real]:
        if r >= real_coseno:
          real_coseno = r

      for nr in nao_reais[i][:idx_ult_nao_real]:
        if nr >= nao_real_coseno:
          nao_real_coseno = nr
      
      pontuacoes.append({
        'real': real_coseno, 'nao_real': nao_real_coseno 
      })

      noticias_classificadas.append(
        1 if real_coseno > nao_real_coseno else 0
      )
    return noticias_classificadas, pontuacoes

class ProcessamentoSrv:
  projeto = None

  def __init__(self):
    self.temporizador = Temporizador()

  def deletar_noticia_processada(self, id):
    try:
      NoticiaProcessada.objects.get(pk=id).delete()
      return {"resultado": "Deletado"}, 200
    except Exception as e:
      return {"erro": str(e)}, 400

  def buscar_noticias(self, projeto_id, id_processamento, filtrar_noticias):
    def converter_para_json(noticias):
      dados = []
      for noticia in noticias:
        dados.append({"id": noticia.id, "titulo": noticia.titulo, 
                      "url": noticia.url, "site": noticia.site.nome})
      return dados
     
    try:
      self.projeto = Projeto.objects.get(pk=projeto_id)

      if filtrar_noticias == '':
        filtrar_noticias = []
      else:     
        filtrar_noticias = filtrar_noticias.split(',')

      #Buscando notícias do projeto para serem usadas de referencia
      cinco_melhores = []

      if id_processamento != '' and id_processamento is not None:
        noticias = ConteudoNoticia.objects.select_related().filter(
          ~Q(pk__in=filtrar_noticias),
          noticiareferenciaprocessamento__isnull=True,
          noticiaresultadoprocessamento__processamento__id_processamento=id_processamento,
          projeto=self.projeto
        ).distinct().order_by("?")[:10]

        excluir = [noticia.id for noticia in noticias]

        #Pegar 5 noticias com pontuacao mais alta e rotuladas como verdadeira
        melhores = ConteudoNoticia.objects.select_related().filter(
          ~Q(pk__in=filtrar_noticias + excluir), projeto=self.projeto,
          noticiaresultadoprocessamento__rotulo_calculado='REAL',
          noticiaresultadoprocessamento__processamento__id_processamento=id_processamento
        ).order_by("-noticiaresultadoprocessamento__pontuacao_real")
        
        #Filtrando as cinco melhores de maneira distinta
        filtradas = []
        for melhor in melhores:
          if melhor.id not in filtradas:
            cinco_melhores.append(melhor)
            filtradas.append(melhor.id)
          if len(filtradas) == 5:
            break
        
        n = 10 - len(filtradas)
        noticias = noticias[:n]
      else:
        noticias = ConteudoNoticia.objects.select_related().filter(
          ~Q(pk__in=filtrar_noticias), projeto=self.projeto
        ).order_by("?")[:10]

      dados = converter_para_json(noticias) + converter_para_json(cinco_melhores)
      return dados, 200
    except Exception as e:
      return {"erro": str(e)}, 400

  def carregar_historico(self, projeto_id, id_processamento):
    try:
      self.projeto = Projeto.objects.get(pk=projeto_id)

      if id_processamento is None:
        resultados = ResultadoProcessamento.objects.select_related().filter(projeto=self.projeto)
      else:
        resultados = ResultadoProcessamento.objects.select_related().filter(projeto=self.projeto,id_processamento=id_processamento)

      historico = []
      for resultado in resultados:
        dado = {
          'modelos_reais': [],
          'modelos_calculados': [],
          'noticias': [],
          'acuracia': resultado.acuracia,
          'precisao': resultado.precisao,
          'recall': resultado.recall,
          'f1_score': resultado.f1_score
        }

        modelos = ClassificacaoModelo.objects.filter(processamento=resultado)
        for modelo in modelos:
          dado['modelos_calculados'].append({
            'modelo': modelo.modelo,
            'acuracia': modelo.acuracia,
            'precisao': modelo.precisao,
            'recall': modelo.recall,
            'f1_score': modelo.f1_score,
            'vp': modelo.vp,
            'vn': modelo.vp,
            'fp': modelo.vp,
            'fn': modelo.fn,
          })

        modelos = ClassificacaoModelo.objects.filter(projeto=self.projeto)
        for modelo in modelos:
          dado['modelos_reais'].append({
            'modelo': modelo.modelo,
            'acuracia': modelo.acuracia,
            'precisao': modelo.precisao,
            'recall': modelo.recall,
            'f1_score': modelo.f1_score,
            'imagem': modelo.matriz_confusao
          })

        noticias_referencia = NoticiaReferenciaProcessamento.objects.select_related().filter(processamento=resultado)
        for ref in noticias_referencia:
          dado['noticias'].append({
            'id': ref.noticia.id, 'site': ref.noticia.site.nome, 'titulo': ref.noticia.titulo , 'tipo': ref.noticia_real
          })

        historico.append(dado)

      return historico, 200
    except Exception as e:
      return {'erro': str(e)}, 400

  def processar(self, post_data):
    def calcular_totais(rotulos_reais, rotulos_calculados):
      qtd_acertos = 0
      vp = 0 #Verdadeiro positivo
      vn = 0 #verdadeiro negativo
      fp = 0 #Falso positivo
      fn = 0 #Falso negativo
      for idx, r in enumerate(rotulos_reais):
        qtd_acertos += 1 if r == rotulos_calculados[idx] else 0
        
        vp += 1 if r == rotulos_calculados[idx] and r == 1 else 0
        vn += 1 if r == rotulos_calculados[idx] and r == 0 else 0

        fp += 1 if r == 0 and rotulos_calculados[idx] == 1 else 0
        fn += 1 if r == 1 and rotulos_calculados[idx] == 0 else 0

      acuracia = 0 if len(rotulos_reais) == 0 else round(qtd_acertos / len(rotulos_reais), n_decimais)
      precisao = 0 if (vp + fp) == 0 else round(vp / (vp + fp), n_decimais)
      recall   = 0 if (vp + fn) == 0 else round(vp / (vp + fn), n_decimais)
      f1_score = 0 if (precisao + recall) == 0 else round( 2 * ((precisao * recall) / (precisao + recall)) , n_decimais)

      return acuracia, precisao, recall, f1_score, vp, vn, fp, fn
    
    def gerar_id():
      return str(datetime.now().timestamp())
    
    resultados = {}
    
    rotulos_projeto = {}
    if str(self.projeto.id) in ROTULOS_NOTICIAS:
      rotulos_projeto = ROTULOS_NOTICIAS[str(self.projeto.id)]

    id_processamento = post_data.get('id_processamento', None)
    noticias_reais_id = post_data.get('noticias_reais', [])
    noticias_falsas_id = post_data.get('noticias_falsas', [])
    salvar_noticias = post_data.get('salvar_noticias', 'N') == 'S'
    n_decimais = 4

    if id_processamento == '' or id_processamento is None:
      id_processamento = gerar_id()
    
    resultados['id_processamento'] = id_processamento

    classificador = Classificador()

    #Buscando todas as noticias do projeto
    noticias = ConteudoNoticia.objects.select_related().filter(projeto=self.projeto)

  
    #Buscando as noticias de referencia
    noticias_reais_ref = ConteudoNoticia.objects.select_related().filter(projeto=self.projeto, pk__in=noticias_reais_id)

    #Buscando as noticias de referencia
    noticias_falsas_ref = ConteudoNoticia.objects.select_related().filter(projeto=self.projeto, pk__in=noticias_falsas_id)

    #Fazendo a limpeza da lista com todas as noticias, rotulando e pontuando------------------------------
    dados_limpos_todas_noticias = []
    dados_limpos_noticias_parciais = []
    rotulos_reais_noticias = []
    rotulos_indicados = {}
    classificacoes = []

    t1 = Temporizador()

    #Limpando o texto das noticias de referencias
    dados_reais_treino = []
    dados_falsos_treino = []

    for noticia in noticias_reais_ref:
      texto_limpo = classificador.ajustar_texto(
        noticia.titulo + ' ' + classificador.noneToStr(noticia.descricao) + ' ' + classificador.noneToStr(noticia.conteudo)
      )
      dados_reais_treino.append(texto_limpo)
      rotulos_indicados[str(noticia.id)] = 1
      
    for noticia in noticias_falsas_ref:
      texto_limpo = classificador.ajustar_texto(
        noticia.titulo + ' ' + classificador.noneToStr(noticia.descricao) + ' ' + classificador.noneToStr(noticia.conteudo)
      )
      dados_falsos_treino.append(texto_limpo)
      rotulos_indicados[str(noticia.id)] = 0

    usar_noticias_parciais = len(noticias) != len(rotulos_projeto)
    for idx, noticia in enumerate(noticias):
      texto_limpo = classificador.ajustar_texto(
        noticia.titulo + ' ' + classificador.noneToStr(noticia.descricao) + ' ' + classificador.noneToStr(noticia.conteudo)
      )

      rotulo = 'SEM RÓTULO'
      if str(noticia.id) in rotulos_projeto:
        rotulo = 'REAL' if rotulos_projeto[str(noticia.id)] else 'FALSA'
        rotulos_reais_noticias.append( 1 if rotulo == 'REAL' else 0 )
      elif str(noticia.id) in rotulos_indicados:
        rotulo = 'REAL' if rotulos_indicados[str(noticia.id)] else 'FALSA'
        rotulos_reais_noticias.append( 1 if rotulo == 'REAL' else 0 )

      if rotulo != 'SEM RÓTULO' and usar_noticias_parciais:
        dados_limpos_noticias_parciais.append(texto_limpo)
      
      dados_limpos_todas_noticias.append(texto_limpo)

      classificacoes.append({
        'id': noticia.id, 'titulo': noticia.titulo, 'site': noticia.site.nome, 'url': noticia.url,
        'rotulo': rotulo, 'classificacao': '', 'idx_noticias': idx, 'pontuacao': '', 'modelos': ''
      })
    
    print("Limpeza:", t1.finalizar())

    #Calculando a classificação via tf-idf

    t1 = Temporizador()
    rotulos_calculados, pontuacoes = classificador.calcular_tfidf(dados_limpos_todas_noticias, dados_reais_treino, dados_falsos_treino)
    print("Calculo:", t1.finalizar())

    #Calculando as métricas dos modelos com dados reais
    t1 = Temporizador()

    #Conferir se ja existe o resultado de aprendizado de maquina para este projeto com este numero de noticias
    if usar_noticias_parciais:
      dados_teste = {'texto': dados_limpos_noticias_parciais, 'label': rotulos_reais_noticias}
    else:
      dados_teste = {'texto': dados_limpos_todas_noticias, 'label': rotulos_reais_noticias}

    #modelos_metricas_reais = ClassificacaoModelo.objects.filter(projeto=self.projeto, qtd_noticias=len(noticias))
#
    #salvar_metricas_reais = False
    #if (len(modelos_metricas_reais) == 0):
    #  salvar_metricas_reais = True
    #  #Se não existir aprendizado de maquinas para este projeto com este numero de noticias então deve-se fazer um novo
    #  resultados['modelos_metricas_reais'] = classificador.executar_classificacao_modelos(dados_teste)
    #else:
    #  resultados['modelos_metricas_reais'] = []
    #  for m in modelos_metricas_reais:
    #    resultados['modelos_metricas_reais'].append({
    #    "modelo": m.modelo,
    #    "acuracia": f"{m.acuracia}",
    #    "precisao": f"{m.precisao}",
    #    "recall": f"{m.recall}",
    #    "f1_score": f"{m.f1_score}",
    #    "imagem": m.matriz_confusao
    #  })
    resultados['modelos_metricas_reais'] = []
  
    print("Modelos com rotulos reais:", t1.finalizar())

    t1 = Temporizador()
    dados_treino = {
      'texto': [t for t in dados_reais_treino] + [t for t in dados_falsos_treino],
      'label': [1 for i in range(len(dados_reais_treino))] + [0 for i in range(len(dados_falsos_treino))],
    }
    modelos_metricas_calculadas, modelos_nomes = classificador.executar_classificacao_modelos2(dados_treino, dados_teste)
    
    print("Modelos com noticias de treino:", t1.finalizar())

    print(rotulos_calculados)

    #Retornando o resultado de cada rotulo para cada noticia
    for idx, rotulo in enumerate(rotulos_calculados):
      classificacoes[idx]['pontuacao_real'] = round(pontuacoes[idx]['real'],n_decimais)
      classificacoes[idx]['pontuacao_nao_real'] = round(pontuacoes[idx]['nao_real'],n_decimais)
      classificacoes[idx]['classificacao'] = 'REAL' if rotulo == 1 else 'FALSA'

      modelos_string = ''
      for modelo in modelos_nomes:
        if modelo in modelos_metricas_calculadas:
          if idx in modelos_metricas_calculadas[modelo]:
            status = modelos_metricas_calculadas[modelo][idx]#'Real' if modelos_metricas_calculadas[modelo][idx] == 1 else 'Falsa'
            modelos_string = modelos_string + '{}: {}<br>'.format(modelo, status)
      classificacoes[idx]['classificadores'] = modelos_string

    print("---FIM enumerate(rotulos_calculados) ---")

    #Calculando % de similaridade entre rotulos reais e rotulos calculados
    #print("CALCULANDO METRICAS DE ROTULOS REAIS X CALCULADOS------------")
    acuracia, precisao, recall, f1_score, vp_calc, vn_calc, fp_calc, fn_calc = calcular_totais(rotulos_reais_noticias, rotulos_calculados)
    
    resultados['acuracia'] = str(acuracia)
    resultados['precisao'] = str(precisao)
    resultados['recall']   = str(recall)
    resultados['f1_score'] = str(f1_score)

    resultados['modelos_rotulos_calculados'] = []
    for modelo in modelos_metricas_calculadas:
      acuracia, precisao, recall, f1_score, vp, vn, fp, fn = calcular_totais(rotulos_reais_noticias, modelos_metricas_calculadas[modelo])

      resultados['modelos_rotulos_calculados'].append({
        "modelo": modelo,
        "acuracia": f"{acuracia:.4f}",
        "precisao": f"{precisao:.4f}",
        "recall": f"{recall:.4f}",
        "f1_score": f"{f1_score:.4f}",
        "vp": vp, "vn": vn, "fp": fp, "fn": fn
      })

    #Salvando os dados calculados
    #print("SALVANDO OS DADOS CALCULADOS------------")
    with transaction.atomic():
      obj_processamento = ResultadoProcessamento()
      obj_processamento.id_processamento = id_processamento
      obj_processamento.projeto = self.projeto
      obj_processamento.acuracia = acuracia
      obj_processamento.precisao = precisao
      obj_processamento.recall = recall
      obj_processamento.vp = vp_calc
      obj_processamento.vn = vn_calc
      obj_processamento.fp = fp_calc
      obj_processamento.fn = fn_calc
      obj_processamento.save()

      for idx, classificacao in enumerate(classificacoes):
        #Salvando as pontuacoes
        noticia = noticias[classificacao['idx_noticias']]
        
        obj_nt = NoticiaResultadoProcessamento()
        obj_nt.processamento = obj_processamento
        obj_nt.noticia = noticia
        obj_nt.rotulo_calculado = classificacao['classificacao']
        obj_nt.rotulo_real = classificacao['rotulo']
        obj_nt.classificadores = classificacao['classificadores'].replace('<br>', '\n')
        obj_nt.pontuacao_real = pontuacoes[idx]['real']
        obj_nt.pontuacao_nao_real = pontuacoes[idx]['nao_real']
        obj_nt.save()
      
        #Salvando as noticias como processadas
        if salvar_noticias:
          if classificacao['classificacao'] == 'REAL':
            noticia_processada = NoticiaProcessada.objects.filter(noticia=noticia).first()
            palavras_chaves = ''.join([p.palavra_chave for p in noticia.palavras_chaves.all()])
            if noticia_processada is None:
              #Adicionar noticia na base de noticias filtradas
              noticia_processada = NoticiaProcessada.objects.create(noticia=noticia, palavras_chaves=palavras_chaves)
            else:
              #Atualizar caso tenha uma nova palavra-chave
              noticia_processada.palavras_chaves = palavras_chaves
              noticia_processada.save(update_fields=['palavras_chaves'])

      for ref in noticias_reais_ref:
        obj1 = NoticiaReferenciaProcessamento()
        obj1.processamento = obj_processamento
        obj1.noticia = ref
        obj1.noticia_real = 'S'
        obj1.save()

      for ref in noticias_falsas_ref:
        obj2 = NoticiaReferenciaProcessamento()
        obj2.processamento = obj_processamento
        obj2.noticia = ref
        obj2.noticia_real = 'N'
        obj2.save()

      for modelo in resultados['modelos_rotulos_calculados']:
        obj_modelo = ClassificacaoModelo()
        obj_modelo.processamento = obj_processamento
        obj_modelo.modelo = modelo['modelo']
        obj_modelo.acuracia = modelo['acuracia']
        obj_modelo.precisao = modelo['precisao']
        obj_modelo.recall = modelo['recall']
        obj_modelo.f1_score = modelo['f1_score']
        obj_modelo.vp = modelo['vp']
        obj_modelo.vn = modelo['vn']
        obj_modelo.fp = modelo['fp']
        obj_modelo.fn = modelo['fn']
        obj_modelo.qtd_noticias = len(noticias)
        obj_modelo.save()

      #if salvar_metricas_reais:
      #  for modelo in resultados['modelos_metricas_reais']:
      #    obj_modelo = ClassificacaoModelo()
      #    obj_modelo.projeto = self.projeto
      #    obj_modelo.modelo = modelo['modelo']
      #    obj_modelo.acuracia = modelo['acuracia']
      #    obj_modelo.precisao = modelo['precisao']
      #    obj_modelo.recall = modelo['recall']
      #    obj_modelo.f1_score = modelo['f1_score']
      #    obj_modelo.qtd_noticias = len(noticias)
      #    obj_modelo.matriz_confusao = modelo['imagem']
      #    obj_modelo.save()

    return resultados, classificacoes

  def executar_processamento(self, projeto_id, body):
    try:
      self.projeto = Projeto.objects.get(pk=projeto_id)
      
      resultados, classificacoes = self.processar(json.loads(body))
 
      tempo = self.temporizador.finalizar()
      return {
        "resultados": resultados,
        "classificacoes": classificacoes,
        "tempo": tempo
      }, 200
    except Exception as e:
      return {"erro": str(e)}, 400
    
  def teste(self):
    noticias = ConteudoNoticia.objects.select_related().all()[:1000]
    grupo1 = []
    grupo2 = []
    grupo3 = []

    for noticia in noticias:
      grupo1.append({
        "titulo": noticia.titulo,
        "resumo": noticia.descricao
    })
      
      grupo2.append({
        "titulo": noticia.titulo,
        "corpo": noticia.conteudo
    })
      
      grupo3.append({
        "titulo": noticia.titulo,
        "resumo": noticia.descricao,
        "corpo": noticia.conteudo
    })

    print("Grupo 1: Título e Descricao")
    for noticia in grupo1[:5]:
        print(f"Título: {noticia['titulo']}")
        print(f"Resumo: {noticia['resumo'] or 'Resumo não disponível'}")
        print("-" * 50)
    
    print(len(noticias))
    
    print("\nGrupo 2: Título e Conteudo")
    for noticia in grupo2[:5]:
        print(f"Título: {noticia['titulo']}")
        print(f"Corpo: {noticia['corpo'] or 'Corpo não disponível'}")
        print("-" * 50)

    print("\nGrupo 3: Título, Descricao e Conteudo")
    for noticia in grupo3[:5]:
        print(f"Título: {noticia['titulo']}")
        print(f"Resumo: {noticia['resumo'] or 'Resumo não disponível'}")
        print(f"Corpo: {noticia['corpo'] or 'Corpo não disponível'}")
        print("-" * 50)
    
    return {"grupo1": grupo1, "grupo2": grupo2, "grupo3": grupo3}

class CsvSbertSrv():
  csv_f = None

  def salvar_csv(self, arr):
    csv_writer = csv.writer(self.csv_f, delimiter=';', quoting=csv.QUOTE_ALL)
    csv_writer.writerow(arr)

  def buscar_noticias(self):
    classificador = Classificador()
    noticias = ConteudoNoticia.objects.select_related().filter(projeto=self.projeto)
 
    nome_arquivo = f"sbert_{str(time.time()).replace('.','')}.csv"
    arquivo = os.path.join(settings.BASE_DIR, 'temp', nome_arquivo)
 
    self.csv_f = open(arquivo, 'w', encoding='UTF8', newline='')
    self.salvar_csv(['pontuacao', 'noticia_id', 'noticia_processada', 'noticia_texto', 'noticia_referencia_id', 'noticia_referencia_texto'])

    #Testando noticia com as noticicas de referencia 
    for noticia in noticias:
      texto = noticia.titulo + ' ' + classificador.noneToStr(noticia.descricao) + ' ' + classificador.noneToStr(noticia.conteudo)
      texto = ' '.join(texto.replace('\n', ' ').replace('"',"'").splitlines())

      if len(noticia.noticiaprocessada_set.all()) > 0:
        processada = 'SIM'
      else:
        processada = 'NÂO'

      for testada in noticia.noticia_testada.select_related().all():
        treino = testada.noticia_referencia
        texto_treino = treino.titulo + ' ' + classificador.noneToStr(treino.descricao) + ' ' + classificador.noneToStr(treino.conteudo)
        texto_treino = ' '.join(texto.replace('\n', ' ').replace('"',"'").splitlines())

        pontuacao = '{:.4f}'.format(testada.pontuacao)
        self.salvar_csv([pontuacao, noticia.id, processada, texto, treino.id, texto_treino])

      if len(noticia.noticia_testada.all()) == 0:
        self.salvar_csv(['', noticia.id, processada, texto, '', ''])

    self.csv_f.close()
    return nome_arquivo

  def gerar_csv(self, projeto_id):
    try:
      self.projeto = Projeto.objects.get(pk=projeto_id)
      caminho = self.buscar_noticias()
      
      return {"arquivo": caminho}, 200
    except Exception as e:
      return {"erro": str(e)}, 400