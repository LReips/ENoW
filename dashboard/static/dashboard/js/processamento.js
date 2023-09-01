$(document).ready(function(){
  $.extend( $.fn.dataTable.defaults, {
    language: {
      "url": "/static/dashboard/datatables/pt-BR.json"
    },
    responsive: true,
    autoWidth: false,
    lengthMenu: [[10, 20, 25, 50, -1],[10, 20, 25, 50, "TODOS"]],
    pageLength: 10,
  });
  
  const tabela_noticias = new DataTable("#tabela_noticias",{fixedHeader: true})
  const tabela_processamento = new DataTable("#tabela_processamento",{fixedHeader: true})

  const modal_historico = $("#modal_historico")
  const modal_matriz_confusao = $("#modal_matriz_confusao")
  const modal_pontuacoes = $("#modal_pontuacoes")

  const input_margem = $("#margem")
  const input_salvar_noticias = $("#salvar_noticias")
  const csrf_token = $("#csrf_token").val()

  /* Variavel de controle de processamento */
  const processamento = {
    id: null,
    projeto_id: $("#projeto_id").val(),
    noticias_selecionadas: {},
    limpar(id){
      this.id = id
      this.noticias_selecionadas = {}
    }
  }

  const modal_alertavel = $("#alertavel").on('hidden.bs.modal', function (e) {
    modal_historico.removeClass("modal-backdrop")
  })

  const btn_executar_processamento = $("#executar_processamento").click(function(){
    let noticias = Object.keys(processamento.noticias_selecionadas)
    if (noticias.length == 0) {
      aviso(false, "Seleciona uma ou mais notícias!")
    } else {
      toggle_botoes(false)
      executar_processamento(noticias)
    }
  })

  const btn_historico_processamento = $("#historico_processamento").click(function(){
    toggle_botoes(false)
    carregar_historico()
  })

  const executar_processamento = noticias => {
    let conf = {
      method: "POST",  
      headers: {"Content-Type": "application/json", 'X-CSRFToken': csrf_token},
      mode: 'same-origin',
      body: JSON.stringify({
        id_processamento: processamento.id,
        noticias: noticias,
        margem: input_margem.val() == ''? '0.5': input_margem.val(),
        salvar_noticias: input_salvar_noticias.is(':checked')? 'S':'N'
      })
    }

    fetch(`/processamento/executar_processamento/${processamento.projeto_id}`, conf)
    .then(response => {
      if (!response.ok) {
        console.log(response)
        throw new Error("Um erro aconteceu executar o processamento!")
      } else {
        return response.json()
      }
    })
    .then(data => {
      montar_tabela_noticias_proximas(data.resultados.noticias_prox_limar)
      montar_classificacoes(data.classificacoes)
      montar_resultado_atual(data.resultados)

      let msg = 
        `<b>Processamento finalizado</b><br>
         Inicio: ${data.tempo.inicio}<br>
         Fim: ${data.tempo.fim}<br>
         Tempo (minutos): ${data.tempo.diff_minutos}<br>
         Tempo (segundos): ${data.tempo.diff_segundos}`

      aviso(true, msg)
      toggle_botoes(true)

      processamento.limpar(data.resultados.id_processamento)
      tabela_noticias.$("input[name='noticias']:checked").prop("checked", false)
    })
    .catch((error) => {
      aviso(false, error)
    })
  }

  const montar_resultado_atual = resultados => {
    let div_cm = modal_matriz_confusao.find(".modal-body > .row")
    div_cm.empty()

    const montar = (div, arr, montar_matriz) => {
      arr.forEach(modelo => {
        div.append(`
          <hr>
          <div class="row" style="margin-top: 3px">
            <div class="col-12"> <b>Modelo: ${modelo.modelo}</b> </div>
            <div class="col-6"> <b>Acurácia: ${modelo.acuracia}</b> </div>
            <div class="col-6"> <b>Precisão: ${modelo.precisao}</b> </div>
            <div class="col-6"> <b>Recall: ${modelo.recall}</b> </div>
            <div class="col-6"> <b>F1-Score: ${modelo.f1_score}</b> </div>
          </div>
        `)

        if (montar_matriz) {
          div_cm.append(`
            <div class="col-12">
              <img src="${modelo.imagem}"/>
            </div>
          `)
        }
      })
    }

    let div_metricas_rotulos_reais = $("#div_metricas_rotulos_reais")
    div_metricas_rotulos_reais.empty().append(`
      <div class="col-12 text-start" style="margin-top: 5px;">
        <button class="btn btn-secondary" type="button" data-bs-toggle="collapse" data-bs-target="#modelos_metricas_reais" aria-expanded="false">
          Métricas reais
        </button>

        <button id="ver_modal_matriz_confusao" class="btn btn-secondary">Ver matriz de confusão</button>
      </div>
      <div id="modelos_metricas_reais" class="col-12 collapse"></div>
    `)
    montar($("#modelos_metricas_reais"), resultados.metricas_reais, true)

    let div_totais_atual = $("#div_totais_atual")
    div_totais_atual.empty()

    div_totais_atual.append(`
      <div class="col-12" style="margin-top: 5px;">
        <b> Limiar: ${resultados.limiar.replace('.',',')} | Margem: ${resultados.margem.replace('.',',')} | Limiar ajustado: ${resultados.limiar_ajustado.replace('.',',')}</b>
        <br>
        <b> Acurácia: ${resultados.acuracia.replace('.',',')}</b> | <b> Precisão: ${resultados.precisao.replace('.',',')}</b>
        <br>
        <b> Recall: ${resultados.recall.replace('.',',')}</b> | <b> F1-Score: ${resultados.f1_score.replace('.',',')}</b>
      </div>
      <div class="col-12 text-start">
        <button class="btn btn-secondary" type="button" data-bs-toggle="collapse" data-bs-target="#modelos_metricas_calculadas" aria-expanded="false">
          Métricas calculadas
        </button>
      </div>
      <div id="modelos_metricas_calculadas" class="col-12 collapse"></div>
    `)
    montar($("#modelos_metricas_calculadas"), resultados.metricas_calculadas, false)
  }

  const montar_tabela_noticias_proximas = noticias => {
    tabela_noticias.clear()

    let up =
       `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-arrow-up-short" viewBox="0 0 16 16"  style="color:green;">
          <path fill-rule="evenodd" d="M8 12a.5.5 0 0 0 .5-.5V5.707l2.146 2.147a.5.5 0 0 0 .708-.708l-3-3a.5.5 0 0 0-.708 0l-3 3a.5.5 0 1 0 .708.708L7.5 5.707V11.5a.5.5 0 0 0 .5.5z"/>
        </svg>`

    let down = 
      `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-arrow-down-short" viewBox="0 0 16 16" style="color:red;">
        <path fill-rule="evenodd" d="M8 4a.5.5 0 0 1 .5.5v5.793l2.146-2.147a.5.5 0 0 1 .708.708l-3 3a.5.5 0 0 1-.708 0l-3-3a.5.5 0 1 1 .708-.708L7.5 10.293V4.5A.5.5 0 0 1 8 4z"/>
      </svg>`

    noticias.forEach(noticia=> {
      tabela_noticias.row.add([
        noticia.id, `${noticia.indicador == 'SIM'? up:down} ${noticia.titulo}`, noticia.site,
        `<button class="btn btn-secondary ver_pontuacoes" value="${noticia.id}">Ver</button>`,
        `<a class="btn btn-info btn-sm" href="${noticia.url}" target="_blank">Acessar</a>`,
        `<div class="btn-group" role="group">
          <input type="checkbox" class="btn-check check_noticias" name="noticias" value="${noticia.id}" id="noticia_check_${noticia.id}" autocomplete="off">
          <label class="btn btn-outline-primary spc_label" for="noticia_check_${noticia.id}">Selecionar</label>
        </div>`
      ])
    })

    tabela_noticias.draw()
  }

  const carregar_historico = () => {
    fetch(`/processamento/carregar_historico/${processamento.projeto_id}?id_processamento=${processamento.id}`)
    .then(response => {
      if (!response.ok) {
        console.log(response)
        throw new Error("Um erro aconteceu ao carregar o histórico!")
      } else {
        return response.json()
      }
    })
    .then(data => {
      montar_historico(data)
      toggle_botoes(true)
    })
    .catch((error) => {
      aviso(false, error)
    })
  }

  const montar_historico = dados => {
    let div = modal_historico.find(".modal-body")
    div.empty()

    if (dados.length == 0) {
      div.append("Esta execução não possui histórico!")
    }

    dados.forEach((dado, i) => {
      let modelos_reais = ''
      let modelos_calculados = ''
      let noticias = ''

      dado.noticias.forEach(noticia => {
        noticias += 
          `<hr>
           <div class="row text-start" style="margin-top: 3px">
             <div class="col-12"> <b>Id: ${noticia.id}</b> </div>
             <div class="col-12"> <b>Site: ${noticia.site}</b> </div>
             <div class="col-12"> <b>Titulo: ${noticia.titulo}</b> </div>
           </div>`
      })

      dado.modelos_reais.forEach(modelo => {
        modelos_reais += 
          `<hr>
           <div class="row text-start" style="margin-top: 3px">
             <div class="col-12"> <b>Modelo: ${modelo.modelo}</b> </div>
             <div class="col-6"> <b>Acurácia: ${modelo.acuracia}</b> </div>
             <div class="col-6"> <b>Precisão: ${modelo.precisao}</b> </div>
             <div class="col-6"> <b>Recall: ${modelo.recall}</b> </div>
             <div class="col-6"> <b>F1-Score: ${modelo.f1_score}</b> </div>
           </div>`
      })

      dado.modelos_calculados.forEach(modelo => {
        modelos_calculados += 
          `<hr>
           <div class="row text-start" style="margin-top: 3px">
             <div class="col-12"> <b>Modelo: ${modelo.modelo}</b> </div>
             <div class="col-6"> <b>Acurácia: ${modelo.acuracia}</b> </div>
             <div class="col-6"> <b>Precisão: ${modelo.precisao}</b> </div>
             <div class="col-6"> <b>Recall: ${modelo.recall}</b> </div>
             <div class="col-6"> <b>F1-Score: ${modelo.f1_score}</b> </div>
           </div>`
      })

      div.append(`
        <hr>
        <div class="row" style="margin-top: 3px">
          <div class="col-12">
            <h4><b>Iteração ${i + 1}</b></h4>
          </div>
          
          <hr>

          <div class="col-12 text-start">
            <h5><b>Notícias selecionadas </b></h5>
          </div>
          
          ${noticias}

          <hr>

          <div class="col-12 text-start">
            <h5><b>Categorização com SBERT </b></h5>
          </div>

          <hr>

          <div class="col-12 text-start">
            <b> Limiar: ${dado.limiar.replace('.',',')} | Margem: ${dado.margem.replace('.',',')} | Limiar ajustado: ${dado.limiar_ajustado.replace('.',',')}</b>
            <br>
            <b> Acurácia: ${dado.acuracia.replace('.',',')}</b> | <b> Precisão: ${dado.precisao.replace('.',',')}</b>
            <br>
            <b> Recall: ${dado.recall.replace('.',',')}</b> | <b> F1-Score: ${dado.f1_score.replace('.',',')}</b>
          </div>

          <hr>

          <div class="col-12 text-start">
            <h5><b>Classificação com Aprendizado de Máquina (com base rotulada) </b></h5>
          </div>

          <hr>

          ${modelos_calculados}

          <div class="col-12 text-start">
            <h5><b>Classificação com base real (rotulada manualmente) </b></h5>
          </div>

          <hr>

          ${modelos_reais}

        </div>
      `)
    })
    modal_historico.modal("show")
  }

  const montar_classificacoes = classificacoes => {
    tabela_processamento.clear()

    classificacoes.forEach(noticia => {
      let analise = ``
      if (noticia.rotulo == 'REAL') {
        analise = noticia.classificacao_limiar == 'REAL'? 'CORRETO POSITIVO' : 'INCORRETO NEGATIVO'
      } else if (noticia.rotulo == 'FALSA') {
        analise = noticia.classificacao_limiar == 'FALSA'? 'CORRETO NEGATIVO' : 'INCORRETO POSITIVO'
      }
      
      tabela_processamento.row.add([
        noticia.id, noticia.site, noticia.titulo, 
        noticia.rotulo, noticia.classificacao_limiar,
        `<button class="btn btn-secondary ver_pontuacoes" value="${noticia.id}">Ver</button>`,
        analise
      ])
    })

    tabela_processamento.draw()
  }

  const carregar_pontuacoes = noticia => {
    fetch(`/processamento/carregar_pontuacoes/${processamento.projeto_id}?id_processamento=${processamento.id}&noticia=${noticia}`)
    .then(response => {
      if (!response.ok) {
        console.log(response)
        throw new Error("Um erro aconteceu as pontuações!")
      } else {
        return response.json()
      }
    })
    .then(data => {
      montar_pontuacoes(data)
      toggle_botoes(true)
    })
    .catch((error) => {
      aviso(false, error)
    })
  }

  const montar_pontuacoes = pontuacoes => {
    let div = modal_pontuacoes.find(".modal-body")
    div.empty()

    if (pontuacoes.length == 0) {
      div.append("As pontuações não foram encontradas!")
    }

    pontuacoes.forEach(pontuacao => {
      div.append(`
        <div class="row text-start">
          <div class="col-12"><b>Id:</b> ${pontuacao.id}</div>
          <div class="col-12"><b>Site:</b> ${pontuacao.site}</div>
          <div class="col-12"><b>Titulo:</b> ${pontuacao.noticia}</div>
          <div class="col-12"><b>Pontuação:</b> ${pontuacao.pontuacao.replace('.',',')}</div>
        </div>
        <hr>
      `)
    })
  
    $(".loader").remove()
    $(".ver_pontuacoes").prop("disabled", false)
    modal_pontuacoes.modal("show")
  }

  const aviso = (ok, msg, reload = false) => {
    if (ok) {
      modal_alertavel.find(".modal-title").text("Aviso")
      modal_alertavel.find(".modal-header").removeClass('alert alert-danger').addClass("alert alert-success")
    } else {
      modal_alertavel.find(".modal-title").text("Erro")
      modal_alertavel.find(".modal-header").removeClass('alert alert-success').addClass("alert alert-danger")
    }

    modal_alertavel.find(".modal-body").html(msg)
    modal_alertavel.modal("show")

    if (reload) {
      modal_alertavel.on('hidden.bs.modal', function (e) {
        window.location.reload()
      })
    }

    toggle_botoes(true)
  }

  const toggle_botoes = liberar => {
    if (!liberar) {
      btn_historico_processamento.attr("disabled", true)
      btn_executar_processamento.attr("disabled", true)
      btn_executar_processamento.parent().append($('<span class="loader">'))
    } else {
      btn_historico_processamento.removeAttr("disabled")
      btn_executar_processamento.removeAttr("disabled")
      $(".loader").remove()
    }
  }
  
  $(document).on("click", ".check_noticias", function(){
    let noticia_id = $(this).val()

    if (noticia_id in processamento.noticias_selecionadas) {
      delete processamento.noticias_selecionadas[noticia_id]
    } else {
      let row = $(this).parent().parent().parent()


      processamento.noticias_selecionadas[noticia_id] = {
        id: noticia_id, site: '', titulo: ''
      }
    }
  })

  $(document).on("click", "#ver_modal_matriz_confusao", function(){
    modal_matriz_confusao.modal("show")
  })

  $(document).on("click", ".ver_pontuacoes", function(){
    $(".ver_pontuacoes").attr("disabled")
    $(this).parent().append($('<span class="loader">'))
    carregar_pontuacoes($(this).val())
  })
})