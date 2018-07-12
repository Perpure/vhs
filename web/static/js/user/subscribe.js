$(".profile_subscribe-btn").click(function(){
    var val = $(this).val();
    $.ajax({
        url: "/subscribe/"+val,
        type: "GET",
        dataType: "text"
    });
    var cnt = $("#subCnt" + val);
    if($(this).html() == "Подписаться")
    {
        cnt.html(cnt.html() - (-1));
        $(this).html() = "Отписаться";
    }
    else
    {
        cnt.html(cnt.html() - 1);
        $(this).html() = "Подписаться";
    }
});
