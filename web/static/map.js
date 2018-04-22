var map, geotag;
var width = 400;
var height = 200;
var data;


function create_geotag(coords) {
    geotag = new ymaps.Placemark(coords,
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
}


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
        create_geotag(e.get('coords'));
    });
}


function show_map() {
    $('#geotag_is_needed').addClass('btn_pushed');
    $('#map').css('width', width+'px');
    $('#map').css('height', height+'px');
}

function hide_map() {
    $('#map').css('width', '0px');
    $('#map').css('height', '0px');
    $('#geotag_is_needed').removeClass('btn_pushed');
}

ymaps.ready(function () {
    data = JSON.parse($('#geotag_data').val())
    init();

    if (data['needed']) {
        for (var i in data['coords']) {
            create_geotag(data['coords'][i]);
        }
        show_map();
    }

    $('#geotag_is_needed').click(function(e) {
        if (data['needed']) {
            data['needed'] = false;
            hide_map();

        }
        else {
            data['needed'] = true;
            show_map();
        }
    });
    
    $('#submit').click(function() {
        if (data['needed'] && typeof geotag === 'object') {
            data['coords'].push(geotag.geometry.getCoordinates());
        }
        $('#geotag_data').val(JSON.stringify(data));
    });
});
