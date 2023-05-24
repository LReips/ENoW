SITES_SQL = """SELECT ppj.sitenoticia_id pagjornal_id,  pj.url, sb.palavra_chave, ppj.projeto_id, pj.acessar_pagina_interna, 
                pj.tipo_paginacao, pj.json_args, pj.req_response, sb.id palavra_chave_id
               FROM coleta_projeto_sites as ppj
               inner join coleta_sitenoticia pj on (pj.id = ppj.sitenoticia_id)
               inner join coleta_projeto_palavras_chaves as ps on (ps.projeto_id = ppj.projeto_id)
               inner join coleta_palavrachave as sb on (sb.id = ps.palavrachave_id)
               where ppj.projeto_id = %s and (ps.palavrachave_id = %s or %s = 0)"""

INICIO_ESTRUTURA_SQL = """SELECT id, tag, caminho
                          FROM coleta_initestruturanoticia 
                          WHERE site_id = %s"""

INSERE_LOG_SQL = """INSERT INTO coleta_log (inserido_em, id_coleta, projeto_id, site_id, url, palavra_chave_id, erro, titulo, conteudo_noticia_id) 
                    VALUES (CURRENT_TIMESTAMP, %s, %s, %s, %s, %s, %s, %s, %s);"""

ESTRUTURAS_SQL = """SELECT e.id, c.tipo, e.tag, e.caminho, e.subtag, e.subtag_caminho
                    FROM coleta_campo c 
                    INNER JOIN coleta_estruturanoticia e ON (c.id = e.campo_id)
                    WHERE e.inicio_estrutura_noticia_id = %s AND e.tipo_pagina = %s;"""

VERIFICAR_NOTICIA_EXISTE = """SELECT cn.id, cn.titulo, 
                                (CASE WHEN cs.palavrachave_id is not null THEN 'S' ELSE 'N' END) as palavra_chave_repetida 
                              FROM coleta_conteudonoticia cn
                              LEFT JOIN coleta_conteudonoticia_palavras_chaves cs on (cs.conteudonoticia_id = cn.id and cs.palavrachave_id = %s)
                              WHERE (cn.site_id = %s and cn.titulo = %s and cn.projeto_id = %s);"""

INSERE_NOTICIA_SQL = """INSERT INTO coleta_conteudonoticia (data_coleta, titulo, descricao, conteudo, dia, mes, ano, localizacao, imagem, url, inicio_estrutura_noticia_id, site_id, caminho_img_local, id_coleta, projeto_id, data_formatada)
                        VALUES (current_date(), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""

INSERE_NOTICIA_PALAVRA_CHAVE_SQL = "INSERT INTO coleta_conteudonoticia_palavras_chaves (palavrachave_id, conteudonoticia_id) VALUES (%s, %s)"