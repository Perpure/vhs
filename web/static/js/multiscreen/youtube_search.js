var videos = [];
var next_page_token = '';
var more_videos = '<button class="yt-search__more" id="more_videos">Больше видео</button>';
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
        }).done(function(data) {
            handle_data(data)
        }).fail(function(jqXHR) {
            if (jqXHR.status == 404) {
                $('#searcher_block').after('<p class="yt-video_error">Видео не найдены</p>')
            }
            else if (jqXHR.status == 500) {
                $('#searcher_block').after('<p class="yt-video_error">Ошибка работы сервера</p>')
            }
            else {
                $('#searcher_block').after('<p class="yt-video_error">Неизвестная ошибка</p>')
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
    }).done(function(data) {
        handle_data(data);
    }).fail(function(jqXHR) {
        if (jqXHR.status == 404) {
            $('#videos_block').after('<p class="yt-video_error">Видео не найдены</p>')
        }
        else if (jqXHR.status == 500) {
            $('#videos_block').after('<p class="yt-video_error">Ошибка работы сервера</p>')
        }
        else {
            $('#videos_block').after('<p class="yt-video_error">Неизвестная ошибка</p>')
        }
    });
}


function handle_data(data) {
    next_page_token = data.nextPageToken;
    videos = data.videos;
    for (var id in videos) {
        output_video(videos[id]);
    }
    if (next_page_token != 0 && videos.length > 0) {
        $('#videos_block').append(more_videos);
        $('#more_videos').click(get_more_videos);
    }
}


function output_video(video_item) {
    var html = '<div class="video">' +
                    '<div class="video_preview">' +
                    '<img class="video_preview-img" src="' + video_item.preview + '">' +
                    '</div>' +
                    '<div>' +
                    '<p class="video_title">' + video_item.title + '</p>' +
                    '<p class="italic">' + video_item.author + '<br>' + video_item.duration + '</p>' +
                    '<span hidden="true">' + video_item.id + '</span>' +
                    '</div>' +
                '</div>';
    $('#videos_block').append(html);
}

$(document).ready(function() {
    $('#submit').click(find_videos);
});

});