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

function change_youtube_state()
{
    $.ajax({
        url: "/change_youtube_state/" + ROOM_ID,
        type: "GET",
        dataType: "text"
    });
}

jQuery(function($) {
  if(FROM_YOUTUBE)
  {
      $('#go_to_youtube').click();
  }

  $('#video_switcher').bind('action', change_youtube_state);
});

var play = false;

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
