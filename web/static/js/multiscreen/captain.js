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

var calib=false;

$('#calibrate_btn').click(function() {
  if(calib)
  {
    calib=false;
    $('#calibrate_btn').html('Калибровка');
    socket.emit('multiscreen_set_calibrate_stop');
  }
  else
  {
    calib=true;
    $('#calibrate_btn').html('Остановить калибровку');
    socket.emit('multiscreen_set_calibrate');
  }
});

var play=false;

$('#show_res').click(function() {
  if(play)
  {
    play=false;
    $('#show_res_img').attr('src','/static/play.png');
    socket.emit('multiscreen_set_pause');
  }
  else
  {
    play=true;
    $('#show_res_img').attr('src','/static/pause.png');
    socket.emit('multiscreen_set_show', ROOM_ID);
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
  socket.emit('multiscreen_set_stop');
  drop_state();
});

$('#refresh_btn').click(function() {
  socket.emit('multiscreen_refresh');
  drop_state();
});
