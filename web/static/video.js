        var speed=3000;
        var hash=window.location.href;
        var sl=0;
        for(var i=0;i<hash.length;i++)
            if(hash[i]=='/')sl=i;
        hash=hash.substring(sl+1);
        
        var commSection=document.getElementById("CSect");
        var curComms = document.getElementsByClassName("Comment").length;
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
                                   dataType:"text",
                                   success:function(response1)
                                   {
                                     var cur=0;
                                     var cur1=0;
                                     for(var i=0;i<def;i++)
                                     {
                                        while(response1[cur1]!="," || response1[cur1+1]!=",")
                                            cur1++;
                                        var login=response1.substr(cur,cur1-cur);
                                        cur=cur1+2;
                                        while(response1[cur1]!="." || response1[cur1+1]!=".")
                                            cur1++;
                                        var name=response1.substr(cur,cur1-cur);
                                        cur=cur1+2;
                                        while(response1[cur1]!=";" || response1[cur1+1]!=";")
                                            cur1++;
                                        var text=response1.substr(cur,cur1-cur);
                                        commSection.innerHTML='<div class="Comment"><img src="../static/a.png" alt="" class="commAva"><div class="commTxt"><p class="commAuth"><a href="/cabinet/'+login+'" class="Link">'+name+'</a></p><p>'+text+'</p></div></div>'+commSection.innerHTML;
                                     }
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
    lkesIn.style.width=(lkes*100)/(lkes*1+disl*1)+"%";
    disIn.style.width=(disl*100)/(lkes*1+disl*1)+"%";
}

if(addCom!=null)calc();

var lk=document.getElementById("like");
var dlk=document.getElementById("dislike");

$('#like').click(function(){
            $.ajax({
               url:"/likeVideo/"+hash,
               type:"GET",
               dataType:"text",
               success:function(response){
                    var parsedJson = $.parseJSON(response);
                    $("span.lik").empty()
                    $("span.dis").empty()
                    var likes = parsedJson[0].likes
                    var dislikes = parsedJson[0].dislikes
                    $("span.lik").html(likes)
                    $("span.dis").html(dislikes)
                    console.log(parsedJson)
                    calc();                    
                    },
               error:function(){
                    alert('Произошла ошибка')}
            });
            var stl=window.getComputedStyle(lk);
            if(stl.backgroundImage[stl.backgroundImage.length-7]=='L')lk.style.backgroundImage="url(/static/lik1.png)";
            else{
                lk.style.backgroundImage="url(/static/lik1L.png)";
                dlk.style.backgroundImage="url(/static/dis1.png)";
            }
});

$('#dislike').click(function(){
            $.ajax({
               url:"/dislikeVideo/"+hash,
               type:"GET",
               dataType:"text",
               success:function(response){
                    var parsedJson = $.parseJSON(response);
                    $("span.lik").empty()
                    $("span.dis").empty()
                    var likes = + parsedJson[0].likes
                    var dislikes = parsedJson[0].dislikes
                    $("span.lik").html(likes)
                    $("span.dis").html(dislikes)
                    console.log(parsedJson)
                    calc();    
                    },
               error:function(){
                    alert('Произошла ошибка')}
            });
            var stl=window.getComputedStyle(dlk);
            if(stl.backgroundImage[stl.backgroundImage.length-7]=='D')dlk.style.backgroundImage="url(/static/dis1.png)";
            else{            
                dlk.style.backgroundImage="url(/static/dis1D.png)";
                lk.style.backgroundImage="url(/static/lik1.png)";
            }
});


(function () {
    var Dator=document.getElementById("Dating");
    var Dte=Dator.innerHTML;
    console.log(12);
    Dte=Dte.substr(0,10);
    Dator.innerHTML=Dte;
})();

var taggs=document.getElementsByClassName("Tag");
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
                            for(var i=0;i<response.length;i++)
                            {
                                if(response[i]=='<' && response[i+1]=='m' && response[i+2]=='a' && response[i+3]=='i')plus=true;
                                if(plus)placer+=response[i];
                                if(response[i+2]=='/' && response[i+3]=='m' && plus)i=response.length;
                            }
                            placer=placer.substr(17);
                            var mn=document.getElementById("Main");
                            mn.innerHTML=placer;
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
