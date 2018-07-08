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
  if($('#calibrate_btn').hasClass('video-control_btn__disabled')==false)
  {
    socket.emit('multiscreen_set_calibrate', ROOM_ID);
  }
});

var play=false;

$('#show_res').click(function() {
  if($('#show_res').hasClass('video-control_btn__disabled')==false)
  {
    if(play)
    {
      play=false;
      $('#show_res_img').attr('src','/static/play.png');
      $('#calibrate_btn').removeClass('video-control_btn__disabled');
      socket.emit('multiscreen_set_pause', ROOM_ID);
    }
    else
    {
      play=true;
      $('#show_res_img').attr('src','/static/pause.png');
      $('#calibrate_btn').addClass('video-control_btn__disabled');
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
  if($('#stop_res').hasClass('video-control_btn__disabled')==false)
  {
    socket.emit('multiscreen_set_stop', ROOM_ID);
    drop_state();
  }
});

$('#refresh_btn').click(function() {
  socket.emit('multiscreen_refresh', ROOM_ID);
  drop_state();
});
