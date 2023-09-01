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

import nlpaug.augmenter.word as naw
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
from imblearn.over_sampling import RandomOverSampler, SMOTE, ADASYN

#Importações django
from django.conf import settings
from django.db.models import Q, Avg
from django.db import transaction

#Importações apps
from coleta.models import (Projeto, ConteudoNoticia)
from .models import *

#Separado por projeto
ROTULOS_NOTICIAS = {
  '1': { '1':1, '2':0, '3':1, '4':0, '5':0, '6':0, '7':0, '8':0, '9':1, '10':0, '11':0, '12':0, '13':0, '14':0, '15':0, '16':0, '17':0, '18':1, '19':0, '20':0, '21':1, '22':1, '23':1, '24':1, '25':1, '26':1, '27':0, '28':0, '29':0, '30':0, '31':0, '32':0, '33':0, '34':0, '35':0, '36':0, '37':0, '38':0, '39':0, '40':0, '41':0, '42':0, '43':0, '44':0, '45':0, '46':0, '47':0, '48':0, '49':0, '50':0, '51':0, '52':0, '53':0, '54':0, '55':0, '56':0, '57':0, '58':0, '59':0, '60':0, '61':0, '62':0, '63':0, '64':0, '65':0, '66':1, '67':0, '68':0, '69':0, '70':0, '71':0, '72':0, '73':0, '74':0, '75':0, '76':0, '77':1, '78':0, '79':0, '80':1, '81':0, '82':0, '83':0, '84':0, '85':0, '86':0, '87':0, '88':1, '89':0, '90':1, '91':1, '92':1, '93':1, '94':1, '95':1, '96':1, '97':1, '98':0, '99':1, '100':1, '101':1, '102':1, '103':1, '104':1, '105':1, '106':1, '107':1, '108':1, '109':1, '110':1, '111':1, '112':1, '113':1, '114':1, '115':1, '116':1, '117':1, '118':1, '119':1, '120':1, '121':1, '122':1, '123':1, '124':1, '125':1, '126':0, '127':1, '128':1, '129':0, '130':0, '131':1, '132':0, '133':0, '134':1, '135':0, '136':0, '137':0, '138':0, '139':0, '140':0, '141':0, '142':0, '143':0, '144':0, '145':0, '146':0, '147':0, '148':0, '149':0, '150':0, '151':0, '152':0, '153':0, '154':0, '155':0, '156':0, '157':0, '158':0, '159':1, '160':1, '161':0, '162':0, '163':0, '164':0, '165':0, '166':0, '167':0, '168':0, '169':0, '170':0, '171':0, '172':0, '173':0, '174':0, '175':0, '176':0, '177':0, '178':0, '179':0, '180':0, '181':0, '182':0, '183':0, '184':0, '185':0, '186':0, '187':0, '188':0, '189':1, '190':0, '191':0, '192':0, '193':0, '194':1, '195':1, '196':0, '197':0, '198':1, '199':0, '200':1, '201':1, '202':1, '203':1, '204':0, '205':1, '206':1, '207':0, '208':0, '209':0, '210':0, '211':0, '212':0, '213':0, '214':0, '215':0, '216':0, '217':0, '218':0, '219':0, '220':0, '221':0, '222':1, '223':0, '224':0, '225':0, '226':0, '227':0, '228':0, '229':0, '230':0, '231':0, '232':0, '233':0, '234':0, '235':0, '236':0, '237':0, '238':0, '239':0, '240':0, '241':0, '242':0, '243':0, '244':0, '245':0, '246':0, '247':0, '248':0, '249':0, '250':0, '251':0, '252':0, '253':0, '254':0, '255':0, '256':0, '257':0, '258':0, '259':0, '260':0, '261':0, '262':0, '263':0, '264':0, '265':0, '266':0, '267':0, '268':0, '269':0, '270':0, '271':0, '272':0, '273':0, '274':0, '275':0, '276':0, '277':0, '278':0, '279':0, '280':0, '281':0, '282':0, '283':0, '284':0, '285':0, '286':0, '287':0, '288':0, '289':0, '290':0, '291':0, '292':0, '293':0, '294':0, '295':0, '296':0, '297':0, '298':0, '299':0, '300':0, '301':0, '302':0, '303':0, '304':0, '305':0, '306':0, '307':0, '308':1, '309':0, '310':1, '311':1, '312':0, '313':0, '314':0, '315':0, '316':0, '317':0, '318':0, '319':1, '320':0, '321':0, '322':0, '323':0, '324':0, '325':0, '326':0, '327':0, '328':1, '329':1, '330':0, '331':0, '332':0, '333':1, '334':0, '335':0, '336':0, '337':0, '338':0, '339':0, '340':0, '341':0, '342':0, '343':0, '344':0, '345':0, '346':0, '347':0, '348':0, '349':0, '350':0, '351':0, '352':0, '353':0, '354':0, '355':0, '356':0, '357':0, '358':0, '359':0, '360':0, '361':0, '362':0, '363':0, '364':0, '365':0, '366':0, '367':1, '368':0, '369':0, '370':0, '371':0, '372':0, '373':0, '374':0, '375':0, '376':0, '377':0, '378':0, '379':0, '380':0, '381':0, '382':0, '383':0, '384':0, '385':0, '386':0, '387':0, '388':0, '389':0, '390':0, '391':0, '392':0, '393':1, '394':0, '395':0, '396':0, '397':0, '398':0, '399':0, '400':0, '401':0, '402':0, '403':0, '404':0, '405':0, '406':0, '407':0, '408':0, '409':0, '410':0, '411':0, '412':0, '413':0, '414':0, '415':0, '416':0, '417':0, '418':0, '419':0, '420':0, '421':0, '422':0, '423':0, '424':0, '425':0, '426':0, '427':0, '428':0, '429':0, '430':0, '431':0, '432':0, '433':0, '434':0, '435':0, '436':0, '437':0, '438':0, '439':0, '440':0, '441':0, '442':0, '443':0, '444':0, '445':0, '446':1, '447':0, '448':0, '449':0, '450':0, '451':0, '452':0, '453':0, '454':0, '455':0, '456':0, '457':0, '458':0, '459':0, '460':0, '461':0, '462':0, '463':0, '464':0, '465':0, '466':0, '467':0, '468':0, '469':0, '470':0, '471':0, '472':0, '473':0, '474':0, '475':0, '476':0, '477':0, '478':0, '479':0, '480':0, '481':0, '482':0, '483':0, '484':0, '485':0, '486':0, '487':0, '488':0, '489':0, '490':0, '491':0, '492':0, '493':0, '494':0, '495':0, '496':0, '497':0, '498':0, '499':0, '500':0, '501':0, '502':0, '503':0, '504':0, '505':0, '506':0, '507':0, '508':0, '509':0, '510':0, '511':0, '512':0, '513':1, '514':1, '515':1, '516':0, '517':0, '518':1, '519':0, '520':0, '521':0, '522':0, '523':0, '524':0, '525':0, '526':0, '527':0, '528':1, '529':0, '530':0, '531':0, '532':0, '533':0, '534':0, '535':0, '536':0, '537':0, '538':0, '539':0, '540':0, '541':0, '542':0, '543':0, '544':0, '545':0, '546':0, '547':0, '548':0, '549':0, '550':0, '551':0, '552':0, '553':0, '554':0, '555':0, '556':0, '557':0, '558':0, '559':0, '560':0, '561':0, '562':0, '563':0, '564':0, '565':0, '566':0, '567':0, '568':0, '569':0, '570':0, '571':0, '572':0, '573':0, '574':0, '575':0, '576':0, '577':0, '578':0, '579':0, '580':0, '581':0, '582':0, '583':0, '584':0, '585':0, '586':0, '587':0, '588':0, '589':0, '590':0, '591':1, '592':0, '593':0, '594':0, '595':0, '596':0, '597':0, '598':1, '599':0, '600':0, '601':0, '602':0, '603':0, '604':0, '605':0, '606':0, '607':0, '608':0, '609':0, '610':0, '611':0, '612':0, '613':0, '614':0, '615':0, '616':0, '617':0, '618':0, '619':0, '620':0, '621':0, '622':1, '623':1 }
}

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
      self.nlp_spacy.add_pipe("spacy_wordnet")

    self.aug = naw.SynonymAug(aug_src='wordnet')
    self.minority_texts = [
      'Caravelas-Portuguesas Causam Preocupação no Litoral Brasileiro',
      'Um fenômeno surpreendente de caravelas-portuguesas tem causado preocupação nas praias do litoral brasileiro neste verão. O aumento significativo na presença desses cnidários peçonhentos levou a um aumento nos casos de ferimentos entre os banhistas.',
      'De acordo com relatórios do Corpo de Bombeiros, mais de 31 mil banhistas foram atendidos em postos salva-vidas apenas nos últimos 20 dias devido a queimaduras causadas pelas caravelas-portuguesas. A equipe de resgate considera essa temporada de verão "atípica" devido ao alto número de incidentes.',
      'As caravelas-portuguesas, conhecidas por sua cor arroxeada e uma crista bolhosa preenchida com ar, carregam toxinas potentes que causam dores intensas, queimaduras de terceiro grau e reações alérgicas em casos extremos. Embora a presença dessas criaturas marinhas tenha sido registrada em menor número em praias de Santa Catarina e do Paraná, seus efeitos têm sido preocupantes.',
      'Especialistas acreditam que esse aumento inesperado pode estar relacionado a um desequilíbrio ecológico ou a fatores como correntes marítimas, altas temperaturas e a redução de predadores naturais, como a pesca excessiva.',
      'Bandeiras lilás têm sido usadas em toda a costa para alertar os banhistas sobre a presença incomum de animais marinhos. A Sociedade Brasileira de Salvamento Aquático (Sobrasa) também emitiu diretrizes sobre como lidar com ferimentos causados por caravelas-portuguesas, incluindo a aplicação de ácido acético e a busca por atendimento médico em casos graves.',
      'Apesar do aumento de casos, especialistas e autoridades estão trabalhando para garantir a segurança dos banhistas e compreender melhor os fatores por trás desse fenômeno incomum.'
    ]

    self.synthetic_texts = [self.aug.augment(text) for text in self.minority_texts]
  
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
  
  def testar_sbert(self, texto1, texto2):
    model = sentence_transformers.SentenceTransformer('all-MiniLM-L6-v2')
    emb1 = model.encode(texto1)
    emb2 = model.encode(texto2)

    cos_sim = sentence_transformers.util.cos_sim(emb1, emb2)
    score = cos_sim[0][0]
    return decimal.Decimal('{:.4f}'.format(score))
  
  def executar_classificacao_modelos(self, dados, rodar_matplot = False):
    #Adicionando dados
    dados['texto'] = np.concatenate((self.minority_texts, dados['texto']))
    dados['label'] = np.concatenate(( [1] * len(self.minority_texts) , dados['label']))

    # Criar um DataFrame a partir dos dados
    df = pd.DataFrame(dados)

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

  def buscar_noticias(self, projeto_id):
    try:
      self.projeto = Projeto.objects.get(pk=projeto_id)

      def converter_para_json(noticias):
        dados = []
        for noticia in noticias:
          dados.append({"id": noticia.id, "titulo": noticia.titulo, 
                        "url": noticia.url, "site": noticia.site.nome})
        return dados

      #Buscando notícias do projeto que não foram gravadas como reais
      noticias = ConteudoNoticia.objects.select_related().filter(
        projeto=self.projeto
      ).order_by("id")
      
      dados = converter_para_json(noticias)
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
          'limiar': resultado.limiar,
          'margem': resultado.margem,
          'limiar_ajustado': resultado.limiar_ajustado,
          'acuracia': resultado.acuracia,
          'precisao': resultado.precisao,
          'recall': resultado.recall,
          'f1_score': resultado.f1_score,
          'modelos_reais': [],
          'modelos_calculados': [],
          'noticias': []
        }

        modelos = ClassificacaoModelo.objects.filter(processamento=resultado)
        for modelo in modelos:
          idx = 'modelos_reais'
          if modelo.tipo_metrica == 'CALCULADA':
            idx = 'modelos_calculados'

          dado[idx].append({
            'modelo': modelo.modelo,
            'acuracia': modelo.acuracia,
            'precisao': modelo.precisao,
            'recall': modelo.recall,
            'f1_score': modelo.f1_score
          })

        for noticia in resultado.noticias_referencias.all():
          dado['noticias'].append({
            'id': noticia.id, 'site': noticia.site.nome, 'titulo': noticia.titulo 
          })

        historico.append(dado)

      return historico, 200
    except Exception as e:
      return {'erro': str(e)}, 400

  def carregar_pontuacoes(self, projeto_id, id_processamento, noticia_id):
    try:
      self.projeto = Projeto.objects.get(pk=projeto_id)

      res_proc = ResultadoProcessamento.objects.filter(projeto=self.projeto,id_processamento=id_processamento).values('noticias_referencias')
      ref = [r['noticias_referencias'] for r in res_proc]

      dados = ProcessamentoSbert.objects.select_related().filter(projeto=self.projeto, noticia__pk=noticia_id, noticia_referencia__pk__in=ref)
      pontuacoes = []

      for dado in dados:
        pontuacoes.append({
          'id': dado.noticia_referencia.id,
          'noticia': dado.noticia_referencia.titulo,
          'site': dado.noticia_referencia.site.nome,
          'pontuacao': str(dado.pontuacao)
        })

      return pontuacoes, 200
    except Exception as e:
      return {'erro': str(e)}, 400

  def processar(self, post_data):
    def gerar_id():
      return str(datetime.now().timestamp())
    
    rotulos_projeto = {}
    if str(self.projeto.id) in ROTULOS_NOTICIAS:
      rotulos_projeto = ROTULOS_NOTICIAS[str(self.projeto.id)]

    n_decimais = 4

    id_processamento = post_data.get('id_processamento', None)
    noticias_ref_id = post_data.get('noticias', [])
    salvar_noticias = post_data.get('salvar_noticias', 'N')

    margem = decimal.Decimal(post_data.get('margem', 0.5))
    margem = round(margem, n_decimais)

    resultados = {
      'id_processamento': None, 'noticias_prox_limar': [],
      'limiar': '', 'margem': margem, 'limiar_ajustado': ''
    }

    limiar = None

    #Pegar informacoes do ultimo processamento desta sessão------------------------------
    if id_processamento is None:
      sessao = ResultadoProcessamento()
      sessao.id_processamento = id_processamento = gerar_id()
    else:
      sessao = ResultadoProcessamento.objects.filter(id_processamento=id_processamento).order_by('-criado_em')
      sessao = sessao.first()
      limiar = sessao.limiar_ajustado

    resultados['id_processamento'] = id_processamento
 
    classificador = Classificador()

    #Buscando todas as noticias do projeto
    noticias = ConteudoNoticia.objects.select_related().filter(projeto=self.projeto)

    #Buscando as noticias de referencia
    noticias_ref = ConteudoNoticia.objects.filter(projeto=self.projeto, pk__in=noticias_ref_id)

    #Fazendo a limpeza da lista com todas as noticias, rotulando e pontuando------------------------------
    #print("LIMPANDO AS NOTICIAS------------")
    dados_limpos = []

    for noticia in noticias:
      texto_limpo = classificador.ajustar_texto(
        noticia.titulo + ' ' + classificador.noneToStr(noticia.descricao) + ' ' + classificador.noneToStr(noticia.conteudo)
      )
      
      dados_limpos.append(texto_limpo)
    
    #print("FAZENDO AS PONTUACOES------------")
    for ref in noticias_ref:
      #limpando a noticia de referencia
      texto_limpo = classificador.ajustar_texto(
        ref.titulo + ' ' + classificador.noneToStr(ref.descricao) + ' ' + classificador.noneToStr(ref.conteudo)
      )
      
      #Pontuando as notícias
      for idx, noticia in enumerate(noticias):
        pontuacao = classificador.testar_sbert(dados_limpos[idx], texto_limpo)

        existe = ProcessamentoSbert.objects.filter(noticia__projeto=self.projeto,noticia_referencia=ref,noticia=noticia)

        #Gravando a pontuacao
        if len(existe) > 0:
          #Registro ja existe
          obj = existe.first()
        else:
          #Novo registro
          obj = ProcessamentoSbert()
          obj.noticia = noticia
          obj.noticia_referencia = ref
          obj.projeto = self.projeto

        obj.pontuacao = pontuacao
        obj.save()
   
    #Calculando classificacoes e totais------------------------------

    #Se não houver um limiar ajustado da ultima execução, calcular um baseado nas pontuacoesdesta execução
    #print("CALCULANDO OU BUSCANDO O LIMIAR------------")
    if limiar is None:
      limiar = decimal.Decimal(0.6)
      #limiar = ProcessamentoSbert.objects.filter(
      #  projeto=self.projeto, noticia_referencia__in=noticias_ref_id
      #).aggregate(Avg("pontuacao"))['pontuacao__avg']

    limiar = round(limiar, n_decimais)
    resultados['limiar'] = limiar

    #Guardar os rotulos gerados pelos calculos
    #print("CLASSIFICANDO AS NOTICIAS E SALVANDO------------")
    rotulos_classificados_limiar = []
    classificacoes = []
    rotulos_reais = []

    #Buscando 10 noticias perto do limiar (maiores e menores)
    n1 = ProcessamentoSbert.objects.select_related().filter(
      ~Q(noticia__pk__in=noticias_ref_id),
      projeto=self.projeto, noticia_referencia__in=noticias_ref_id,
      pontuacao__gte=limiar
    ).order_by('pontuacao').values('noticia_id').distinct()[:5]

    n1 = [n['noticia_id'] for n in n1] + noticias_ref_id

    n2 = ProcessamentoSbert.objects.select_related().filter(
      ~Q(noticia__pk__in=n1),
      projeto=self.projeto, noticia_referencia__in=noticias_ref_id,
      pontuacao__lt=limiar
    ).order_by('-pontuacao').values('noticia_id').distinct()[:5]

    n2 = [n['noticia_id'] for n in n2]

    for noticia in noticias:
      #Pesquisando as pontuações desta noticia e vendo qual passar pela margem e limiar
      classif_limiar = len(ProcessamentoSbert.objects.filter(noticia=noticia, noticia_referencia__in=noticias_ref_id, pontuacao__gte=limiar)) > 0
      rotulos_classificados_limiar.append(1 if classif_limiar else 0)
      classif_limiar = 'REAL' if classif_limiar else 'FALSA'

      if noticia.id in n1 or noticia.id in n2:
        indicador = 'SIM' if noticia.id in n1 else 'NÃO'
        resultados['noticias_prox_limar'].append({
          'indicador': indicador, 'id': noticia.id, 'titulo': noticia.titulo, 'site': noticia.site.nome,
          'url': noticia.url
        })

      rotulo = 'SEM RÓTULO'
      if str(noticia.id) in rotulos_projeto:
        rotulo = 'REAL' if rotulos_projeto[str(noticia.id)] else 'FALSA'
      
      rotulos_reais.append( 1 if rotulo == 'REAL' else 0 )

      classificacoes.append({
        'id': noticia.id, 'titulo': noticia.titulo, 'site': noticia.site.nome,
        'rotulo': rotulo, 'classificacao_limiar': classif_limiar
      })
      
      #Salvando as noticias classificadas como reais
      if salvar_noticias == 'S' and classif_limiar == 'REAL':
        noticia_processada = NoticiaProcessada.objects.filter(noticia=noticia).first()

        palavras_chaves = ''.join([p.palavra_chave for p in noticia.palavras_chaves.all()])
        if noticia_processada is None:
          #Adicionar noticia na base de noticias filtradas
          noticia_processada = NoticiaProcessada.objects.create(noticia=noticia, palavras_chaves=palavras_chaves)
        else:
          #Atualizar caso tenha uma nova palavra-chave
          noticia_processada.palavras_chaves = palavras_chaves
          noticia_processada.save(update_fields=['palavras_chaves'])

    noticias = []

    #Calculando o limiar ajustado-----------------------------
    #print("CALCULANDO O LIMIAR AJUSTADO------------")
    pontuacoes = ProcessamentoSbert.objects.filter(
      projeto=self.projeto, noticia_referencia__in=noticias_ref_id
    )

    soma_diff_quadrada = decimal.Decimal(0)
    for pontuacao in pontuacoes:
      soma_diff_quadrada += ((pontuacao.pontuacao - limiar) ** 2)

    media_diff_quadrada = round(soma_diff_quadrada / len(pontuacoes), n_decimais)
    desvio_padrao = round(math.sqrt(media_diff_quadrada),n_decimais)
    limiar_ajustado = round(limiar + (margem * media_diff_quadrada), n_decimais)

    resultados['limiar_ajustado'] = limiar_ajustado

    #print("CALCULANDO AS METRICAS------------")

    #Calculando acuracia, precisao, recall e f1-score----------------------
    resultados['metricas_calculadas'] = classificador.executar_classificacao_modelos({'texto': dados_limpos, 'label': rotulos_classificados_limiar})
    resultados['metricas_reais'] = classificador.executar_classificacao_modelos({'texto': dados_limpos, 'label': rotulos_reais}, True)

    #Pegando as imagens dos graficos de matriz de confusão
    #POR FAZER

    #Calculando % de similaridade entre rotulos reais e rotulos calculados
    #print("CALCULANDO METRICAS DE ROTULOS REAIS X CALCULADOS------------")
    qtd_acertos = 0
    verdadeiro_positivo = 0
    verdadeiro_negativo = 0
    falso_positivo = 0
    falsos_negativo = 0
    for idx, r in enumerate(rotulos_reais):
      igual = r == rotulos_classificados_limiar[idx]

      qtd_acertos += 1 if igual else 0

      verdadeiro_positivo += 1 if igual and r == 1 else 0
      verdadeiro_negativo += 1 if igual and r == 0 else 0

      falso_positivo += 1 if r == 0 and igual is False else 0
      falsos_negativo += 1 if r == 1 and igual is False else 0

    acuracia = round(qtd_acertos / len(rotulos_reais), n_decimais)
    precisao = round(verdadeiro_positivo / (verdadeiro_positivo + falso_positivo), n_decimais)

    recall = round(verdadeiro_positivo / (verdadeiro_positivo + falsos_negativo), n_decimais)
    f1_score = round(2 * (precisao * recall) / (precisao + recall), n_decimais)

    resultados['acuracia'] = str(acuracia)
    resultados['precisao'] = str(precisao)
    resultados['recall'] = str(recall)
    resultados['f1_score'] = str(f1_score)    

    #Salvando os dados calculados
    #print("SALVANDO OS DADOS CALCULADOS------------")
    with transaction.atomic():
      obj = ResultadoProcessamento()
      obj.id_processamento = id_processamento
      obj.projeto = self.projeto
      obj.limiar = limiar
      obj.margem = margem
      obj.media_diff_quadrada = media_diff_quadrada
      obj.desvio_padrao = desvio_padrao
      obj.limiar_ajustado = limiar_ajustado
      obj.acuracia = acuracia
      obj.precisao = precisao
      obj.recall = recall
      obj.f1_score = f1_score
      obj.save()

      for ref in noticias_ref:
        obj.noticias_referencias.add(ref)

      for modelo in resultados['metricas_calculadas']:
        obj_modelo = ClassificacaoModelo()
        obj_modelo.processamento = obj
        obj_modelo.modelo = modelo['modelo']
        obj_modelo.acuracia = modelo['acuracia']
        obj_modelo.precisao = modelo['precisao']
        obj_modelo.recall = modelo['recall']
        obj_modelo.f1_score = modelo['f1_score']
        obj_modelo.tipo_metrica = 'CALCULADA'
        obj_modelo.save()

      for modelo in resultados['metricas_reais']:
        obj_modelo = ClassificacaoModelo()
        obj_modelo.processamento = obj
        obj_modelo.modelo = modelo['modelo']
        obj_modelo.acuracia = modelo['acuracia']
        obj_modelo.precisao = modelo['precisao']
        obj_modelo.recall = modelo['recall']
        obj_modelo.f1_score = modelo['f1_score']
        obj_modelo.tipo_metrica = 'REAL'
        obj_modelo.save()

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
