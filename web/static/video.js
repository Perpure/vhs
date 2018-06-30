var speed=3000;
var hash=window.location.href;
var sl=0;
for(var i=0;i<hash.length;i++)
    if(hash[i]=='/')sl=i;
hash=hash.substring(sl+1);

var commSection=document.getElementById("CSect");
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
                            $("#CSect").get(0).innerHTML='<div class="comment"><div class="comment_ava"><img src="'+element.ava+'" alt="" class="comment_ava-img"></div><div class="comment_txt"><p class="comment_txt__auth"><a href="/cabinet/'+element.login+'">'+element.name+'</a></p><p>'+element.text+'</p></div></div>'+$("#CSect").get(0).innerHTML;
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

var addCom=document.getElementById("addC");
var plate=document.getElementById("txtPlate");
if(addCom!=null)addCom.addEventListener('click',function(){
            var txt=plate.value;
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
    var lkes=document.getElementById("lik");
    var disl=document.getElementById("dis");
    var lkesIn=document.getElementById("likSh");
    var disIn=document.getElementById("disSh");
    lkes=lkes.innerHTML;
    disl=disl.innerHTML;
    denom=lkes*1+disl*1;
    if(!denom)
    {
      lkes=0.5;
      disl=0.5;
      denom=1;
    }
    lkesIn.style.width=(lkes*100)/denom+"%";
    disIn.style.width=(disl*100)/denom+"%";
}

calc();

var taggs=document.getElementsByClassName("tag");
for(var i=0;i<taggs.length;i++)
    taggs[i].addEventListener('click',function(){
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
