var device = 0;
if(screen.width<=1024)
{
    device++;
}
if(screen.width<=500)
{
    device++;
}

var X = [[-90, 0, 0, -90, -95, -30, 0, -300, 0],
         [0, 0, 0, 0, 0, 0, 0, -100, 0],
         [-90, 0, 0, -70, -95, -20, 0, -110, 0]];

var Y = [[60, 40, -40, 40, 50, 45, -35, -40, 290],
         [60, 40, -40, 40, 50, 45, -35, -40, 290],
         [60, 40, -40, -60, 50, 45, -55, -90, -100]];

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
            content: '<p>Пусть ваши друзья зайдут в комнату</p>',
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
            content: '<p>Начните калибровку</p>',
            offsetX: X[device][i++],
            offsetY: Y[device][j++],
            beforeFunc: guideScroll
        },
        {
            element: $('#tourPhoto'),
            content: '<p>Сфотографируйте устройства, инициализируйте фотографию</p>',
            offsetX: X[device][i++],
            offsetY: Y[device][j++],
            beforeFunc: guideScroll
        },
        {
            element: $('#show_res'),
            content: '<p>Если вас устраивает получившаяся карта устройств, нажмите play для начала демонстрации</p>',
            offsetX: X[device][i++],
            offsetY: Y[device][j++],
            beforeFunc: guideScroll
        },
        {
            element: $('#tourFinale'),
            content: '<p>Надеемся, что вам понравится Сплитскрин, приятного использования</p>',
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
