jQuery(function($) {
  var socketUrl = location.protocol + '//' + location.host;
  socket = io.connect(socketUrl);
  socket.on('update', function(msg) {
    $("#countUsers").html("Количество участников: " + msg);
  });
  socket.on('connect', function() {
    socket.emit('join', ROOM_ID, socket.id);
  });
  socket.on('disconnect', function() {
    socket.emit('leave', ROOM_ID);
  });
});

$('#calibrate_btn').click(function() {
  if($('#calibrate_btn').hasClass('video-control__btn_disabled')==false)
  {
    socket.emit('multiscreen_set_calibrate', ROOM_ID);
  }
});


$('#image_form').on('submit', function(e) {
    $('#formMssg').deleteClass('correct');
    e.preventDefault();
    if ($('#image').val() == '') {
        $('#formMssg').html('Файл не выбран');
        return;
    }
    var imageExtension =  $('#image').val()
            .split('.')
            .pop()
            .toLowerCase();
    if ( !['jpg', 'jpeg'].includes(imageExtension) ) {
        $('#formMssg').html('Неправильное расширение (должно быть jpeg или jpg)');
        return;
    }

    var form_data = new FormData();
    form_data.append('image', $('#image')[0].files[0]);

    $.ajax({
        data: form_data,
        processData: false,
        type: 'POST',
        contentType: false,
        dataType: 'json',
        success: function(data) {
            if (data.status) {
                $('#formMssg').deleteClass('error');
                $('#formMssg').addClass('correct');
                $('#formMssg').html('Фотография загружена');
                $('#map').show();
                $('#map').attr('src', data.map_url);
            }
            else {
                 $('#formMssg').html('Мы не смогли идентифицировать устройства, попробуйте загрузить другую фотографию.');
            }
        },
        error: function(textStatus) {
            $('#formMssg').html(textStatus.status + ' ' + textStatus.statusText);
        }
    });
});


$('#show_res').click(function() {
  if($('#show_res').hasClass('video-control__btn_disabled')==false)
  {
    if(play)
    {
      play=false;
      $('#show_res_img').removeClass('fa-pause');
      $('#show_res_img').addClass('fa-play');
      $('#calibrate_btn').removeClass('video-control__btn_disabled');
      socket.emit('multiscreen_set_pause', ROOM_ID);
    }
    else
    {
      play=true;
      $('#show_res_img').removeClass('fa-play');
      $('#show_res_img').addClass('fa-pause');
      $('#calibrate_btn').addClass('video-control__btn_disabled');
      socket.emit('multiscreen_set_show', ROOM_ID);
    }
  }
});

function drop_state()
{
  if(play)
  {
    $('#show_res').click();
  }
}

$('#stop_res').click(function() {
  if($('#stop_res').hasClass('video-control__btn_disabled')==false)
  {
    socket.emit('multiscreen_set_stop', ROOM_ID);
    drop_state();
  }
});

$('#refresh_btn').click(function() {
  socket.emit('multiscreen_refresh', ROOM_ID);
  drop_state();
});
