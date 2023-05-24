import sys
from coleta import Coleta

if __name__ == "__main__":

  if len(sys.argv) == 1:
    print('Nenhum projeto foi passado como argumento!')
  else:
    projetos_id = str(sys.argv[1]).split(',')

    palavra_chave = 0
    if len(sys.argv) == 3:
      palavra_chave = str(sys.argv[2])

    coleta = Coleta(projetos_id, palavra_chave)
    coleta.executar()
