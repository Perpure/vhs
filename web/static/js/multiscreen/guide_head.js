var device;
if(screen.width<=500)
{
    device = 'phone';
} else if(screen.width<=1024)
{
    device = 'tablet';
} else
{
    device = 'desktop';
}

var X = {
        desktop: [-90, -5, 0, -90, -135, -5, -5, -5, -300, -5, -5, 0],
        tablet: [0, 0, 0, 0, 0, 0, 0, 0, -130, 0, 0, 0],
        phone: [-90, 0, 0, -70, -95, -90, 0, -10, -110, -80, -50, 0]};

var Y = {
        desktop: [60, 40, -40, 40, 50, 45, -35, 45, -40, -40, -40, 290],
        tablet: [60, 40, -40, 40, 50, 45, -35, 45, 45, -40, -40, 290],
        phone: [60, 40, -40, -60, 50, 45, -35, 45, -105, 45, 45, -100]};

jQuery(function($) {
    function guideScroll() {
        setTimeout(function() {
            var duration = 400;

            var txtUpper = $('.jquery-guide-content').offset().top;
            var height = $('.jquery-guide-content').height();
            var txtLower = txtUpper + height;

            var rectUpper = currentTop;
            var rectLower = rectUpper + currentHeight;

            var windUpper = $(window).scrollTop();
            var windLower = windUpper + screen.height;

            var guideUpper, guideLower;
            guideUpper = Math.min(txtUpper, rectUpper);
            guideLower = Math.max(rectLower, txtLower);

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
        var i = 0;
        var j = 0;
        var guide = $.guide({
        actions: [
        {
            element: $('#startTour'),
            content: '<p>Добро пожаловать в гид по Сплитскрину,<br> нажмите на экран, чтобы продолжить</p>',
            offsetX: X[device][i++],
            offsetY: Y[device][j++],
            beforeFunc: guideScroll
        },
        {
            element: $('#tourCount'),
            content: '<p>Пусть устройства, с которых планируется показ, зайдут в комнату</p>',
            offsetX: X[device][i++],
            offsetY: Y[device][j++],
            beforeFunc: guideScroll
        },
        {
            element: $('#tourChoose'),
            content: '<p>Выберите видео</p>',
            offsetX: X[device][i++],
            offsetY: Y[device][j++],
            beforeFunc: guideScroll
        },
        {
            element: $('#video_switcher'),
            content: '<p>Либо с нашего сайта, либо с YouTube</p>',
            offsetX: X[device][i++],
            offsetY: Y[device][j++],
            beforeFunc: guideScroll
        },
        {
            element: $('#calibrate_btn'),
            content: '<p>Составьте большой экран из устройств участников</p>',
            offsetX: X[device][i++],
            offsetY: Y[device][j++],
            beforeFunc: guideScroll
        },
        {
            element: $('#calibrate_btn'),
            content: '<p>Начните калибровку, чтобы придать каждому девайсу уникальный цвет</p>',
            offsetX: X[device][i++],
            offsetY: Y[device][j++],
            beforeFunc: guideScroll
        },
        {
            element: $('#tourPhoto'),
            content: '<p>Сфотографируйте устройства</p>',
            offsetX: X[device][i++],
            offsetY: Y[device][j++],
            beforeFunc: guideScroll
        },
        {
            element: $('#submit'),
            content: '<p>Инициализируйте фотографию, тогда сервер сможет определить положение каждого экрана</p>',
            offsetX: X[device][i++],
            offsetY: Y[device][j++],
            beforeFunc: guideScroll
        },
        {
            element: $('#show_res'),
            content: '<p>Если карта устройств соответствует их реальному положению и соотношению размеров, нажмите play для начала демонстрации</p>',
            offsetX: X[device][i++],
            offsetY: Y[device][j++],
            beforeFunc: guideScroll
        },
        {
            element: $('#stop_res'),
            content: '<p>Нажав на эту кнопку, вы остановите показ видео</p>',
            offsetX: X[device][i++],
            offsetY: Y[device][j++],
            beforeFunc: guideScroll
        },
        {
            element: $('#refresh_btn'),
            content: '<p>Если вы сменили видео, обязательно нажмите эту кнопку</p>',
            offsetX: X[device][i++],
            offsetY: Y[device][j++],
            beforeFunc: guideScroll
        },
        {
            element: $('#tourFinale'),
            content: '<p>Заметили ошибку? Пишите в Обратную связь. Приятного использования!</p>',
            offsetX: X[device][i],
            offsetY: Y[device][j],
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
