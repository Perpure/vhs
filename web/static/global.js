elem1=document.getElementById("Home");
elem2=document.getElementById("HomImg");
elem3=document.getElementById("Log");
elem4=document.getElementById("LogImg");
elem5=document.getElementById("Come");
elem6=document.getElementById("ComeImg");

elem1.addEventListener('mouseover',function(){
    elem2.src="static/mainH.png";        
});
elem1.addEventListener('mouseout',function(){
    elem2.src="static/main.png";         
});

elem3.addEventListener('mouseover',function(){
    elem4.src="static/regH.png";        
});
elem3.addEventListener('mouseout',function(){
    elem4.src="static/reg.png";         
});

elem5.addEventListener('mouseover',function(){
    elem6.src="static/logH.png";        
});
elem5.addEventListener('mouseout',function(){
    elem6.src="static/log.png";         
});
