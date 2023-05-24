import requests
import os
import pathlib
import uuid
import random

class Noticia:
  id = None
  id_coleta = None
  projeto_id = None
  titulo = ""
  data_formatada = ""
  descricao = ""
  conteudo =  ""
  dia = ""
  mes =  ""
  ano = ""
  localizacao =""
  imagem = ""
  url = ""
  estrutura_noticia_id = None 
  pagjornal_id = None
  caminho_img = ""

  salvou_imagem = False
  erro_imagem = ''

  def retornar_args(self):
    return (str(self.titulo), str(self.descricao), str(self.conteudo), str(self.dia), str(self.mes), str(self.ano), str(self.localizacao),
            str(self.imagem), str(self.url), self.estrutura_noticia_id, self.pagjornal_id, str(self.caminho_img), self.id_coleta, self.projeto_id, self.data_formatada)

  def salvar_imagem(self, imagem):

    pasta = os.path.join(pathlib.Path().resolve(), "imagens_coletor", str(self.id_coleta))
    if not os.path.exists(pasta):
      os.makedirs(pasta)

    caminho_img = os.path.join(pasta, str(random.randint(0, 10)) + uuid.uuid4().hex + '.jpg')

    try:
      if type(imagem) is str:
        self.imagem = imagem
      else:
        self.imagem = imagem.get("src") or imagem.get("data-src")

      if self.imagem.startswith('//'):
        self.imagem = 'https:' + self.imagem

      img_data = requests.get(self.imagem, headers={"User-Agent": "XY"}).content

      with open(caminho_img, 'wb') as handler:
        handler.write(img_data)

      self.caminho_img = caminho_img
      self.salvou_imagem = True
    except Exception as err:
      if os.path.exists(caminho_img):
        os.remove(caminho_img)
      self.imagem = ''
      self.caminho_img = ''
      self.erro_imagem = err
      self.salvou_imagem = False

  def deletar_imagem(self):
    if self.caminho_img is not None and self.caminho_img != "":
     if os.path.exists(self.caminho_img):
        os.remove(self.caminho_img)