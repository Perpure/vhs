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
                                        var name=response1.substr(cur,cur1-cur);
                                        cur=cur1+2;
                                        while(response1[cur1]!=";" || response1[cur1+1]!=";")
                                            cur1++;
                                        var text=response1.substr(cur,cur1-cur);
                                        commSection.innerHTML='<div class="Comment"><img src="../static/a.png" alt="" class="commAva"><div class="commTxt"><p>'+name+'</p><p>'+text+'</p></div></div>'+commSection.innerHTML;
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
addCom.addEventListener('click',function(){
            var txt=plate.value;
            $.ajax({
               url:"/postComm/"+hash+"/"+txt,
               type:"GET",
               dataType:"text",
               success:function(response){},
               error:function(){}
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

calc();

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
            document.getElementById("like").style.backgroundImage="url(/static/lik1L.png)";
            document.getElementById("dislike").style.backgroundImage="url(/static/dis1.png)";
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
            document.getElementById("dislike").style.backgroundImage="url(/static/dis1D.png)";
            document.getElementById("like").style.backgroundImage="url(/static/lik1.png)";
});


(function () {
    var Dator=document.getElementById("Dating");
    var Date=Dator.innerHTML;
    Date=Date.substr(0,20);
    Dator.innerHTML=Date;
    })();
