var HASH = window.location.href;
var sl = 0;

for (var i = 0; i < HASH.length; i++) {
    if(HASH[i] == '/') {
        sl = i;
    }
}

HASH = HASH.substring(sl + 1);

var calc;

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
        var txt = $('<div class="comment__text"><p class="comment__author"><a href="' + $('#myProf').attr('href')+'">' + $('#myProf').html() + '</a></p><p>' + txt + '</p></div></div>');
        comment.append(ava);
        comment.append(txt);
        $('#CSect').prepend(comment);
    });

    calc = function()
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
        var tagName = $(this).text();
        tagName = tagName.replace('#', '*');
        window.location.replace('/search/' + tagName);
    });
});
