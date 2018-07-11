$(".profile_subscribe-btn").click(function(){
    var val=this.value();
    $.ajax({
        url:"/subscribe/"+val,
        type:"GET",
        dataType:"text",
        success:function(response){},
        error:function(){}
    });
    var cnt=$("#subCnt"+val);
    if(this.innerHTML=="Подписаться")
    {
        cnt.html(cnt.html()-(-1));
        this.innerHTML="Отписаться";
    }
    else
    {
        cnt.html(cnt.html()-1);
        this.innerHTML="Подписаться";
    }
});
