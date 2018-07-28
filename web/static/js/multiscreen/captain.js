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
    $('.error').remove();
    e.preventDefault();
    if ($('#image').val() == '') {
        $('#image_form').after('<p class="error" style="color: red;">Файл не выбран</p>');
        return '';
    }
    if (!(['jpg', 'jpeg'].includes($('#image').val().split('.').pop().toLowerCase()))) {
        $('#image_form').after('<p class="error" style="color: red;">Неправильное расширение (должно быть jpeg или jpg)</p>');
        return '';
    }

    var form_data = new FormData();
    form_data.append('image', $('#image')[0].files[0]);

    $.ajax("", {
        data: form_data,
        processData: false,
        type: 'POST',
        contentType: false
    }).done(function(data, textStatus) {
    var extrc_data = JSON.parse(data);
        if (extrc_data.status == 'OK') {
            $('#image_form').hide();
            $('#image_form').after('<p style="color: green;">Фотография загружена</p>');
            $('#map').src = extrc_data.map_url;
        }
        else {
             $('#image_form').after('<p class="error" style="color: red;">' + extrc_data.status + '</p>');
        }
    }).fail(function(textStatus) {
        $('#image_form').after('<p class="error" style="color: red;">Ошибка: ' + textStatus.status + ' ' + textStatus.statusText + '</p>');

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
