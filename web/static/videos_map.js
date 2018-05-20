var map;
var long, lat;
var width = '100%';
var height = 700;


function add_geotags(videos) {
    map.geoObjects.removeAll();
    
    var myClusterer = new ymaps.Clusterer({
        clusterDisableClickZoom: true,    
    });

    for (var i in videos) {
        for (var j in videos[i]['geotags']) {
            var gt = videos[i]['geotags'][j];

            var geotag = new ymaps.Placemark([gt[0], gt[1]],
            {
                balloonContentHeader: videos[i]['title'],
                balloonContentBody: 
                        '<a href="' + videos[i]['link'] + '">' +
                            '<img width="200px" height="200px"' +
                                'src="' + videos[i]['preview'] + '" href="' + videos[i]['link'] + '">' +
                        '</a>',
                clusterCaption: videos[i]['title']
            });
            myClusterer.add(geotag);
        }
    }

    map.geoObjects.add(myClusterer);

}


function init_all() {
    typeof ymaps.geolocation.latitude === 'undefined' ?
                (lat = 55.76, long = 37.64) :
                (lat = ymaps.geolocation.latitude, long = ymaps.geolocation.longitude);

    map = new ymaps.Map("videos_map", {
            center : [lat, long],
            zoom : 7,
            maxZoom : 23,
            minZoom : 23,
            controls : ['zoomControl']
    });

    map.events.add('wheel', function(e){e.preventDefault();});

    $('#show_video_map').change(function () {
        $('#video_table').hide();
        $('#videos_map').css('width', width);
        $('#videos_map').css('height', height+'px');
        $('#showMap').hide();
        $('#showTab').show();
        map.container.fitToViewport();
    });

    $('#show_video_table').change(function () {
        $('#video_table').show();
        $('#videos_map').css('width', '0px');
        $('#videos_map').css('height', '0px');
        $('#showMap').show();
        $('#showTab').hide();
        map.container.fitToViewport();
    });

    $.get("/video/data", {search: key.value}).done(add_geotags);

    if (map_needed) {
        $('#show_video_map').trigger('change');
        $('#show_video_map').prop('checked', true);
    }
}

ymaps.ready(init_all);
