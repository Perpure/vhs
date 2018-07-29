jQuery(function($) {
  var socketUrl = location.protocol + '//' + location.host;
  socket = io.connect(socketUrl);
  socket.on('update', function(msg) {
    $("#countUsers").html("Количество участников: " + msg);
  });
  socket.on('video_ended', function() {
    drop_state();
  });
  socket.on('connect', function() {
    socket.emit('join', ROOM_ID, socket.id);
  });
  socket.on('disconnect', function() {
    socket.emit('leave', ROOM_ID);
  });

    $('#calibrate_btn').click(function() {
        if( !$('#calibrate_btn').hasClass('video-control__btn_disabled') ) {
            socket.emit('multiscreen_set_calibrate', ROOM_ID);
        }
    });

    function changeVideoMode(videoMode) {
        if (videoMode === "self") {
            $('#choose_site').show();
            $('#choose_yt').hide();
            if($('.video__preview').length == 0) {
                $('#stop_res').addClass('video-control__btn_disabled');
                $('#show_res').addClass('video-control__btn_disabled');
            }
        } else if (videoMode === "youtube") {
            $('#choose_site').hide();
            $('#choose_yt').show();
            $('#stop_res').removeClass('video-control__btn_disabled');
            $('#show_res').removeClass('video-control__btn_disabled');
        }
    }

    if(from_youtube) {
        $('#go_to_youtube').click();
        changeVideoMode('youtube');
    }

    $('#video_switcher').bind('switch', function(e, videoMode) {
        changeVideoMode(videoMode);
        $.ajax({
            url: "/change_youtube_state/" + ROOM_ID,
            type: "GET",
            dataType: "text"
        });
    });


var play = false;

$('#show_res').click(function() {
  if($('#show_res').hasClass('video-control__btn_disabled') == false)
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
  if($('#stop_res').hasClass('video-control__btn_disabled') == false)
  {
    socket.emit('multiscreen_set_stop', ROOM_ID);
    drop_state();
  }
});

$('#refresh_btn').click(function() {
  socket.emit('multiscreen_refresh', ROOM_ID);
  drop_state();
});

});
