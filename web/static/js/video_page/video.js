var HASH = window.location.href;
var sl = 0;

for (var i = 0; i < HASH.length; i++) {
    if(HASH[i] == '/') {
        sl = i;
    }
}

HASH = HASH.substring(sl + 1);

jQuery(function($) {
    $('#addC').click(function(){
        var txt = $('#txtPlate').val();
        $.ajax({
            url: "/postComm/" + HASH + "/",
            type: "GET",
            dataType: "text",
            data: {comm: txt}
        });
        $('#txtPlate').val('');
        var comment = $('<div class="comment"></div>');
        var ava = $('<div class="comment__ava"><img src="' + $('#myAva').attr('src') + '" alt="" class="comment__ava-img"></div>');
        var txt = $('<div><p class="comment__author"><a href="' + $('#myProf').attr('href')+'">' + $('#myProf').html() + '</a></p><p>' + txt + '</p></div></div>');
        comment.append(ava);
        comment.append(txt);
        $('#CSect').prepend(comment);
    });

    function calc()
    {
        var likes = parseInt( $("#lik").html() ),
            dislikes = parseInt( $("#dis").html() ),
            lkesIn = $("#likSh"),
            disIn = $("#disSh"),
            denom = likes + dislikes;
        if ( !denom )
        {
            likes = 0.5;
            dislikes = 0.5;
            denom = 1;
        }
        lkesIn.css('width', likes * 100 / denom + "%");
        disIn.css('width', dislikes * 100 / denom + "%");
    }

    calc();

    $('.tag').click(function() {
        var tagName = $(this).text(),
            vw = 0,
            dt = 0;
        if( tagName == "" ) {
            tagName = " ";
        }
        $.ajax({
            url: "/startSearch",
            type: "GET",
            dataType: "html",
            data: {
                ask: tagName,
                view: vw,
                dat: dt
            },
            success: function(response)
            {
                var placer = "";
                response = $.parseHTML(response);
                var tempDom = $('search').append(response);
                var maine = $('#Main', tempDom);
                $(tempDom).empty();
                $("#Main").html($(maine).html());
            }
        });
        if ( pr_page == "" ) {
            map_needed = $('#show_video_map').prop('checked');
            $.getScript('/static/videos_map.js');
        } else {
            $.getScript("https://api-maps.yandex.ru/2.1/?lang=ru_RU", function() {
                $.getScript('/static/videos_map.js');
            });
        }
        pr_page = "";
    });
});
