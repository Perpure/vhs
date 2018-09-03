var YTSearchQuery = '',
    YTSearchNextPageToken = '';

jQuery(function($) {

    function find_videos(query) {
        YTSearchQuery = query;
        $('.yt-search__result').html('');
        $('.yt-video_error').remove();
        $('#more').show();

        if (query.length > 0) {
            send_video_search(query);
        } else {
            $('.yt-search__searcher').after('<p class="yt-video_error">Строка запроса не должна быть пустой</p>');
        }
    }

    function get_more_videos(query, nextPageToken) {
        $('#more').hide();
        send_video_search(query, nextPageToken);
    }

    function send_video_search(query, nextPageToken) {
        var requestData = {
                query: query
            };
        if (nextPageToken) {
            requestData.nextPageToken = nextPageToken;
        }
        $.ajax({
            url: '/youtube_videos',
            data: requestData
        }).done(function(data) {
            handle_data(data);
        }).fail(function(jqXHR) {
            if (jqXHR.status == 404) {
                $('.yt-search__searcher').after('<p class="yt-video_error">Видео не найдены</p>');
            }
            else if (jqXHR.status == 500) {
                $('.yt-search__searcher').after('<p class="yt-video_error">Ошибка работы сервера</p>');
            }
            else {
                $('.yt-search__searcher').after('<p class="yt-video_error">Неизвестная ошибка</p>');
            }
        });
    }

    function handle_data(data) {
        var videos = data.videos;
        YTSearchNextPageToken = data.nextPageToken;
        for (var i = 0; i < videos.length; i++) {
            output_video(videos[i]);
        }
        if (videos.length && YTSearchNextPageToken) {
            $('#more').show();
        }
        $('.video').click(select_video);
    }

    function output_video(video_item) {
        var html = '<div class="video">' +
                        '<div class="video__preview">' +
                            '<img class="video__preview-img" src="' + video_item.preview + '">' +
                        '</div>' +
                        '<div>' +
                            '<p class="video__title">' + video_item.title + '</p>' +
                            '<p class="italic">' + video_item.author + '<br>' + video_item.duration + '</p>' +
                            '<span class="video__id hidden">' + video_item.id + '</span>' +
                        '</div>' +
                    '</div>';
        $('.yt-search__result').append(html);
    }

    $('.searcher__btn').click(function() {
        var ytSearcher = $(this).parents('.searcher'),
            ytSearcherInput = ytSearcher.find('.searcher__input'),
            query = ytSearcherInput.val();
        find_videos(query);
    });

    $('#more').click(function() {
        get_more_videos(YTSearchQuery, YTSearchNextPageToken);
    });

    function select_video() {

        var requestData = {
            id: $(this).find('.video__id').text(),
            preview: $(this).find('.video__preview-img').attr('src')
        }

        $.post({
            url: location.href,
            data: requestData
        }).done(function() {
            location.href = location.href.split('/choose_youtube')[0];
        })
    };
});
