var PLAYER,
    PICTURE_SIZE = 16 / 9;

if(from_youtube) {
  var tag = document.createElement('script');
  var yt_video_id = $('#ResultVideoShell').data('yt-video-id');

  tag.src = "https://www.youtube.com/iframe_api";
  var firstScriptTag = document.getElementsByTagName('script')[0];
  firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

  function onYouTubeIframeAPIReady() {
      PLAYER = new YT.Player('ResultVideo',{
          videoId: yt_video_id,
          playerVars: {
              controls: 0,
              disablekb: 1,
              fs: 0,
              enablejsapi: 1,
              rel: 0,
              showinfo: 0,
              modestbranding: 1
          },
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
    var videoShell = $('#ResultVideoShell')
        video = $('#ResultVideo');
    // TODO надо убрать отсюда математику. Все должно вычисляться на сервере и в пикселях
    video.css({
        top: screen.height * response.top / response.scale + "px",
        left: screen.width * response.left / response.scale + "px",
        width: response.scale + "%",
        height: screen.width * response.scale / PICTURE_SIZE / 100 + "px"
    });
    if(response.noSound) {
      PLAYER.mute();
    }
    videoShell.show();
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
  $.ajax({
    url: '/tellRes',
    type: "POST",
    dataType:"json",
    data: {
        width: screen.width * ratio,
        height: screen.height * ratio
    }
  });
});
