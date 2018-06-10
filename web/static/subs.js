
var subBtns=document.getElementsByClassName("subscribe-btn");
for(var i=0;i<subBtns.length;i++)
    subBtns[i].addEventListener('click',function(){
      var val=this.value;
      $.ajax({
         url:"/subscribe/"+val,
         type:"GET",
         dataType:"text",
         success:function(response){
           var cnt=document.getElementById("subCnt"+val);
           if(this.innerHTML=="Подписаться")
             {
               cnt.innerHTML-=(-1);
               this.innerHTML="Отписаться";
             }
           else
           {
             cnt.innerHTML-=1;
             this.innerHTML="Подписаться";
           }
         },
         error:function(){}
      });
    });
