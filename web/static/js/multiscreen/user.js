function Result()
{
    $('#Body').css('overflow', 'hidden');
    $('#ReVi').show();
    $('#ReVi').get(0).play();
    $('#ReVi').on('ended',function(){
        $('#ReVi').hide();
        $('#Footer').show();
        $('#Body').css('overflow', 'auto')
    });
    $('#Footer').hide();
}

$(document).ready(function() {
  socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
  socket.on('multiscreen_show_calibrate', function(msg) {
      $('#Body').css('overflow', 'hidden');
      $('#Body').prepend('<div id="calibrImage" style="position:fixed; width:110%; height:110%; ' +
          'background:' + ROOM_COLOR + ';"></div>');
      $('#calibrImage').click(fullscreen);
      $('#Footer').hide();
      $('#Header').hide();
  });
  socket.on('multiscreen_show_result', function(response) {
    setTimeout(Result,wait_time);
    $('#Body').css('overflow', 'hidden');
    $('#ReVi').css({
        top: response.top + "%",
        left: response.left + "%",
        width: response.width+"%",
    });
    $('#ReVi').css({
        top: $('#ReVi').height() * ( response.top / response.width ) + "px",
        left: $('#ReVi').width() * ( response.left / response.width ) + "px",
        width: response.width+"%",
    });
    if(response.noSound)$("#ReVi").prop('muted', true);
    countDown(wait_time/1000);
  });
  socket.on('refresh', function() {
      location.reload();
  });
  socket.on('update', function(msg) {
      $("#countUsers").html(msg);
  });
  socket.on('connect', function() {
      socket.emit('join', ROOM_ID, socket.id);
  });
  socket.on('disconnect', function() {
      socket.emit('leave', ROOM_ID);
  });
});
