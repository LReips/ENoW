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

  const projeto_id = $("#projeto_id").val()
  const tabela_noticias_processadas = new DataTable("#tabela_noticias_processadas",{fixedHeader: true})
  const tabela_noticias_duplicadas = new DataTable("#tabela_noticias_duplicadas",{fixedHeader: true})
  
  const modal_alertavel = $("#alertavel")

  const btn_gerar_csv_sbert = $("#gerar_csv_sbert").click(function(){
    toggle_botoes(false)
    download_csv_sbert()
  });

  const toggle_botoes = liberar => {
    if (!liberar) {
      let span = $('<span class="loader">')
      btn_gerar_csv_sbert.attr("disabled", true)
      btn_gerar_csv_sbert.parent().append(span)
    } else {
      btn_gerar_csv_sbert.removeAttr("disabled")
      $(".loader").remove()
    }
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

    toggle_botoes(true)
  }

  const download_file = file => {
    var file_path = file;
    var a = document.createElement('A');
    a.href = file_path;
    a.download = file_path.substr(file_path.lastIndexOf('/') + 1);
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  }

  const download_csv_sbert = () => {
    fetch(`../../processamento/gerar_csv_sbert/${projeto_id}`)
    .then(response => {
      if (!response.ok) {
        console.log(response)
        throw new Error("Um erro aconteceu ao gerar o CSV!")
      } else {
        return response.json()
      }
    })
    .then(data => {
      toggle_botoes(true)
      download_file(`../../processamento/download?arquivo=${data.arquivo}`)
      aviso(true, "Download finalizado!")
    })
    .catch((error) => {
      aviso(false, error)
    })
  }

  const deletar_noticia_processada = id => {
    let conf = {
      method: "DELETE",  
      headers: {"Content-Type": "application/json", 'X-CSRFToken': csrf_token},
      mode: 'same-origin'
    }
    fetch(`../../processamento/deletar_noticia/${id}`, conf)
    .then(response => {
      if (!response.ok) {
        console.log(response)
        throw new Error("Um erro aconteceu ao deletar a noticia!")
      } else {
        return response.json()
      }
    })
    .then(data => {
      aviso(true, "Noticia deletada!", true)
    })
    .catch((error) => {
      aviso(false, error)
    })
    .finally(() => {
      $(".deletar_noticia_processada").removeAttr("disabled")
      $(".loader").remove()
    })
  }

  $(".deletar_noticia_processada").click(function() {
    if(confirm("Deseja realmente deletar esta noticia processada?")) {
      let span = $('<span class="loader">')
      $(".deletar_noticia_processada").attr("disabled", true)
      $(this).parent().append(span)
      
      deletar_noticia_processada($(this).val())
    }
  })

})