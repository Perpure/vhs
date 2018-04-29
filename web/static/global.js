let elem=document.getElementById("logoTxt");
let body=document.getElementById("Body");
let wid=body.offsetWidth;
if(wid<=1400)elem.innerHTML="VHS";

function move(){
        let Height=document.body.scrollHeight;
        let foot=document.getElementById("Footer");
        foot.style.top=(Height-130)+"px";
}

setTimeout(move,2000);

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
