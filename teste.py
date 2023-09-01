import decimal

import sentence_transformers
import spacy
import Levenshtein

nlp_spacy = spacy.load('pt_core_news_lg')

def noneToStr(val):
  if val is None:
    return ''
  return val

def limpar(texto):
  texto = texto.replace('\xa0','')
  texto = texto.replace('"',"'")
  texto = texto.replace("\n", " ")
  texto = texto.translate ({ord(c): "" for c in "!@#$%^&*()[]{};:,./<>?\|`~=_+"})
  texto = texto.lower()
  return ''.join(texto.strip().lower().replace('"',"'").splitlines())

def ajustar_texto(frase):
  #Removendo quebra de linhas
  frase = limpar(frase)
  doc = nlp_spacy(frase)

  filtrado = []
  for token in doc:
    if not token.is_stop and token.text.strip() not in ["","'",'"'] and not token.text.isnumeric():
      filtrado.append(token.lemma_)

  return filtrado

def testar_sentencas(seq1, seq2):
  if type(seq1).__name__ == 'list':
    score = Levenshtein.seqratio(seq1, seq2)
  else:
    score = Levenshtein.ratio(seq1, seq2)
  return decimal.Decimal('{:.4f}'.format(score))

def testarSbert(texto1, texto2):
  model = sentence_transformers.SentenceTransformer('all-MiniLM-L6-v2')
  emb1 = model.encode(' '.join(texto1))
  emb2 = model.encode(' '.join(texto2))

  cos_sim = sentence_transformers.util.cos_sim(emb1, emb2)
  score = cos_sim[0][0]
  return decimal.Decimal('{:.4f}'.format(score))

NOTICIA_REFERENCIA_TITULO = "Caravelas-portuguesas estão presentes nas praias de Penha e Balneário Piçarras nesta quinta-feira"
NOTICIA_REFERENCIA_TITULO_T = ajustar_texto(NOTICIA_REFERENCIA_TITULO)

NOTICIA_REFERENCIA_TEXTO = """
  Caravelas-portuguesas estão presentes nas praias de Penha e Balneário Piçarras nesta quinta-feira
  O leitor Marcos Aguiar enviou imagem de uma caravela-portuguesa encontrada por ele mesmo em uma…
  O leitor Marcos Aguiar enviou imagem de uma caravela-portuguesa encontrada por ele mesmo em uma das praias de Penha.
  Pela manhã, os guarda-vidas já hasteavam bandeiras lilás nos postos, indicando a presença de águas-vivas na região. Durante o dia, os bombeiros militares foram acionados para atendimento à vítimas de queimaduras pelas caravelas, tanto em Penha quanto em Balneário Piçarras
  Conforme o Penha Online já havia informado em outras ocasiões, veja como se proteger e remediar em caso de contato
  Devido ao vento maral, as Caravelas-Portuguesas continuam chegando em nossas praias. De acordo com o biólogo Éric Comin as caravelas-portuguesas oferecem grande risco, pois seus tentáculos liberam substâncias extremamente urticantes que podem causar queimaduras de terceiro grau.
  Apesar de interessantes, não se iluda com suas cores e tons translúcidos e vibrantes: elas são venenosas. Muito confundidas com águas-vivas, seus parentes próximos, elas são bem mais perigosas, podendo até matar. Importante frisar que os organismos não atacam, porém o contato na região torácica de crianças ou de doentes cardíacos com as toxinas das caravelas-portuguesas pode causar arritmia cardíaca ou até mesmo parada cardiorrespiratória, que pode levar à morte.
  Em contato com uma caravela, os especialistas indicam nunca lavar a região afetada com água doce, pois ela espalha as células urticantes. Como consequência, aumenta a área queimada e a dor. Tampouco deve-se tentar limpar com álcool e esfregar a área atingida. Os primeiros socorros devem ser feitos ainda na praia, lavando a região afetada com água do mar. A água salgada pode ser levada para casa a fim de continuar o tratamento. Gelada, deve-se aplicá-la até a dor passar e a vermelhidão diminuir. É indicado ainda o uso de vinagre, que impede que as toxinas se espalhem no corpo e também alivia a dor. Se possível, recomenda-se buscar assistência médica.
"""
NOTICIA_REFERENCIA_TEXTO_T = ajustar_texto(NOTICIA_REFERENCIA_TEXTO)

NOTICIA_TITULO = "Praia do Estaleiro amanheceu com muitas caravelas-portuguesas  nesta quarta"
NOTICIA_TITULO_T = ajustar_texto(NOTICIA_TITULO)

NOTICIA_TEXTO = """
Praia do Estaleiro amanheceu com muitas caravelas-portuguesas  nesta quarta
O contato com as caravelas pode causar irritação forte, dor intensa e queimaduras de até terceiro grau
Nesta quarta-feira (09), a Praia do Estaleiro amanheceu com muitas caravelas-portuguesas (Physalia physalis). Os organismos marinhos, que têm o corpo gelatinoso, foram encontrados na areia.

Com a proximidade do verão, a água do mar fica mais quente, favorecendo o surgimento de águas-vivas e caravelas nas praias de Balneário Camboriú. Esses organismos são jogados para o mar em função dos ventos e das correntes. Apesar de o fenômeno ser natural e comum, os frequentadores devem evitar tocar nesses organismos, pois eles liberam toxinas em caso de contato físico.

Como o contato com as caravelas pode causar irritação forte, dor intensa e queimaduras de até terceiro grau, a Secretaria do Meio Ambiente de Balneário Camboriú orienta que a população que não se aproxime desses organismos e não os toque. “É bom as pessoas ficarem alertas, evitarem contato com o organismo, principalmente quando ele estiver na água, mas também na areia porque ele pode ainda causar ardência”, explica a secretária do Meio Ambiente, Maria Heloisa Furtado Lenzi.

CONTINUA APÓS O ANÚNCIO

Em caso de contato, a pessoa deve lavar a área da pele atingida com a própria água do mar ou com vinagre. Ela jamais deve usar água doce, nem esfregar a região afetada. Se a dor e a vermelhidão não passarem com as horas, a pessoa deve buscar atendimento médico.
"""
NOTICIA_TEXTO_T = ajustar_texto(NOTICIA_TEXTO)

print("\n------------------------TITULO------------------------\n")

print("Referência: \n", NOTICIA_REFERENCIA_TITULO,"\n")
print("Tratado: \n", NOTICIA_REFERENCIA_TITULO_T,"\n")

print("Original: \n", NOTICIA_TITULO,"\n")
print("Tratado: \n", ajustar_texto(NOTICIA_TITULO),"\n")

print("Levenshtein (ratio) (String original):", testar_sentencas(NOTICIA_TITULO,NOTICIA_REFERENCIA_TITULO))
print("Levenshtein (seqratio) (String Tratada):", testar_sentencas(NOTICIA_TITULO_T, NOTICIA_REFERENCIA_TITULO_T))

print("\n------------------------TEXTO INTEIRO------------------------\n")

print("Referência: \n", NOTICIA_REFERENCIA_TEXTO,"\n")
print("Tratado: \n", NOTICIA_REFERENCIA_TEXTO_T,"\n")

print("Original: \n", NOTICIA_TEXTO,"\n")
print("Tratado: \n", NOTICIA_TEXTO_T,"\n")
print("Sentence transformers (sbert): ", testarSbert(NOTICIA_TEXTO_T,NOTICIA_REFERENCIA_TEXTO_T))
print("Sentence transformers (sbert): ", testarSbert(NOTICIA_TITULO_T, NOTICIA_REFERENCIA_TITULO_T))