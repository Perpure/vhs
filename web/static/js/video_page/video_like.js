var LK = $("#like");
var DLK = $("#dislike");
var CONDITION = 0;

if(LK.css('background-image')[LK.css('background-image').length-7] == 'L')
{
    CONDITION = 1;
}
if(DLK.css('background-image')[DLK.css('background-image').length-7] == 'D')
{
    CONDITION = -1;
}

$('#like').click(function(){
    $.ajax({
        url: "/likeVideo/"+hash,
        type: "GET",
        dataType: "text",
        error: function(){
            alert('Произошла ошибка')}
    });
    if(CONDITION == 1)
    {
        LK.css('background-image', "url(/static/images/lik1.png)");
        $("#lik").html($("#lik").html() - 1);
        CONDITION = 0;
    }
    else if(CONDITION){
        LK.css('background-image', "url(/static/images/lik1L.png)");
        DLK.css('background-image', "url(/static/images/dis1.png)");
        CONDITION = 1;
        $("#lik").html($("#lik").html() - (-1));
        $("#dis").html($("#dis").html() - 1);
    }
    else
    {
        LK.css('background-image', "url(/static/images/lik1L.png)");
        CONDITION = 1;
        $("#lik").html($("#lik").html() - (-1));
    }
    calc();
});

$('#dislike').click(function(){
    $.ajax({
        url: "/dislikeVideo/"+hash,
        type: "GET",
        dataType: "text",
        error: function(){
            alert('Произошла ошибка')}
    });
    if(CONDITION == -1)
    {
        DLK.css('background-image', "url(/static/images/dis1.png)");
        CONDITION = 0;
        $("#dis").html($("#dis").html() - 1);
    }
    else if(CONDITION)
    {
        DLK.css('background-image', "url(/static/images/dis1D.png)");
        LK.css('background-image', "url(/static/images/lik1.png)");
        CONDITION = -1;
        $("#dis").html($("#dis").html() - (-1));
        $("#lik").html($("#lik").html() - 1);
    }
    else
    {
        DLK.css('background-image', "url(/static/images/dis1D.png)");
        CONDITION = -1;
        $("#dis").html($("#dis").html() - (-1));
    }
    calc();
});
