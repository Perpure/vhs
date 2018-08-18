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

function show_message(type, text)
{
    $('#formMessage').show();
    if(type == 'error')
    {
        $('#formMessage').removeClass('message_correct')
                      .addClass('message_error')
                      .html(text);
    }
    if(type == 'correct')
    {
        $('#formMessage').removeClass('message_error')
                      .addClass('message_correct')
                      .html(text);
    }
}

$('#image_form').on('submit', function(e) {
    e.preventDefault();
    if ($('#image').val() == '') {
        show_message('error', 'Файл не выбран');
        return;
    }
    var imageExtension =  $('#image').val()
            .split('.')
            .pop()
            .toLowerCase();
    if ( !['jpg', 'jpeg'].includes(imageExtension) ) {
        show_message('error', 'Неправильное расширение (должно быть jpeg или jpg)');
        return;
    }

    var form_data = new FormData();
    form_data.append('image', $('#image')[0].files[0]);

    $.ajax({
        data: form_data,
        processData: false,
        type: 'POST',
        contentType: false,
        dataType: 'json',
        success: function(data) {
            if (data.status) {
                show_message('correct', 'Фотография загружена');
                $('#map').show();
                $('#map').attr('src', data.map_url);
            }
            else {
                show_message('error', 'Мы не смогли идентифицировать устройства, попробуйте загрузить другую фотографию.');
            }
        },
        error: function(textStatus) {
            show_message('error', textStatus.status + ' ' + textStatus.statusText);
        }
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

    function guide() {
        var guide = $.guide({
            actions: [
                {
                    element: $('#startTour'),
                    content: '<p>Добро пожаловать в гид по Сплитскрину,<br> нажмите на экран, чтобы продолжить</p>',
                    offsetX: -90,
                    offsetY: 60
                },
                {
                    element: $('#tourCount'),
                    content: '<p>Пусть ваши друзья зайдут в комнату</p>',
                    offsetX: 0,
                    offsetY: 60
                },
                {
                    element: $('#tourChoose'),
                    content: '<p>Выберите видео</p>',
                    offsetX: 0,
                    offsetY: -40
                },
                {
                    element: $('#video_switcher'),
                    content: '<p>Либо с нашего сайта, либо с YouTube</p>',
                    offsetX: -90,
                    offsetY: 40
                },
                {
                    element: $('#calibrate_btn'),
                    content: '<p>Составьте большой экран из устройств участников, <br> Начните калибровку</p>',
                    offsetX: -90,
                    offsetY: 40
                },
                {
                    element: $('#tourPhoto'),
                    content: '<p>Сфотографируйте устройства,<br> инициализируйте фотографию</p>',
                    offsetX: 0,
                    offsetY: -50
                },
                {
                    element: $('#show_res'),
                    content: '<p>Если вас устраивает получившаяся карта устройств, нажмите play для начала демонстрации</p>',
                    offsetX: -90,
                    offsetY: 50,
                    isBeforeFuncExec: true,
                    beforeFunc: function(g) {
                        $('#show_res').slideDown(function() {
                            g.execAction();
                        });
                    }
                }
            ]
        });
    }
    $('#startTour').click(guide);
});
