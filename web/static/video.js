        let speed=5000;
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

        let addCom=document.getElementById("addC");
        let plate=document.getElementById("txtPlate");
        addCom.addEventListener('click',function(){
            let txt=plate.value;
            let name="lol";
            $.ajax({
               url:"/postComm/"+hash+"/"+name+"/"+txt,
               type:"GET",
               dataType:"text",
               success:function(response){},
               error:function(){}
            });
            plate.value="";
        });
