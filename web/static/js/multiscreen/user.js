function Result() {
  $('#ReVi').show();
  $('#ReVi').get(0).play();
  $('#ReVi').on('ended',function(){
    $('#ReVi').hide();
  });
}

jQuery(function($) {
  socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
  socket.on('multiscreen_show_calibrate', function(msg) {
    $('#Body').append('<div id="calibrImage" '
        + 'style="' + 'background:' + ROOM_COLOR + ';" '
        + 'class="calibration-image fullscreen-switcher"></div>');
  });
  socket.on('multiscreen_show_result', function(response) {
    $('#Body').css('overflow', 'hidden');
    $('#ReVi').css({
        top: screen.height * (response.top / response.width) + "px",
        left: screen.width * (response.left / response.width) + "px",
        width: response.width + "%"
    });
    if(response.noSound)
    {
      $('#ReVi').get(0).muted=true;
    }
    Result();
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

jQuery(function($) {
  var ratio = window.devicePixelRatio || 1;
  var width = screen.width * ratio;
  var height = screen.height * ratio;
  $.ajax({
    url: '/tellRes',
    contentType: "application/json; charset=utf-8",
    type: "POST",
    dataType:"json",
    data: JSON.stringify({ "width": width, "height" : height }),
    success: function () {
      console.log(JSON.stringify({ "width": width, "height" : height }));},
  });
});
