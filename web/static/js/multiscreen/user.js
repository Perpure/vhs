function Result() {
  $('#ReShell').show();
  $('#ReVi').get(0).play();
  $('#ReVi').on('ended',function(){
    $('#ReShell').hide();
  });
}

jQuery(function($) {
  socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
  socket.on('multiscreen_show_calibrate', function() {
    $('#Body').append('<img '
        + 'src = "' ROOM_IMAGE '"'
        + 'class="calibration-image fullscreen-switcher"></img>');
  });
  socket.on('multiscreen_show_result', function(response) {
    $('#ReVi').css({
        top: screen.height * (response.top / response.scale) + "px",
        left: screen.width * (response.left / response.scale) + "px",
        width: response.scale + "%"
    });
    if(response.noSound)
    {
      $('#ReVi').get(0).muted=true;
    }
    Result();
  });
  socket.on('multiscreen_show_pause', function() {
    $('#ReVi').get(0).pause();
  });
  socket.on('multiscreen_show_stop', function() {
    $('#ReVi').hide();
    $('#ReVi').get(0).currentTime=0;
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
