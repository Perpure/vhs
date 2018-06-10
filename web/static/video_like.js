var lk=document.getElementById("like");
var dlk=document.getElementById("dislike");
var condition=0;

var stl=window.getComputedStyle(lk);
if(stl.backgroundImage[stl.backgroundImage.length-7]=='L')
  condition=1;
stl=window.getComputedStyle(dlk);
if(stl.backgroundImage[stl.backgroundImage.length-7]=='D')
  condition=-1;

$('#like').click(function(){
            $.ajax({
               url:"/likeVideo/"+hash,
               type:"GET",
               dataType:"text",
               success:function(response){},
               error:function(){
                    alert('Произошла ошибка')}
            });
            if(condition==1)
            {
                lk.style.backgroundImage="url(/static/lik1.png)";
                $("#lik").html($("#lik").html()-1);
                condition=0;
            }
            else if(condition){
                lk.style.backgroundImage="url(/static/lik1L.png)";
                dlk.style.backgroundImage="url(/static/dis1.png)";
                condition=1;
                $("#lik").html($("#lik").html()-(-1));
                $("#dis").html($("#dis").html()-1);
            }
            else
            {
              lk.style.backgroundImage="url(/static/lik1L.png)";
              condition=1;
              $("#lik").html($("#lik").html()-(-1));
            }
            calc();
});

$('#dislike').click(function(){
            $.ajax({
               url:"/dislikeVideo/"+hash,
               type:"GET",
               dataType:"text",
               success:function(response){},
               error:function(){
                    alert('Произошла ошибка')}
            });
            var stl=window.getComputedStyle(dlk);
            if(condition==-1)
            {
                dlk.style.backgroundImage="url(/static/dis1.png)";
                condition=0;
                $("#dis").html($("#dis").html()-1);
            }
            else if(condition)
            {
                dlk.style.backgroundImage="url(/static/dis1D.png)";
                lk.style.backgroundImage="url(/static/lik1.png)";
                condition=-1;
                $("#dis").html($("#dis").html()-(-1));
                $("#lik").html($("#lik").html()-1);
            }
            else
            {
                dlk.style.backgroundImage="url(/static/dis1D.png)";
                condition=-1;
                $("#dis").html($("#dis").html()-(-1));
            }
            calc();
});
