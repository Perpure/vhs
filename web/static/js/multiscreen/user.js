var PLAYER;

if(from_youtube) {
  var tag = document.createElement('script');

  tag.src = "https://www.youtube.com/iframe_api";
  var firstScriptTag = document.getElementsByTagName('script')[0];
  firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

  function onYouTubeIframeAPIReady() {
      PLAYER = new YT.Player('ResultVideo',{
          events: {
              onStateChange: function(event) {
                  if(event.data == 0) {
                      $('#ResultVideoShell').hide();
                      if ( !PLAYER.isMuted() ) {
                          socket.emit('ended', ROOM_ID);
                      }
                  }
              }
          }
      });
  }
} else {
  PLAYER = {
      el: $('#ResultVideo').get(0),
      elJQ: $('#ResultVideo'),
      stopVideo: function() {
          this.el.currentTime = 0;
      },
      pauseVideo: function() {
          this.el.pause();
      },
      playVideo: function() {
          this.el.play();
          this.elJQ.on('ended',function(){
              $('#ResultVideoShell').hide();
              if( !this.muted ) {
                  socket.emit('ended', ROOM_ID);
              }
          });
      },
      mute: function() {
          this.el.muted = true;
      }
  }
}

jQuery(function($) {
  socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
  socket.on('multiscreen_show_calibrate', function() {
    $('#Body').append('<div '
        + 'style="' + 'background:' + ROOM_COLOR + ';" '
        + 'class="calibration-image fullscreen-switcher"></div>');
  });
  socket.on('multiscreen_show_result', function(response) {
    $('#ResultVideo').css({
        top: screen.height * (response.top / response.scale) + "px",
        left: screen.width * (response.left / response.scale) + "px",
        width: response.scale + "%"
    });
    if(response.noSound) {
      PLAYER.mute();
    }
    $('#ResultVideoShell').show();
    PLAYER.playVideo();
  });
  socket.on('multiscreen_show_pause', function() {
      PLAYER.pauseVideo();
  });
  socket.on('multiscreen_show_stop', function() {
      $('#ResultVideoShell').hide();
      PLAYER.stopVideo();
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
