var LK = $("#like");
var DLK = $("#dislike");
var CONDITION = 0;

if(LK.hasClass('video-rating__btn_good_active'))
{
    CONDITION = 1;
}
if(DLK.hasClass('video-rating__btn_bad_active'))
{
    CONDITION = -1;
}

$('#like').click(function(){
    $.ajax({
        url: "/likeVideo/"+HASH,
        type: "GET",
        dataType: "text",
        error: function(){
            alert('Произошла ошибка')}
    });
    if(CONDITION == 1)
    {
        LK.removeClass('video-rating__btn_good_active');
        $("#lik").html($("#lik").html() - 1);
        CONDITION = 0;
    }
    else if(CONDITION){
        LK.addClass('video-rating__btn_good_active');
        DLK.removeClass('video-rating__btn_bad_active');
        CONDITION = 1;
        $("#lik").html($("#lik").html() - (-1));
        $("#dis").html($("#dis").html() - 1);
    }
    else
    {
        LK.addClass('video-rating__btn_good_active');
        CONDITION = 1;
        $("#lik").html($("#lik").html() - (-1));
    }
    calc();
});

$('#dislike').click(function(){
    $.ajax({
        url: "/dislikeVideo/"+HASH,
        type: "GET",
        dataType: "text",
        error: function(){
            alert('Произошла ошибка')}
    });
    if(CONDITION == -1)
    {
        DLK.removeClass('video-rating__btn_bad_active');
        CONDITION = 0;
        $("#dis").html($("#dis").html() - 1);
    }
    else if(CONDITION)
    {
        DLK.addClass('video-rating__btn_bad_active');
        LK.removeClass('video-rating__btn_good_active');
        CONDITION = -1;
        $("#dis").html($("#dis").html() - (-1));
        $("#lik").html($("#lik").html() - 1);
    }
    else
    {
        DLK.addClass('video-rating__btn_bad_active');
        CONDITION = -1;
        $("#dis").html($("#dis").html() - (-1));
    }
    calc();
});
