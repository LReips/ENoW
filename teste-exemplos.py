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
import sentence_transformers
import spacy
from spacy_wordnet.wordnet_annotator import WordnetAnnotator 

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, mean_squared_error
from imblearn.over_sampling import RandomOverSampler

class Classificador:

  def __init__(self):
    self.nlp_spacy = spacy.load('pt_core_news_lg')
    if 'spacy_wordnet' not in self.nlp_spacy.pipe_names:
      self.nlp_spacy.add_pipe("spacy_wordnet")
 
  def limpar(self, texto):
    texto = texto.replace('\xa0','')
    texto = texto.replace('"',"'")
    texto = texto.replace("\n", " ")
    texto = texto.translate ({ord(c): "" for c in "!@#$%^&*()[]{};:,./<>?\|`“°ªº~=_+"})
    texto = texto.lower()
    return ''.join(texto.strip().lower().replace('"',"'").splitlines())

  def ajustar_texto(self, frase):
    #Removendo quebra de linhas
    #frase = self.limpar(frase)
    doc = self.nlp_spacy(frase)

    filtrado = []
    for token in doc:
      if not token.is_stop and token.text.strip() not in ["","'",'"'] and not token.text.isnumeric():
        filtrado.append(token.lemma_)

    return ' '.join(filtrado)
  
  def executar_classificacao_modelos(self, dados, rodar_matplot = False):
    # Criar um DataFrame a partir dos dados
    df = pd.DataFrame(dados)

    # Vetorização usando TF-IDF
    tfidf_vectorizer = TfidfVectorizer(max_df=0.8, min_df=0.1)
    tfidf_matrix = tfidf_vectorizer.fit_transform(df['texto'])

    # Tratamento de palavras raras ou frequentes
    vocab = tfidf_vectorizer.get_feature_names_out()
    df_tfidf = pd.DataFrame(tfidf_matrix.toarray(), columns=vocab)

    return tfidf_matrix,vocab,df_tfidf

    # Tratamento de dados ausentes (usando substituição por zero como exemplo)
    df_tfidf.fillna(0, inplace=True)

    # Codificação de rótulos
    label_encoder = LabelEncoder()
    df['encoded_label'] = label_encoder.fit_transform(df['label'])

    # Divisão em treino, validação e teste (70%, 15%, 15%)
    X_train, X_temp, y_train, y_temp = train_test_split(df_tfidf, df['encoded_label'], test_size=0.3, random_state=42)
    X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

    # Balanceamento de classes usando RandomOverSampler
    oversampler = RandomOverSampler(random_state=42)
    X_resampled, y_resampled = oversampler.fit_resample(X_train, y_train)

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

      if rodar_matplot:
        matplotlib.use('agg')

        # Matriz de confusão
        cm = confusion_matrix(y_val, y_pred)
        fig = matplotlib.pyplot.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=label_encoder.classes_, yticklabels=label_encoder.classes_)
        matplotlib.pyplot.title(f"Matriz de Confusão - Modelo {name}")
        matplotlib.pyplot.xlabel("Previsão")
        matplotlib.pyplot.ylabel("Real")

        tmpfile = BytesIO()
        fig.savefig(tmpfile, format='png')
        encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')

        imagem = 'data:image/png;base64,{}'.format(encoded)
        res['imagem'] = imagem
        #plt.show()
      
      resultados.append(res)
    
    return resultados

  def entidades_nomeadas(self, texto):
    doc = self.nlp_spacy(texto)
    gpe = []
    for ent in doc.ents:
      if (ent.label_ == 'LOC'):
        if ent.text not in gpe:
          gpe.append(ent.text)
    return gpe
  

NOTICIA = """
  Caravelas-portuguesas assustam banhistas em SP; elas são perigosas 
  O surgimento de dezenas caravelas-portuguesas em praias da Baixada Santista e do litoral sul de São Paulo tem assustado banhistas. 
  Há relatos de aparecimento desses animais marinhos no Guarujá, Santos e Peruíbe. O surgimento da espécie é bem comum nesta época do ano e ocorre por causa da correnteza marítima.
  Créditos: Divulgação/PMS Caravelas-portuguesas assustam banhistas em SP; elas são perigosas e podem até matar 
  O contato com a caravela-portuguesa é altamente perigoso. Ela oferece grande risco, pois pode causar queimaduras de até 3º grau, devido aos seus tentáculos, que liberam uma substância extremamente urticante. A queimadura pode até causar uma parada cardiorrespiratória, levando a pessoa a morte, principalmente em crianças.
  Segundo o biólogo marinho Alex Ribeiro, coordenador do Aquário de Santos, cada caravela (Physalia physalis) é uma colônia de indivíduos, com tentáculos utilizados para capturar presas. “Eles soltam uma toxina paralisante, que continua ativa mesmo fora d’água. O aumento da incidência de acidentes está sempre associado ao verão”.
  Alex reforça que é fácil identificar uma caravela, uma vez que ela está sempre com sua bolsa de ar acima do nível d’água. “É essa bolsa que a conduz na direção dos ventos e correntes. Se a pessoa a vir, melhor não se aproximar”.
  A orientação é de que, ao avistar uma caravela-portuguesa na praia, não chegar perto. Se tiver contato involuntário com uma, no mar ou na areia, não coce ou esfregue o local, para não espalhar o veneno.
  E procure um médico imediatamente, pois como algumas pessoas são alérgicas às toxinas, podem sofrer um choque anafilático.
"""

classificador = Classificador()

print(NOTICIA,'\n')

texto_limpo = classificador.limpar(NOTICIA)

print(texto_limpo,'\n')

texto_ajustado = classificador.ajustar_texto(texto_limpo)

print(texto_ajustado,'\n')

nomeadas = classificador.entidades_nomeadas(NOTICIA)

print(nomeadas,'\n')

tfidf_matrix,vocab,df_tfidf = classificador.executar_classificacao_modelos({'texto': [NOTICIA, texto_ajustado]}, [1,1])
print(tfidf_matrix,'\n')
print(vocab,'\n')
print(df_tfidf,'\n')