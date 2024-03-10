$(document).ready(function(){
  $.extend( $.fn.dataTable.defaults, {
    responsive: true,
    autoWidth: false,
    lengthMenu: [[10, 20, 25, 50, -1],[10, 20, 25, 50, "TODOS"]],
    pageLength: 10,
  });
  
  const tabela_noticias = new DataTable("#tabela_noticias",{fixedHeader: true})
  const tabela_processamento1 = new DataTable("#tabela_processamento1",{fixedHeader: true})
  const tabela_processamento2 = new DataTable("#tabela_processamento2",{fixedHeader: true})

  const modal_historico = $("#modal_historico")
 
  const input_id_processamento = $("#id_processamento")
  const input_salvar_noticias = $("#salvar_noticias")
  const csrf_token = $("#csrf_token").val()

  /* Variavel de controle de processamento */
  const processamento = {
    id: '',
    projeto_id: $("#projeto_id").val(),
    noticias_reais: [],
    noticias_falsas: []
  }

  const modal_alertavel = $("#alertavel").on('hidden.bs.modal', function (e) {
    modal_historico.removeClass("modal-backdrop")
  })

  const btn_executar_processamento = $("#executar_processamento").click(function(){
    $('.check_noticias').each(function(i,val){
      if ($(val).is(":checked")) {
        if(!processamento.noticias_reais.includes(val.value)) {
          processamento.noticias_reais.push(val.value)
        }
      } else {
        if(!processamento.noticias_falsas.includes(val.value)) {
          processamento.noticias_falsas.push(val.value)
        }
      }
    })

    if (processamento.noticias_reais.length == 0) {
      aviso(false, "Select one or more records!")
    } else {
      toggle_botoes(false)
      executar_processamento()
    }
  })

  const btn_historico_processamento = $("#historico_processamento").click(function(){
    toggle_botoes(false)
    carregar_historico()
  })

  const btn_carregar_noticias = $("#carregar_noticias").click(function(){
    $('.check_noticias').each(function(i,val){
      if ($(val).is(":checked")) {
        if(!processamento.noticias_reais.includes(val.value)) {
          processamento.noticias_reais.push(val.value)
        }
      } else {
        if(!processamento.noticias_falsas.includes(val.value)) {
          processamento.noticias_falsas.push(val.value)
        }
      }
    })

    toggle_botoes(false)
    carregar_noticias(processamento.noticias_reais.concat(processamento.noticias_falsas))

    //Se for o primeiro processamento e não houve nenhuma noticia real selecionada, ignorar as noticias falsas
    if (processamento.id == null && processamento.noticias_reais.length == 0) {
      processamento.noticias_falsas = []
    }
  })

  const btn_carregar_processamento = $("#carregar_processamento").click(function(){
    if (input_id_processamento.val() != "") {
      processamento.id = input_id_processamento.val()
      input_id_processamento.attr("disabled", true)
      btn_carregar_processamento.attr("disabled", true)

      toggle_botoes(true)
      carregar_noticias([])

    } else {
      aviso(false, "Insert the processing ID!", false)
    }
  })

  const carregar_noticias = (filtrar_noticias) => {
    fetch(`/processamento/buscar_noticias/${processamento.projeto_id}?filtrar_noticias=${filtrar_noticias}&id_processamento=${processamento.id}`)
    .then(response => {
      if (!response.ok) {
        console.log(response)
        throw new Error("An error happened during the execution!")
      } else {
        return response.json()
      }
    })
    .then(data => {
      montar_noticias(data)
      toggle_botoes(true)
    })
    .catch((error) => {
      aviso(false, error)
    })
  }

  const executar_processamento = () => {    
    let conf = {
      method: "POST",  
      headers: {"Content-Type": "application/json", 'X-CSRFToken': csrf_token},
      mode: 'same-origin',
      body: JSON.stringify({
        id_processamento: processamento.id,
        noticias_reais: processamento.noticias_reais,
        noticias_falsas: processamento.noticias_falsas,
        salvar_noticias: input_salvar_noticias.is(':checked')? 'S':'N'
      })
    }

    fetch(`/processamento/executar_processamento/${processamento.projeto_id}`, conf)
    .then(response => {
      if (!response.ok) {
        try{
          return response.json()
        } catch(e) {
          throw new Error("An error happened during the execution!")
        }
      } else {
        return response.json()
      }
    })
    .then(data => {

      if (data.erro) {
        aviso(false, data.erro)
      } else {
        processamento.id = data.resultados.id_processamento
        input_id_processamento.val(processamento.id)
        input_id_processamento.attr("disabled", true)
        btn_carregar_processamento.attr("disabled", true)

        montar_classificacoes(data.classificacoes)
        montar_resultado_atual(data.resultados)

        let msg = 
          `Execution completed!<br>
          Start time: ${data.tempo.inicio}<br>
          End time: ${data.tempo.fim}<br>
          Time (minutes): ${data.tempo.diff_minutos}<br>
          Time (seconds): ${data.tempo.diff_segundos}`

        aviso(true, msg)
        toggle_botoes(true)
      }

    })
    .catch((error) => {
      aviso(false, error)
    })
  }

  const montar_resultado_atual = resultados => {

    const montar = (div, arr, montar_matriz) => {
      arr.forEach(modelo => {
        div.append(`
          <hr>
          <div class="row" style="margin-top: 3px">
            <div class="col-12"> <b>Model: ${modelo.modelo}</b> </div>
            <div class="col-6"> <b>Accuracy: ${modelo.acuracia}</b> </div>
            <div class="col-6"> <b>Precision: ${modelo.precisao}</b> </div>
            <div class="col-6"> <b>Recall: ${modelo.recall}</b> </div>
            <div class="col-6"> <b>F1-Score: ${modelo.f1_score}</b> </div>
            ` + 
             ((montar_matriz)? 
             `<button class="btn btn-secondary ver_matriz" value=${modelo.imagem}>Matrix</button>`:
             `<div class="col-6"> <b>TP: ${modelo.vp}</b> </div>
              <div class="col-6"> <b>TN: ${modelo.vn}</b> </div>
              <div class="col-6"> <b>FP: ${modelo.fp}</b> </div>
              <div class="col-6"> <b>FN: ${modelo.fn}</b> </div>` )
            + `
          </div>
        `)
      })
    }

    let div_metricas_rotulos_reais = $("#div_metricas_rotulos_reais")
    div_metricas_rotulos_reais.empty().append(`
      <div class="col-12 text-start" style="margin-top: 5px;">
        <button class="btn btn-secondary" type="button" data-bs-toggle="collapse" data-bs-target="#modelos_metricas_reais" aria-expanded="false">
          Real metrics
        </button>
      </div>
      <div id="modelos_metricas_reais" class="col-12 collapse"></div>
    `)
    montar($("#modelos_metricas_reais"), resultados.modelos_metricas_reais, true)

    let div_metricas_rotulos_calculados = $("#div_metricas_rotulos_calculados")
    div_metricas_rotulos_calculados.empty().append(`
      <div class="col-12 text-start" style="margin-top: 5px;">
        <button class="btn btn-secondary" type="button" data-bs-toggle="collapse" data-bs-target="#modelos_rotulos_calculados" aria-expanded="false">
          Calculated metrics
        </button>
      </div>
      <div id="modelos_rotulos_calculados" class="col-12 collapse"></div>
    `)
    montar($("#modelos_rotulos_calculados"), resultados.modelos_rotulos_calculados, false)

    let div_totais_atual = $("#div_totais_atual")
    div_totais_atual.empty()

    div_totais_atual.append(`
      <div class="col-12" style="margin-top: 5px;">
        <b> Accuracy: ${resultados.acuracia.replace('.',',')}</b> | <b> Precision: ${resultados.precisao.replace('.',',')}</b>
        <br>
        <b> Recall: ${resultados.recall.replace('.',',')}</b> | <b> F1-Score: ${resultados.f1_score.replace('.',',')}</b>
      </div>
    `)
  }

  const montar_noticias = noticias => {
    tabela_noticias.clear()

    noticias.forEach(noticia=> {
      tabela_noticias.row.add([
        noticia.id, noticia.site, noticia.titulo,
        `<a class="btn btn-info btn-sm" href="${noticia.url}" target="_blank">Link</a>`,
        `<div class="btn-group" role="group">
          <input type="checkbox" class="btn-check check_noticias" name="noticias" value="${noticia.id}" id="noticia_check_${noticia.id}" autocomplete="off">
          <label class="btn btn-outline-primary spc_label" for="noticia_check_${noticia.id}">Select</label>
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
        throw new Error("An error happened during the execution!")
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
      div.append("No records were found!")
    }

    dados.forEach((dado, i) => {
      let modelos_reais = ''
      let modelos_calculados = ''
      let noticias = ''

      dado.noticias.forEach(noticia => {
        noticias += 
          `<hr>
           <div class="row text-start" style="margin-top: 3px">
             <div class="col-12"> <b>ID: ${noticia.id}</b> </div>
             <div class="col-12"> <b>Site: ${noticia.site}</b> </div>
             <div class="col-12"> <b>Title: ${noticia.titulo}</b> </div>
             <div class="col-12"> <b>Is real news?: ${noticia.tipo}</b> </div>
           </div>`
      })

      dado.modelos_reais.forEach(modelo => {
        modelos_reais += 
          `<hr>
           <div class="row text-start" style="margin-top: 3px">
             <div class="col-12"> <b>Model: ${modelo.modelo}</b> </div>
             <div class="col-6"> <b>Accuracy: ${modelo.acuracia}</b> </div>
             <div class="col-6"> <b>Precision: ${modelo.precisao}</b> </div>
             <div class="col-6"> <b>Recall: ${modelo.recall}</b> </div>
             <div class="col-6"> <b>F1-Score: ${modelo.f1_score}</b> </div>
             <button class="btn btn-secondary ver_matriz" value=${modelo.imagem}>Matrix</button>
           </div>`
      })

      dado.modelos_calculados.forEach(modelo => {
        modelos_calculados += 
          `<hr>
           <div class="row text-start" style="margin-top: 3px">
             <div class="col-12"> <b>Model: ${modelo.modelo}</b> </div>
             <div class="col-6"> <b>Accuracy: ${modelo.acuracia}</b> </div>
             <div class="col-6"> <b>Precision: ${modelo.precisao}</b> </div>
             <div class="col-6"> <b>Recall: ${modelo.recall}</b> </div>
             <div class="col-6"> <b>F1-Score: ${modelo.f1_score}</b> </div>
             <div class="col-6"> <b>TP: ${modelo.vp}</b> </div>
             <div class="col-6"> <b>TN: ${modelo.vn}</b> </div>
             <div class="col-6"> <b>FP: ${modelo.fp}</b> </div>
             <div class="col-6"> <b>FN: ${modelo.fn}</b> </div>
           </div>`
      })

      div.append(`
        <hr>
        <div class="row" style="margin-top: 3px">
          <div class="col-12">
            <h4><b>Iteration ${i + 1}</b></h4>
          </div>
          
          <hr>

          <div class="col-12 text-start">
            <h5><b>Selected news </b></h5>
          </div>
          
          ${noticias}

          <hr>

          <div class="col-12 text-start">
            <b> Accuracy: ${dado.acuracia}</b> | <b> Precision: ${dado.precisao}</b>
            <br>
            <b> Recall: ${dado.recall}</b> | <b> F1-Score: ${dado.f1_score}</b>
          </div>

          <hr>

          <div class="col-12 text-start">
            <h5><b>Classification with training data</b></h5>
          </div>
          
          ${modelos_calculados}

          <hr>

          <div class="col-12 text-start">
            <h5><b>Classification with real data </b></h5>
          </div>

          ${modelos_reais}

        </div>
      `)
    })
    modal_historico.modal("show")
  }

  const montar_classificacoes = classificacoes => {
    tabela_processamento1.clear()
    tabela_processamento2.clear()

    let totais = {'VP': 0, 'FN': 0, 'VN': 0, 'FP': 0}

    classificacoes.forEach(noticia => {
      let analise = ``
      if (noticia.rotulo == 'REAL') {
        analise = noticia.classificacao == 'REAL'? 'VP' : 'FN'
      } else if (noticia.rotulo == 'FALSA') {
        analise = noticia.classificacao == 'FALSA'? 'VN' : 'FP'
      }

      totais[analise]++

      let linha = [
        noticia.id, noticia.site, noticia.titulo, `<a class="btn btn-info btn-sm" href="${noticia.url}" target="_blank">Link</a>`,
        noticia.pontuacao_real, noticia.pontuacao_nao_real, analise, noticia.classificadores
      ]
      
      if (noticia.classificacao == 'REAL') {
        tabela_processamento1.row.add(linha)
      } else {
        tabela_processamento2.row.add(linha)
      }
    })

    tabela_processamento1.draw()
    tabela_processamento2.draw()

    let div = $("#div_totais_analise")
    div.html(`
      <div class="col-12" style="margin-top: 5px;">
        <b> TP: ${totais['VP']}</b> | <b> FN: ${totais['FN']}</b>
        <br>
        <b> TN: ${totais['VN']}</b> | <b> FP: ${totais['FP']}</b>
      </div>
    `)
  }

  const aviso = (ok, msg, reload = false) => {
    if (ok) {
      modal_alertavel.find(".modal-title").text("Success")
      modal_alertavel.find(".modal-header").removeClass('alert alert-danger').addClass("alert alert-success")
    } else {
      modal_alertavel.find(".modal-title").text("Warning")
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
      btn_executar_processamento.attr("disabled", true)
      btn_historico_processamento.attr("disabled", true)
      btn_carregar_noticias.attr("disabled", true)
      btn_carregar_noticias.parent().append($('<span class="loader">'))
    } else {
      btn_executar_processamento.removeAttr("disabled")
      btn_historico_processamento.removeAttr("disabled")
      btn_carregar_noticias.removeAttr("disabled")
      $(".loader").remove()
    }
  }

  $(document).on("click", ".ver_matriz", function(){
    var image = new Image();
    image.src = $(this).val();

    var w = window.open("",'targetWindow', `toolbar=no,location=no,status=no,menubar=no,scrollbars=yes,resizable=yes,width=750, height=750`);
    w.document.write(image.outerHTML);
  })

  btn_carregar_noticias.trigger("click")
})