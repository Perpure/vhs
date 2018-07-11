var lk=$("#like");
var dlk=$("#dislike");
var condition=0;

if(lk.css('background-image')[lk.css('background-image').length-7]=='L')
{
    condition=1;
}
if(dlk.css('background-image')[dlk.css('background-image').length-7]=='D')
{
    condition=-1;
}

$('#like').click(function(){
    $.ajax({
        url:"/likeVideo/"+hash,
        type:"GET",
        dataType:"text",
        success:function(response){},
        error:function(){
            alert('Произошла ошибка')}
    });
    if(condition==1)
    {
        lk.css('background-image',"url(/static/images/lik1.png)");
        $("#lik").html($("#lik").html()-1);
        condition=0;
    }
    else if(condition){
        lk.css('background-image',"url(/static/images/lik1L.png)");
        dlk.css('background-image',"url(/static/images/dis1.png)");
        condition=1;
        $("#lik").html($("#lik").html()-(-1));
        $("#dis").html($("#dis").html()-1);
    }
    else
    {
        lk.css('background-image',"url(/static/images/lik1L.png)");
        condition=1;
        $("#lik").html($("#lik").html()-(-1));
    }
    calc();
});

$('#dislike').click(function(){
    $.ajax({
        url:"/dislikeVideo/"+hash,
        type:"GET",
        dataType:"text",
        success:function(response){},
        error:function(){
            alert('Произошла ошибка')}
    });
    if(condition==-1)
    {
        dlk.css('background-image',"url(/static/images/dis1.png)");
        condition=0;
        $("#dis").html($("#dis").html()-1);
    }
    else if(condition)
    {
        dlk.css('background-image',"url(/static/images/dis1D.png)");
        lk.css('background-image',"url(/static/images/lik1.png)");
        condition=-1;
        $("#dis").html($("#dis").html()-(-1));
        $("#lik").html($("#lik").html()-1);
    }
    else
    {
        dlk.css('background-image',"url(/static/images/dis1D.png)");
        condition=-1;
        $("#dis").html($("#dis").html()-(-1));
    }
    calc();
});
