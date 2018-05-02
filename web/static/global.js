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
