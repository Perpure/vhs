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
    
    var inputSearch = new ymaps.control.SearchControl({
        options: {
            size: 'large'          
        }
    });    
    
    map = new ymaps.Map("videos_map", {
            center: [lat, long],
            zoom: 7,
            controls: [inputSearch]
    });

    add_geotags(map);
}


function add_geotags(map) {
    var myClusterer = new ymaps.Clusterer();

    for (var i in videos) {
        for (var j in videos[i]['geotags']) {

            var gt = videos[i]['geotags'][j];

            var geotag = new ymaps.Placemark([gt[0], gt[1]],
            {
                balloonContent: 
                    '<div>' +
                        '<h3>' + videos[i]['title'] + '</h3>' +
                        '<a href="' + videos[i]['link'] + '">' +
                            '<img width="200px" height="200px"' +
                                'src="' + videos[i]['preview'] + '" href="' + videos[i]['link'] + '">' +
                        '</a>' +
                    '</div>',
                clusterCaption: videos[i]['title']
            });

            myClusterer.add(geotag);

        }
    }
    map.geoObjects.add(myClusterer);
}


ymaps.ready(function () {
    $('#videos_map').css('width', width);
    $('#videos_map').css('height', height);
    init();
});
