let elem=document.getElementById("logoTxt");
let body=document.getElementById("Body");
let wid=body.offsetWidth;
if(wid<=550)elem.innerHTML="VHS";

function mov()
{
    
    let Height=document.body.scrollHeight;
    let foot=document.getElementById("Footer");
    foot.style.top=0;
    foot.style.top=(Height-130)+"px";
    console.log(11);
}

mov();

let searching=false;
let search=document.getElementById("Search");
let searcher=document.getElementById("searcher");
let shadow=document.getElementById("Shad");
search.addEventListener('click',function(){
    if(searching)
    {
        shadow.style.display="none";
        searcher.style.display="none";
        searching=false;
    }
    else
    {       
        shadow.style.display="block";
        searcher.style.display="block";
        searching=true;
    }
});

let holder=document.getElementById("mHolder");
let opned=false;
holder.addEventListener('click',function(){
    let els=document.getElementsByClassName("navMen");
    if(opned)
    {        
        for(let i=0;i<els.length;i++)
            els[i].style.display="none";
        holder.style.backgroundColor="rgba(240, 203, 142,0)";
        opned=false;
    }
    else
    {
        for(let i=0;i<els.length;i++)
            els[i].style.display="block";
        holder.style.backgroundColor="rgba(240, 203, 142,0.4)";
        opned=true;
    }
    mov();
});

function swit(e){
        let elem=e.currentTarget;
        if(elem.value)
        {
            elem.style.backgroundColor="rgba(0,0,0,0)";
            elem.style.fontWeight="normal";
            elem.style.color="grey";
            elem.value=0;
        }
        else
        {        
            elem.style.backgroundColor="#f0cb8e";
            elem.style.fontWeight="bold";
            elem.style.color="black";
            elem.value=1;
        }
}

let start=document.getElementById("startSearch");
let date=document.getElementById("Date");
let views=document.getElementById("byViews");
let key=document.getElementById("searchKey");

views.value=0;
date.value=0;
views.addEventListener('click',swit);     
date.addEventListener('click',swit);  
     

    start.addEventListener('click',function(){
        let val=key.value;
        let vw=views.value;
        let dt=date.value;
        if(val=="")val=" ";
        $.ajax({
                       url:"/startSearch/"+val+"/"+vw+"/"+dt,
                       type:"GET",
                       dataType:"html",
                       success:function(response)
                       {
                            let placer="";
                            let plus=false;
                            for(let i=0;i<response.length;i++)
                            {
                                if(response[i]=='<' && response[i+1]=='m' && response[i+2]=='a' && response[i+3]=='i')plus=true;
                                if(plus)placer+=response[i];
                                if(response[i+2]=='/' && response[i+3]=='m' && plus)i=response.length;
                            }
                            placer=placer.substr(17);
                            let mn=document.getElementById("Main");
                            mn.innerHTML=placer;
                       },
                       error:function(){}
        });
    });
