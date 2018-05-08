        let speed=3000;
        let hash=window.location.href;
        let sl=0;
        for(let i=0;i<hash.length;i++)
            if(hash[i]=='/')sl=i;
        hash=hash.substring(sl+1);
        
        let commSection=document.getElementById("CSect");
        let curComms = document.getElementsByClassName("Comment").length;
        setTimeout(function step(){
            $.ajax({
                       url:"/askNewComm/"+hash,
                       type:"GET",
                       dataType:"text",
                       success:function(response)
                       {
                            if(response>curComms)
                            {
                                   let def=response-curComms;
                                   $.ajax({
                                   url:"/getNewComm/"+hash+"/"+curComms,
                                   type:"GET",
                                   dataType:"text",
                                   success:function(response1)
                                   {
                                     let cur=0;
                                     let cur1=0;
                                     for(let i=0;i<def;i++)
                                     {
                                        while(response1[cur1]!="," || response1[cur1+1]!=",")
                                            cur1++;
                                        let name=response1.substr(cur,cur1-cur);
                                        cur=cur1+2;
                                        while(response1[cur1]!=";" || response1[cur1+1]!=";")
                                            cur1++;
                                        let text=response1.substr(cur,cur1-cur);
                                        commSection.innerHTML+='<div class="Comment"><img src="../static/a.png" alt="" class="commAva"><div class="commTxt"><p>'+name+'</p><p>'+text+'</p></div></div>';
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

var lkes=document.getElementById("lik");
var disl=document.getElementById("dis");
var lkesIn=document.getElementById("likSh");
var disIn=document.getElementById("disSh");
lkes=lkes.innerHTML;
disl=disl.innerHTML;
lkesIn.style.width=(lkes*100)/(lkes*1+disl*1)+"%";
disIn.style.width=(disl*100)/(lkes*1+disl*1)+"%";
