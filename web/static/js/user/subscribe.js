$(".profile__subscribe-btn").click(function(){
    var me=$(this);
    var val = me.val();
    $.ajax({
        url: "/subscribe/"+val,
        type: "GET",
        dataType: "text"
    });
    var cnt = $("#subCnt" + val);
    if(me.html() == "Подписаться")
    {
        cnt.html(cnt.html() - (-1));
        me.html("Отписаться");
    }
    else
    {
        cnt.html(cnt.html() - 1);
        me.html("Подписаться");
    }
});
