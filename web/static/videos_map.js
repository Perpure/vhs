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


function init_all(videos) {
    typeof ymaps.geolocation.latitude === 'undefined' ?
                (lat = 55.76, long = 37.64) :
                (lat = ymaps.geolocation.latitude, long = ymaps.geolocation.longitude);

    map = new ymaps.Map("videos_map", {
            center : [lat, long],
            zoom : 7,
            maxZoom : 23,
            minZoom : 23,
            controls : []
    });

    $('#show_video_map').change(function () {
        $('#video_table').hide();
        $('#videos_map').css('width', width);
        $('#videos_map').css('height', height+'px');
        map.container.fitToViewport();

        var footer_top = Number($('#Footer').css('top').slice(0, -2));
        footer_top += height/2;
        $('#Footer').css('top', footer_top+"px");
    });

    $('#show_video_table').change(function () {
        $('#video_table').show();
        $('#videos_map').css('width', '0px');
        $('#videos_map').css('height', '0px');
        map.container.fitToViewport();

        var footer_top = Number($('#Footer').css('top').slice(0, -2));
        footer_top -= height/2;
        $('#Footer').css('top', footer_top+"px");
    });


    fetch("/video/data", {search:key.value}).then(function(response){
        if(response.status == 200){
            response.json().then(add_geotags);
        }
    });

    if (map_needed) {
        $('#show_video_map').trigger('change');
        $('#show_video_map').prop('checked', true);
    }
}

ymaps.ready(function (videos) {
    init_all(videos);

});

function mover(){
        var Height=document.body.scrollHeight;
        var foot=document.getElementById("Footer");
        foot.style.top=(Height-130)+"px";
}

setTimeout(mover,2000);
