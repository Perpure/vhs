var speed=3000;
var hash=window.location.href;
var sl=0;
for(var i=0;i<hash.length;i++)
    if(hash[i]=='/')sl=i;
hash=hash.substring(sl+1);

var curComms = document.getElementsByClassName("comment").length;
setTimeout(function step(){
    $.ajax({
        url:"/askNewComm/"+hash,
        type:"GET",
        dataType:"text",
        success:function(response)
        {
            if(response>curComms)
            {
                var def=response-curComms;
                $.ajax({
                    url:"/getNewComm/"+hash+"/"+curComms,
                    type:"GET",
                    dataType:"json",
                    success:function(response1)
                    {
                        response1.forEach(function(element){
                          var comment=$('<div class="comment"></div>');
                          var ava=$('<div class="comment_ava"><img src="'+element.ava+'" alt="" class="comment_ava-img"></div>');
                          var txt=$('<div><p class="comment_author"><a href="/cabinet/'+element.login+'">'+element.name+'</a></p><p>'+element.text+'</p></div></div>');
                          comment.append(ava);
                          comment.append(txt);
                          $('#CSect').prepend(comment);
                        });
                    },
                    error:function(){}
                });
                curComms=response;
            }
        },
        error:function(){}
    });
    setTimeout(step,speed);
},speed);

if($('#addC')!=null)$('#addC').click(function(){
            var txt=$('#txtPlate').val();
            $.ajax({
               url:"/postComm/"+hash+"/",
               type:"GET",
               dataType:"text",
               success:function(response){},
               error:function(){},
               data:{comm: txt}
            });
            plate.value="";
});

function calc()
{
    var lkes=$("#lik");
    var disl=$("#dis");
    var lkesIn=$("#likSh");
    var disIn=$("#disSh");
    lkes=lkes.html();
    disl=disl.html();
    denom=lkes*1+disl*1;
    if(!denom)
    {
      lkes=0.5;
      disl=0.5;
      denom=1;
    }
    lkesIn.css('width',(lkes*100)/denom+"%");
    disIn.css('width',(disl*100)/denom+"%");
}

calc();

$('.tag').click(function(){
        var val = this.innerText;
        var vw=0;
        var dt=0;
        if (pr_page == "" ) {
            map_needed=$('#show_video_map').prop('checked');
        }

        if(val=="") val=" ";
        $.ajax({
                       url:"/startSearch",
                       type:"GET",
                       dataType:"html",
                       data: {
                            ask:val,
                            view:vw,
                            dat:dt
                       },
                       success:function(response)
                       {
                         var placer="";
                         var plus=false;
                         response=$.parseHTML(response);
                         var tempDom = $('search').append(response);
                         var maine=$('#Main', tempDom);
                         $(tempDom).empty();
                         $("#Main").html($(maine).html());
                       },
                       error:function(){}
        });
        if (pr_page != "") {
            $.getScript("https://api-maps.yandex.ru/2.1/?lang=ru_RU", function () {$.getScript('/static/videos_map.js');});
        }
        else {
            $.getScript('/static/videos_map.js');
        }
        pr_page="";

    });
