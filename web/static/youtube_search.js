var videos = [];
var next_page_token = '';
var more_videos = '<button class="yt-search_more" id="more_videos">Больше видео</button>';
var search;

function find_videos() {
    search = $('#search').val();
    $('#videos_block').html('');

    if (search.length > 0) {

        $.ajax({
            url:'/youtube_videos',
            data: {'query': search}
        }).then(function(data) {
            if (data !== 'Error') {
                handle_data(data);
            }
        });

    } else {
        alert('string must not be empty');
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
    if (next_page_token != 0) {
        $('#videos_block').append(more_videos);
        $('#more_videos').click(get_more_videos);
    }
}


function output_video(video_item) {
    var title = truncate(video_item['snippet']['title'], 25);
    var author = truncate(video_item['snippet']['channelTitle'], 20);
    var duration = moment.duration(video_item['contentDetails']['duration']);

    var html = '<div class="yt-video">' +
                    '<div class="yt-video_img">' +
                    '<img src="' + video_item['snippet']['thumbnails']['medium']['url'] + '">' +
                    '</div>' +
                    '<div class="yt-video_info">' +
                    '<h6>' + title + '</h6>' +
                    '<p>Автор: ' + author + '<br>' +
                    'Длина: ' + duration.humanize() + '</p>' +
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


$(document).ready(function() {
    moment.locale('ru');
    $('#submit').click(find_videos);
});
