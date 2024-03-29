<html>
  <head>
  </head>
  <body>
    <div>
      <h1 align="center"> Coleta de notícias </h1>
      <h3> Versão inicial do projeto de coleta de notícias </h3>
      <div>
        <h4>Sumário</h4>
        <ul>
          <li> <a href="#execucao">1. Estrutura de tabelas</a> </li>
          <li> <a href="#dados">3. Explicação dos dados</a> </li>
          <li> <a href="#estrutura_sistema">4. Estrutura do sistema</a> </li>
          <li> <a href="#execucao_via_site">5. Execução do programa via o site</a> </li>
        </ul>
      </div>
      <div id="estrutura_tabelas">
        <h4>2. Estrutura de tabelas</h4>
        <p>Nesta seção será detalhado a estrutura de tabelas.</p>
        <ul>
          <li>
            coleta_projeto (Tabela contendo os projetos)
          </li>
          <li>
            coleta_palavrachave (Tabela para cadastro das palavras chaves que serão utilizadas nos projetos)
          </li>
          <li>
            coleta_projeto_palavras_chaves (Tabela de vínculo de projetos com palavras chaves)
          </li>
          <li>
            coleta_sitenoticia (Tabela de sites que serão uitilizados para pesquisar as noticias)
          </li>
          <li>
            coleta_projeto_sites (Tabela de vínculo do projeto com o site de notícias)
          </li>
          <li>
            coleta_campo (Tabela com os campos quye serão coletados)
          </li>
          <li>
            coleta_initestruturanoticia (Tabela com informações de como a lista de notícias deve ser lida por site)
          </li>
          <li>
            coleta_estruturanoticia (Tabela que contém inrformações sobre os elementos html da noticia correspondente com o campo)
          </li>
          <li>
            coleta_conteudonoticia (Tabela com os dados coletados)
          </li>
          <li>
            coleta_conteudonoticia_palavras_chaves (Tabela para vínculo da notícia com a palavra chave que a gerou)
          </li>
          <li>
            coleta_log (Tabela de logs de erro da coleta)
          </li>
        </ul>
      </div>
      <div id="dados">
        <h4>3. Explicação dos dados</h4>
        <p>Nesta seção será explicado em detalhes o funcionamento do programa e como as tabelas interagem entre si.</p>
        <ul>
          <li>1. Inserir os campos e suas informações na tabela "coleta_campo", os campos devem ser únicos. Ex. titulo, descricao, imagem, etc..;</li>
          <li>2. Cadastrar os projetos na tabela "coleta_projeto";</li>
          <li>3. Cadastrar as palavras-chaves na tabela "coleta_palavrachave";</li>
          <li>4. Vincular projeto e palavra-chave na tabela "coleta_projeto_palavras_chaves", sem este vínculo nenhuma execução será feita;</li>
          <li>
            5. Cadastrar sites na tabela "coleta_sitenoticia";
            <ul>
              <li>5.1 Coluna "acessar_pagina_interna" (S|N) informa se o sistema deve acessar a pagina individual da noticia;</li>
              <li>5.2 Coluna "tipo_paginacao" informa o tipo de paginação. Caso não haja paginação, deixar vazio;</li>
              <li>5.3 Coluna "json_args" informa como deve executar a paginacao, informando a tag e atributo no caso de elmento html ou variaveis de url;</li>
              <li>5.4 Coluna "req_response" informa no caso da url_backend o tipo de retorno dos dados ou caso seja o index de um array de dados;</li>
            </ul>
          </li>
          <li>6. Vincular projeto com o site de busca na tabela "coleta_projeto_sites";</li>
          <li>7. Informar como as notícias esta estruturado o html da lista de notícias de cada site na tabela "coleta_initestruturanoticia", ou seja, informar como encontrar a lista de notícias;</li>
          <li>8. Informar na tabela "coleta_estruturanoticia" como esta estruturado o html para resgatar os campos cadastrados na tabela "coleta_campo" de cada notícia do site específico;</li>
          <li>9. A tabela "conteudo_noticia" conterá os dados coletados, uma linha por notícia, de maneira unica considerando titulo, site e projeto;</li>
          <li>10. A tabela "coleta_conteudonoticia_palavras_chaves" irá possuir o vínculo entre a palavra-chave e a notícia gerada;</li>
          <li>11. A tabela "coleta_logs" conterá os logs de erros, como:
            <ul>
              <li>11.1 Erro de acesso á lista de notícias do site;</li>
              <li>11.2 Erro de acesso á página individual da notícia (quando informada que pode ser acessada);</li>
              <li>11.3 Erro de gravação de imagem;</li>
              <li>11.4 Erro de paginação;</li>
            </ul>
          </li>
        </ul>
      </div>
      <div id="estrutura_sistema">
        <h4>4. Estrutura do sistema</h4>
        <p>
          O sistema esta estruturado da seguinte forma:
        </p>
        <ul>
         ...
        </ul>
      </div>
      <div id="execucao_via_site">
        <h4>5. Execução do programa via o site</h4>
        <ul>
          <li>1. Iniciar o serviço do docker (docker desktop via interface ou iniciar o serviço via cmd)</li>
          <li>2. Modificar o arquivo example.env para .env e altera as informações de acesso</li>
          <li>3. Executar o comando: docker compose build</li>
          <li>4. Executar o comando: docker compose up -d</li>
          <li>5. Executar o comando: docker compose run web python3 manage.py init_db (executar uma unica vez durante a instalação)</li>
          <li>6. O site pode ser acessado via a url http://localhost:8000</li>
          <li>7. O acesso se dará com usuário e senha informados na etapa 2</li>
        </ul>
      </div>
    </div>
  </body>
</html>
