var body = document.getElementById("Body");
var wid = body.offsetWidth;

var holder=document.getElementById("mHolder");
var opned=false;
holder.addEventListener('click',function(){
    var els=document.getElementsByClassName("nav-menu__nav-men");
    if(opned)
    {
        for(var i = 0; i<els.length; i++)
            els[i].style.display="none";
        holder.style.backgroundColor="rgba(240, 203, 142,0)";
        opned=false;
    }
    else
    {
        for(var i = 0; i<els.length; i++)
            els[i].style.display="block";
        holder.style.backgroundColor="rgb(73, 69, 59)";
        opned=true;
    }
});

var clast=document.getElementsByClassName("nav-menu__nav-men_nav-clast");
for(var j=0;j<clast.length;j++){
    clast[j].addEventListener('click',function()
    {
        if(screen.width<570)
        {
            var ins=this.getElementsByClassName("nav-menu__nav-men_sub-btn");
            this.style.height=ins.length*50+60+"px";
        }
    });
    clast[j].addEventListener('mouseout',function()
    {
        if(screen.width<570)
        {
            this.style.height=50+"px";
        }
    });
    }
