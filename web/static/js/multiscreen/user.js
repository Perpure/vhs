var PLAYER;
if(YT_VID)
{
  var tag = document.createElement('script');

  tag.src = "https://www.youtube.com/iframe_api";
  var firstScriptTag = document.getElementsByTagName('script')[0];
  firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

  function onYouTubeIframeAPIReady() {
      PLAYER = new YT.Player('ReVi');
  }
}

function Result() {
  $('#ReShell').show();
  if(YT_VID)
  {
      PLAYER.playVideo();
  }
  else
  {
      $('#ReVi').get(0).play();
  }
  $('#ReVi').on('ended',function(){
      $('#ReShell').hide();
  });
}

jQuery(function($) {
  socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
  socket.on('multiscreen_show_calibrate', function() {
    $('#Body').append('<div '
        + 'style="' + 'background:' + ROOM_COLOR + ';" '
        + 'class="calibration-image fullscreen-switcher"></div>');
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
    if(YT_VID)
    {
        PLAYER.pauseVideo();
    }
    else
    {
        $('#ReVi').get(0).pause();
    }
  });
  socket.on('multiscreen_show_stop', function() {
    $('#ReShell').hide();
    if(YT_VID)
    {
        PLAYER.stopVideo();
    }
    else
    {
        $('#ReVi').get(0).currentTime=0;
    }
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
