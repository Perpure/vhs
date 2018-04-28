let elem=document.getElementById("logoTxt");
let body=document.getElementById("Body");
let wid=body.offsetWidth;
if(wid<=1200)elem.innerHTML="VHS";

let Height=document.body.scrollHeight;
let foot=document.getElementById("Footer");
foot.style.top=(Height-130)+"px";
