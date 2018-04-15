var x = 55.76;
var y = 37.64;
var map, geotag;
var width = 400
var height = 200


function init () {
    map = new ymaps.Map("map", {
            center: [x, y],
            zoom: 7
    });
    geotag = new ymaps.Placemark([x, y],
        {hintContent: 'Выберите геотег для видео'},
        {draggable: true,
        preset: 'islands#redIcon'});

    map.geoObjects.add(geotag);

    map.events.add('click', function(e) {
        geotag.geometry.setCoordinates(e.get('coords'));
    });
}


ymaps.ready(function () {
    $('#geotag_is_needed').removeAttr('checked');

    $('#submit').click(function() {
        if ($('#geotag_is_needed').is(':checked')) {
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
            init();

        }
        else {

            map.destroy();
            $('#map').css('width', '0');
            $('#map').css('height', '0');

        }
    });
});