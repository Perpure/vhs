var videos = [];
var next_page_token = '';
var more_videos = '<button class="yt-search_more" id="more_videos">Больше видео</button>';
var search;


jQuery(function($) {

function find_videos() {
    search = $('#search').val();
    $('#videos_block').html('');
    $('.yt-video_error').remove();

    if (search.length > 0) {

        $.ajax({
            url:'/youtube_videos',
            data: {'query': search}
        }).then(function(data) {
            if (data !== 'Error') {
                handle_data(data);
            } else {
                $('#searcher_block').after('<p class="yt-video_error">Ошибка поиска</p>')
            }
        });

    } else {
        $('#searcher_block').after('<p class="yt-video_error">Строка запроса не должна быть пустой</p>')
    }
}


function get_more_videos() {
    $('#more_videos').remove();

    $.ajax({
        url:'/youtube_videos',
        data: {
            'query': search,
            'nextPageToken': next_page_token
        }
    }).then(function(data) {
        if (data !== 'Error') {
            handle_data(data);
        }
    });
}


function handle_data(data) {
    next_page_token = data['nextPageToken'];
    videos = data['videos'];
    for (var id in videos) {
        output_video(videos[id]);
    }
    if (next_page_token != 0 && videos.length > 0) {
        $('#videos_block').append(more_videos);
        $('#more_videos').click(get_more_videos);
    }
}


function output_video(video_item) {
    var title = truncate(video_item['snippet']['title'], 25);
    var author = truncate(video_item['snippet']['channelTitle'], 20);
    var dur = duration(video_item['contentDetails']['duration']);

    var html = '<div class="yt-video">' +
                    '<div class="yt-video_img">' +
                    '<img src="' + video_item['snippet']['thumbnails']['medium']['url'] + '">' +
                    '</div>' +
                    '<div class="yt-video_info">' +
                    '<h6>' + title + '</h6>' +
                    '<p>Автор: ' + author + '<br>' +
                    'Длина: ' + dur + '</p>' +
                    '<span hidden="true">' + video_item['id'] + '</span>' +
                    '</div>' +
                '</div>';
    $('#videos_block').append(html);
}


function truncate(string, length){
    var trunc_str;
    if (string.length > length) {
        trunc_str = string.substr(0, length-3) + '...';
    } else {
        trunc_str = string;
    }

    return trunc_str;
}


function duration(iso8601) {
    var x = '';
    var data = {};

    for (var i=2; i<iso8601.length; i++) {
        if (!isNaN(iso8601.charAt(i))) {
            x+=iso8601.charAt(i);
        } else {
            data[iso8601.charAt(i)] = x;
            x = '';
        }
    }
    if (data['H'] !== undefined) {
        var h = data['H'];

        if (h == 1) return ("1 час");
        else if (h <= 4) return (h + " часа");
        else if (h <= 20) return (h + " часов");
        else if (h.charAt(h.length-1) == 1) return (h + " час");
        else if (h.charAt(h.length-1) <= 4) return (h + " часа");
        else return (h + " часов");
    }

    if (data['M'] !== undefined) {
        var m = data['M'];

        if (m == 1) return ("1 минута");
        else if (m <= 4) return (m + " минуты");
        else if (m <= 20) return (m + " минут");
        else if (m.charAt(m.length-1) == 1) return (m + " минута");
        else if (m.charAt(m.length-1) <= 4) return (m + " минуты");
        else return (m + " минут");
    }

    if (data['S'] !== undefined) {
        var s = data['S'];

        if (s == 1) return ("1 секунда");
        else if (s <= 4) return (s + " секунды");
        else if (s <= 20) return (s + " секунд");
        else if (s.charAt(s.length-1) == 1) return (s + " секунда");
        else if (s.charAt(s.length-1) <= 4) return (s + " секунды");
        else return (s + " секунд");
    }
}


$(document).ready(function() {
    $('#submit').click(find_videos);
});

});