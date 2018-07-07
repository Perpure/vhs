var videos = [];
var next_page_token = '';
var more_videos = '<button id="more_videos">Больше видео</button>';
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
    $('#videos_block').append(more_videos);
    $('#more_videos').click(get_more_videos);
}


function output_video(video_item) {
    var duration = moment.duration(video_item['contentDetails']['duration']);

    var html = '<div>' +
                    '<div>' +
                    '<img width="320px" height="180px" src="' + video_item['snippet']['thumbnails']['medium']['url'] + '">' +
                    '</div>' +
                    '<div>' +
                    '<h5>' + video_item['snippet']['title'] + '</h5>' +
                    '<p>Автор: ' + video_item['snippet']['channelTitle'] + '</p>' +
                    '<p> Длина: ' + duration.humanize() + '</p>' +
                    '<span hidden="true">' + video_item['id'] + '</span>' +
                    '</div>' +
                '</div>';
    $('#videos_block').append(html);
}


$(document).ready(function() {
    moment.locale('ru');
    $('#submit').click(find_videos);
});
