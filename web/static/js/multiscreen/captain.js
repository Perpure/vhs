jQuery(function($) {
  socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
  socket.on('update', function(msg) {
    $("#countUsers").html("Количество участников: "+msg);
  });
  socket.on('connect', function() {
    socket.emit('join', ROOM_ID, socket.id);
  });
  socket.on('disconnect', function() {
    socket.emit('leave', ROOM_ID);
  });
});

$('#calibrate_btn').click(function() {
  socket.emit('multiscreen_set_calibrate', {
    room: ROOM_ID
  });
});

$('#showRes').click(function() {
  socket.emit('multiscreen_set_show', ROOM_ID);
});
