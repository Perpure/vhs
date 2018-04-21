var map, geotag;
var width = 400
var height = 200


function init () {
    map = new ymaps.Map("map", {
            center: [55, 47],
            zoom: 6,
            controls: [],
        },
        {
            autoFitToViewport: 'always'
        }
    );

    map.events.once('click', function(e) {
        geotag = new ymaps.Placemark(e.get('coords'),
            {
                hintContent: 'Выберите геотег для видео'
            },
            {
                draggable: true,
                preset: 'islands#redIcon'
            }
        );

        map.geoObjects.add(geotag);

        map.events.add('click', function(e) {
            geotag.geometry.setCoordinates(e.get('coords'));
        });
    });
}


ymaps.ready(function () {
    init();

    if ($('#geotag_is_needed').prop('checked')) {
        $('#map').css('width', width+'px');
        $('#map').css('height', height+'px');
    }
    
    $('#submit').click(function() {
        if ($('#geotag_is_needed').is(':checked') && typeof geotag === 'object') {
            $('#geotag_data').val(geotag.geometry.getCoordinates());
        }
        else {
            $('#geotag_data').value = '';
        }
    });

    $('#geotag_is_needed').change(function () {
        if ($('#geotag_is_needed').prop('checked')) {
            $('#map').css('width', width+'px');
            $('#map').css('height', height+'px');
        }
        else {
            $('#map').css('width', '0');
            $('#map').css('height', '0');
        }
    });
});
