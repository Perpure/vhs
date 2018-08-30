jQuery(function($) {
    function guideScroll() {
        setTimeout(function() {
            var duration = 400;
            $('#placeholder').height($('.jquery-guide-content').height());

            var guideUpper = currentTop;
            var guideLower = guideUpper + currentHeight;

            var windUpper = $(window).scrollTop();
            var windLower = windUpper + screen.height - $('#placeholder').height();

            var delta, dU, dL;

            dU = guideUpper - windUpper - 20;
            dL = windLower - guideLower - 20;
            delta = Math.min(dL, dU) * ((dL < 0) * -1 + (dL > 0) * 1);
            delta *= dL * dU < 0;

            if(delta != 0)
            {
                $('body,html').animate({scrollTop: windUpper + delta}, duration);
            }
        }, 420);
    }

    function guide() {
        var guide = $.guide({
        actions: [
        {
            element: $('#startTour'),
            content: '<p>Добро пожаловать в гид по Сплитскрину,<br> нажмите на экран, чтобы продолжить</p>',
            beforeFunc: guideScroll
        },
        {
            element: $('#tourCount'),
            content: '<p>Пусть устройства, с которых планируется показ, зайдут в комнату</p>',
            beforeFunc: guideScroll
        },
        {
            element: $('#tourChoose'),
            content: '<p>Выберите видео</p>',
            beforeFunc: guideScroll
        },
        {
            element: $('#video_switcher'),
            content: '<p>Либо с нашего сайта, либо с YouTube</p>',
            beforeFunc: guideScroll
        },
        {
            element: $('#calibrate_btn'),
            content: '<p>Составьте большой экран из устройств участников</p>',
            beforeFunc: guideScroll
        },
        {
            element: $('#calibrate_btn'),
            content: '<p>Начните калибровку, чтобы придать каждому девайсу уникальный цвет</p>',
            beforeFunc: guideScroll
        },
        {
            element: $('#tourPhoto'),
            content: '<p>Сфотографируйте устройства</p>',
            beforeFunc: guideScroll
        },
        {
            element: $('#submit'),
            content: '<p>Инициализируйте фотографию, тогда сервер сможет определить положение каждого экрана</p>',
            beforeFunc: guideScroll
        },
        {
            element: $('#show_res'),
            content: '<p>Если карта устройств соответствует их реальному положению и соотношению размеров, нажмите play для начала демонстрации</p>',
            beforeFunc: guideScroll
        },
        {
            element: $('#stop_res'),
            content: '<p>Нажав на эту кнопку, вы остановите показ видео</p>',
            beforeFunc: guideScroll
        },
        {
            element: $('#refresh_btn'),
            content: '<p>Если вы сменили видео, обязательно нажмите эту кнопку</p>',
            beforeFunc: guideScroll
        },
        {
            element: $('#tourFinale'),
            content: '<p>Заметили ошибку? Пишите в Обратную связь. Приятного использования!</p>',
            isBeforeFuncExec: true,
            beforeFunc: function(g) {
                guideScroll();
                $('#show_res').slideDown(function() {
                    g.execAction();
                });
            }
        }]
        });
    }
    $('#startTour').click(guide);
});
