$(document).ready(function() {
  const modal_alertavel = $("#alertavel")

  const aviso = (ok, msg, projeto = null) => {
    if (ok) {
      modal_alertavel.find(".modal-title").text("Aviso")
      modal_alertavel.find(".modal-header").removeClass('alert alert-danger').addClass("alert alert-success")

      modal_alertavel.on('hidden.bs.modal', function (e) {
        window.location.href = `../dashboard/projeto/${projeto}`
      })
    } else {
      modal_alertavel.find(".modal-title").text("Erro")
      modal_alertavel.find(".modal-header").removeClass('alert alert-success').addClass("alert alert-danger")
    }

    modal_alertavel.find(".modal-body").html(msg)
    modal_alertavel.modal("show")
  }

  const executar_coleta = (projeto, palavra_chave) => {
    fetch(`executar_coleta/${projeto}/${palavra_chave}`)
    .then(response => {
      if (!response.ok) {
        console.log(response)
        throw new Error("Um erro aconteceu na coleta!")
      } else {
        return response.json()
      }
    })
    .then(data => {

      let sites_erros = ''
      if (data.sites_erros.length != 0) {
        sites_erros = 'Os seguintes sites podem ter alterado sua estrutura HTML, favor verificar: <br>' + data.sites_erros.join(', ')
      }

      let msg = 
        `Coleta finalizada!<br>
         Inicio: ${data.tempo.inicio}<br>
         Fim: ${data.tempo.fim}<br>
         Tempo (minutos): ${data.tempo.diff_minutos}<br>
         Tempo (segundos): ${data.tempo.diff_segundos}
         <br>
         <br>
         ${sites_erros}`
      aviso(true, msg, projeto)
    })
    .catch((error) => {
      aviso(false, error)
    })
    .finally(() => {
      liberar_projetos()
    })
  }

  const liberar_projetos = () => {
    $(".coletar_btn, .processar_noticias").removeAttr("disabled")
    $(".loader").remove()
  }

  const travar_projetos = obj => {
    let span = $('<span class="loader">')
    $(".coletar_btn, .processar_noticias").attr("disabled", true)
    obj.parent().append(span)
  }

  $(".coletar_btn").click(function(){
    travar_projetos($(this))
    executar_coleta($(this).attr('data-projeto'), $(this).attr("data-palavra_chave")??0)
  });

});