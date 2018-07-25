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
                        '<div class="video__preview"><a href="' + videos[i]['link'] + '">' +
                            '<img ' +
                                'src="' + videos[i]['preview'] + '" href="' + videos[i]['link'] + '" class="video__preview-img">' +
                        '</a></div>',
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
    map.events.add('wheel', function(e) {e.preventDefault();});

    map.events.add('wheel', function(e){e.preventDefault();});


    function changeTab(showingMode)
    {
        if (showingMode === 'table')
        {
            $('#video_table').show();
            $('#videos_map').hide();
        }
        else if (showingMode === 'map')
        {
            $('#video_table').hide();
            $('#videos_map').show();
        }
    }

    $('#map_switcher').bind('switch', function(e, showingMode) {
        changeTab(showingMode);
        $('#videos_map').css({
            'width': width,
            'height': height + 'px'
        });
        map.container.fitToViewport();
    });

    if (map_needed) {
        $('#showMap').click();
    }

    $.get("/video/data", {search: key.value}).done(add_geotags);
}

ymaps.ready(init_all);
