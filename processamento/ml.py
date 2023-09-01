import json
import decimal
import pandas as pd
import re
import matplotlib.pyplot as plt
import seaborn as sns
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
from scipy.stats import pearsonr, spearmanr

from coleta.models import (Projeto, ConteudoNoticia)
from .models import ProcessamentoSbert

class Classificador:
  def __init__(self):
    self.projeto = Projeto.objects.get(pk=1)
    self.rotulos = { '1':1, '2':0, '3':1, '4':0, '5':0, '6':0, '7':0, '8':0, '9':1, '10':0, '11':0, '12':0, '13':0, '14':0, '15':0, '16':0, '17':0, '18':1, '19':0, '20':0, '21':1, '22':1, '23':1, '24':1, '25':1, '26':1, '27':0, '28':0, '29':0, '30':0, '31':0, '32':0, '33':0, '34':0, '35':0, '36':0, '37':0, '38':0, '39':0, '40':0, '41':0, '42':0, '43':0, '44':0, '45':0, '46':0, '47':0, '48':0, '49':0, '50':0, '51':0, '52':0, '53':0, '54':0, '55':0, '56':0, '57':0, '58':0, '59':0, '60':0, '61':0, '62':0, '63':0, '64':0, '65':0, '66':1, '67':0, '68':0, '69':0, '70':0, '71':0, '72':0, '73':0, '74':0, '75':0, '76':0, '77':1, '78':0, '79':0, '80':1, '81':0, '82':0, '83':0, '84':0, '85':0, '86':0, '87':0, '88':1, '89':0, '90':1, '91':1, '92':1, '93':1, '94':1, '95':1, '96':1, '97':1, '98':0, '99':1, '100':1, '101':1, '102':1, '103':1, '104':1, '105':1, '106':1, '107':1, '108':1, '109':1, '110':1, '111':1, '112':1, '113':1, '114':1, '115':1, '116':1, '117':1, '118':1, '119':1, '120':1, '121':1, '122':1, '123':1, '124':1, '125':1, '126':0, '127':1, '128':1, '129':0, '130':0, '131':1, '132':0, '133':0, '134':1, '135':0, '136':0, '137':0, '138':0, '139':0, '140':0, '141':0, '142':0, '143':0, '144':0, '145':0, '146':0, '147':0, '148':0, '149':0, '150':0, '151':0, '152':0, '153':0, '154':0, '155':0, '156':0, '157':0, '158':0, '159':1, '160':1, '161':0, '162':0, '163':0, '164':0, '165':0, '166':0, '167':0, '168':0, '169':0, '170':0, '171':0, '172':0, '173':0, '174':0, '175':0, '176':0, '177':0, '178':0, '179':0, '180':0, '181':0, '182':0, '183':0, '184':0, '185':0, '186':0, '187':0, '188':0, '189':1, '190':0, '191':0, '192':0, '193':0, '194':1, '195':1, '196':0, '197':0, '198':1, '199':0, '200':1, '201':1, '202':1, '203':1, '204':0, '205':1, '206':1, '207':0, '208':0, '209':0, '210':0, '211':0, '212':0, '213':0, '214':0, '215':0, '216':0, '217':0, '218':0, '219':0, '220':0, '221':0, '222':1, '223':0, '224':0, '225':0, '226':0, '227':0, '228':0, '229':0, '230':0, '231':0, '232':0, '233':0, '234':0, '235':0, '236':0, '237':0, '238':0, '239':0, '240':0, '241':0, '242':0, '243':0, '244':0, '245':0, '246':0, '247':0, '248':0, '249':0, '250':0, '251':0, '252':0, '253':0, '254':0, '255':0, '256':0, '257':0, '258':0, '259':0, '260':0, '261':0, '262':0, '263':0, '264':0, '265':0, '266':0, '267':0, '268':0, '269':0, '270':0, '271':0, '272':0, '273':0, '274':0, '275':0, '276':0, '277':0, '278':0, '279':0, '280':0, '281':0, '282':0, '283':0, '284':0, '285':0, '286':0, '287':0, '288':0, '289':0, '290':0, '291':0, '292':0, '293':0, '294':0, '295':0, '296':0, '297':0, '298':0, '299':0, '300':0, '301':0, '302':0, '303':0, '304':0, '305':0, '306':0, '307':0, '308':1, '309':0, '310':1, '311':1, '312':0, '313':0, '314':0, '315':0, '316':0, '317':0, '318':0, '319':1, '320':0, '321':0, '322':0, '323':0, '324':0, '325':0, '326':0, '327':0, '328':1, '329':1, '330':0, '331':0, '332':0, '333':1, '334':0, '335':0, '336':0, '337':0, '338':0, '339':0, '340':0, '341':0, '342':0, '343':0, '344':0, '345':0, '346':0, '347':0, '348':0, '349':0, '350':0, '351':0, '352':0, '353':0, '354':0, '355':0, '356':0, '357':0, '358':0, '359':0, '360':0, '361':0, '362':0, '363':0, '364':0, '365':0, '366':0, '367':1, '368':0, '369':0, '370':0, '371':0, '372':0, '373':0, '374':0, '375':0, '376':0, '377':0, '378':0, '379':0, '380':0, '381':0, '382':0, '383':0, '384':0, '385':0, '386':0, '387':0, '388':0, '389':0, '390':0, '391':0, '392':0, '393':1, '394':0, '395':0, '396':0, '397':0, '398':0, '399':0, '400':0, '401':0, '402':0, '403':0, '404':0, '405':0, '406':0, '407':0, '408':0, '409':0, '410':0, '411':0, '412':0, '413':0, '414':0, '415':0, '416':0, '417':0, '418':0, '419':0, '420':0, '421':0, '422':0, '423':0, '424':0, '425':0, '426':0, '427':0, '428':0, '429':0, '430':0, '431':0, '432':0, '433':0, '434':0, '435':0, '436':0, '437':0, '438':0, '439':0, '440':0, '441':0, '442':0, '443':0, '444':0, '445':0, '446':1, '447':0, '448':0, '449':0, '450':0, '451':0, '452':0, '453':0, '454':0, '455':0, '456':0, '457':0, '458':0, '459':0, '460':0, '461':0, '462':0, '463':0, '464':0, '465':0, '466':0, '467':0, '468':0, '469':0, '470':0, '471':0, '472':0, '473':0, '474':0, '475':0, '476':0, '477':0, '478':0, '479':0, '480':0, '481':0, '482':0, '483':0, '484':0, '485':0, '486':0, '487':0, '488':0, '489':0, '490':0, '491':0, '492':0, '493':0, '494':0, '495':0, '496':0, '497':0, '498':0, '499':0, '500':0, '501':0, '502':0, '503':0, '504':0, '505':0, '506':0, '507':0, '508':0, '509':0, '510':0, '511':0, '512':0, '513':1, '514':1, '515':1, '516':0, '517':0, '518':1, '519':0, '520':0, '521':0, '522':0, '523':0, '524':0, '525':0, '526':0, '527':0, '528':1, '529':0, '530':0, '531':0, '532':0, '533':0, '534':0, '535':0, '536':0, '537':0, '538':0, '539':0, '540':0, '541':0, '542':0, '543':0, '544':0, '545':0, '546':0, '547':0, '548':0, '549':0, '550':0, '551':0, '552':0, '553':0, '554':0, '555':0, '556':0, '557':0, '558':0, '559':0, '560':0, '561':0, '562':0, '563':0, '564':0, '565':0, '566':0, '567':0, '568':0, '569':0, '570':0, '571':0, '572':0, '573':0, '574':0, '575':0, '576':0, '577':0, '578':0, '579':0, '580':0, '581':0, '582':0, '583':0, '584':0, '585':0, '586':0, '587':0, '588':0, '589':0, '590':0, '591':1, '592':0, '593':0, '594':0, '595':0, '596':0, '597':0, '598':1, '599':0, '600':0, '601':0, '602':0, '603':0, '604':0, '605':0, '606':0, '607':0, '608':0, '609':0, '610':0, '611':0, '612':0, '613':0, '614':0, '615':0, '616':0, '617':0, '618':0, '619':0, '620':0, '621':0, '622':1, '623':1 }

  def comparar(self):
    try:
      #Pegando os rótulos
      similarities_real = [self.rotulos[r] for r in self.rotulos]

      # Exemplo de similaridades calculadas pelo modelo Sentence BERT
      similarities_calculated = [
        float(noticia.pontuacao) for noticia in ProcessamentoSbert.objects.filter(projeto=self.projeto)
      ]

      # Calcular coeficiente de correlação de Pearson
      pearson_corr, _ = pearsonr(similarities_calculated, similarities_real)

      # Calcular coeficiente de correlação de Spearman
      spearman_corr, _ = spearmanr(similarities_calculated, similarities_real)

      # Calcular Mean Squared Error
      mse = mean_squared_error(similarities_real, similarities_calculated)
      
      return {
        "pearson:": pearson_corr,
        "spearman:": spearman_corr,
        "mean_squared_error:": mse
      }, 200
    except Exception as e:
      
      return {"erro": str(e)}, 400

  def salvar_json(self, dados_df):
    pass

  def executar(self):
    def noneToStr(val):
      if val is None:
        return ''
      return val
    
    # Limpeza de dados
    def clean_text(text):
      text = re.sub(r'[^\w\s]', '', text.lower())  # Remover pontuações e converter para minúsculas
      return text
 
    data = {
      'text': [],
      'label': []
    }

    try:
      noticias = ConteudoNoticia.objects.filter(projeto=self.projeto).order_by('id')
      
      for noticia in noticias:
        texto = noticia.titulo + ' ' + noneToStr(noticia.descricao) + ' ' + noneToStr(noticia.conteudo)
        data['text'].append(texto)

        if str(noticia.id) in self.rotulos:
          data['label'].append(self.rotulos[str(noticia.id)])
        else:
          data['label'].append(0)
      
      # Criar um DataFrame a partir dos dados
      df = pd.DataFrame(data)

      df['cleaned_text'] = df['text'].apply(clean_text)

      # Tokenização
      df['tokenized_text'] = df['cleaned_text'].apply(lambda x: x.split())

      # Remoção de stopwords (usando stopwords fictícias como exemplo)
      stopwords = ['nas', 'do', 'de', 'o', 'os', 'a', 'as', 'como']
      df['filtered_text'] = df['tokenized_text'].apply(lambda x: [word for word in x if word not in stopwords])

      # Stemming e Lemmatization (usando uma abordagem fictícia)
      stemmer = lambda x: x[:4]  # Stemmer fictício que remove os últimos caracteres das palavras
      lemmatizer = lambda x: x + 'a'  # Lemmatizer fictício que adiciona 'a' no final das palavras
      df['stemmed_text'] = df['filtered_text'].apply(lambda x: [stemmer(word) for word in x])
      df['lemmatized_text'] = df['filtered_text'].apply(lambda x: [lemmatizer(word) for word in x])

      # Vetorização usando TF-IDF
      tfidf_vectorizer = TfidfVectorizer(max_df=0.8, min_df=0.1)
      tfidf_matrix = tfidf_vectorizer.fit_transform(df['lemmatized_text'].apply(' '.join))

      # Tratamento de palavras raras ou frequentes
      vocab = tfidf_vectorizer.get_feature_names_out()
      df_tfidf = pd.DataFrame(tfidf_matrix.toarray(), columns=vocab)

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
          #("Regressão Logística", LogisticRegression()),
          #("Árvore de Decisão", DecisionTreeClassifier()),
          ("Random Forest", RandomForestClassifier()),
          #("K-Nearest Neighbors", KNeighborsClassifier(n_neighbors=3)),
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

        resultados.append({
          "modelo": name,
          "acuracia": f"{accuracy:.4f}",
          "precisao": f"{precision:.4f}",
          "recall": f"{recall:.4f}",
          "f1-score": f"{f1:.4f}"
        })

      df.drop('text', axis=1, inplace=True)
      df.drop('filtered_text', axis=1, inplace=True)
      df.drop('cleaned_text', axis=1, inplace=True)
      df_json = df.to_json(orient='records')[1:-1].replace('},{', '} {')

      self.salvar_json(df_json)

      return resultados, 200
    except Exception as e:
      return {"erro": str(e)}, 400