var map, geotag;
var width = '100%';
var height = '700px';
var lat, long;
var BalloonLayout;


function init () {
    if (typeof ymaps.geolocation.latitude != 'undefined')  {
        lat = ymaps.geolocation.latitude
        long = ymaps.geolocation.longitude
    }
    else {
        lat = 55.76;
        long = 37.64;
    }

    map = new ymaps.Map("videos_map", {
            center: [lat, long],
            zoom: 7
    });

    add_geotags(map);
}


function add_geotags(map) {

    for (var i in videos) {
        var geotag = new ymaps.Placemark([videos[i]['latitude'], videos[i]['longitude']],
        {
            title: videos[i]['title'],
            preview: videos[i]['preview'],
            link: videos[i]['link']
        },
        {
            balloonContentLayout: BalloonLayout
        });

        map.geoObjects.add(geotag);
    }
}


ymaps.ready(function () {
    BalloonLayout = ymaps.templateLayoutFactory.createClass(
        '<div>' +
            '<h3>$[properties.title]</h3>' +
            '<a href="$[properties.link]">' +
                '<img width="200px" height="200px"' +
                    'src="$[properties.preview]" href="$[properties.link]">' +
            '</a>' +
            '<a href="$[properties.link]"> Смотреть </a>' +
        '</div>'
    );

    $('#videos_map').css('width', width);
    $('#videos_map').css('height', height);
    init();
});