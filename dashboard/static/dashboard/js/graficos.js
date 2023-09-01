$(document).ready(function(){
  const projeto_id = $("#projeto_id").val()
  const div_graficos = $("#div_graficos")

  const modal_alertavel = $("#alertavel")

  const buscar_noticias = () => {
    fetch(`../${projeto_id}/pontuacoes`)
    .then(response => {
      if (!response.ok) {
        console.log(response)
        throw new Error("Um erro aconteceu ao carregar as notícias!")
      } else {
        return response.json()
      }
    })
    .then(data => {
      montar_graficos_distribuicao(data)
    })
    .catch((error) => {
      aviso(false, error)
    })
  }

  const montar_graficos_distribuicao = dados => {
    
    dados.forEach((processamento, i) => {
      div_graficos.append(`
        <div class="col-6">
          <canvas id="g_distribuicao_${i}"></canvas>
        </div>`)
 
        grafico_distribuicao(`g_distribuicao_${i}`, processamento)
    })

  }

  const grafico_distribuicao = (id, dados) => {
    let dados_prep = {'reais': [], 'falsas': [], 't1': 0, 't2': 0}

    for(pontuacao in dados.reais) {
      dados_prep.reais.push({
        'x': pontuacao,
        'y': dados.reais[pontuacao]
      })

      dados_prep.t1 += dados.reais[pontuacao]
    }

    for(pontuacao in dados.falsas) {
      dados_prep.falsas.push({
        'x': pontuacao,
        'y': dados.falsas[pontuacao]
      })

      dados_prep.t2 += dados.falsas[pontuacao]
    }


    const data = {
      datasets: [
        {
          label: `Notícias reais (${dados_prep.t1})`,  backgroundColor: 'green',
          data: dados_prep.reais
        },
        {
          label: `Notícias falsas (${dados_prep.t2})`, backgroundColor: 'red',
          data: dados_prep.falsas
        }
      ]
    };
   
    const myChart = new Chart(
      document.getElementById(id), 
      {
        type: 'scatter',
        data: data,
        options: {
          responsive: true,
          scales: {
            x: {
              type: 'linear',
              position: 'bottom',
              title: {
                display: true,
                text: 'Aproximação de noticia real'
              }
            },
            y: {
              title: {
                display: true,
                text: 'Quantidade de notícias'
              }
            }
          },
          plugins: {
            legend: {
              position: 'top',
            },
            subtitle: {
              display: true,
              text: `${dados.noticia_referencia} | ${dados.nota_corte}`
            },
            title: {
              display: true,
              text: `Gráfico de distribuição`
            }
          }
        },
      }
    )
  }

  const aviso = (ok, msg) => {
    if (ok) {
      modal_alertavel.find(".modal-title").text("Aviso")
      modal_alertavel.find(".modal-header").removeClass('alert alert-danger').addClass("alert alert-success")
    } else {
      modal_alertavel.find(".modal-title").text("Erro")
      modal_alertavel.find(".modal-header").removeClass('alert alert-success').addClass("alert alert-danger")
    }

    modal_alertavel.find(".modal-body").html(msg)
    modal_alertavel.modal("show")
  }
  
  buscar_noticias()
})