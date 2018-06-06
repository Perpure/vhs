
var subBtns=document.getElementsByClassName("subscribe-btn");
for(var i=0;i<subBtns.length;i++)
    subBtns[i].addEventListener('click',function(){
      var val=this.value;
      $.ajax({
         url:"/subscribe/"+val,
         type:"GET",
         dataType:"text",
         success:function(response){},
         error:function(){}
      });
      if(this.innerHTML=="Подписаться")this.innerHTML="Отписаться";
      else this.innerHTML="Подписаться";
    });
