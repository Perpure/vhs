var elem=document.getElementById("logoTxt");
var body=document.getElementById("Body");
var wid=body.offsetWidth;
if(wid<=550)elem.innerHTML="VHS";

var searching=false;
var search=document.getElementById("Search");
var searcher=document.getElementById("searcher");
search.addEventListener('click',function(){
    if(searching)
    {
        searcher.style.display="none";
        searching=false;
    }
    else
    {
        if(screen.width>570)
            searcher.style.display="flex";
        else
            searcher.style.display="block";
        searching=true;
    }
});

var holder=document.getElementById("mHolder");
var opned=false;
holder.addEventListener('click',function(){
    var els=document.getElementsByClassName("navMen");
    if(opned)
    {
        for(var i=0;i<els.length;i++)
            els[i].style.display="none";
        holder.style.backgroundColor="rgba(240, 203, 142,0)";
        opned=false;
    }
    else
    {
        for(var i=0;i<els.length;i++)
            els[i].style.display="block";
        holder.style.backgroundColor="rgba(240, 203, 142,0.4)";
        opned=true;
    }
});

var clast=document.getElementsByClassName("navClast");
for(var j=0;j<clast.length;j++){
    clast[j].addEventListener('click',function()
    {
        if(screen.width<570)
        {
            var ins=this.getElementsByClassName("subBtn");
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

function swit(e){
        var elem=e.currentTarget;
        elem.classList.toggle("searcher_field__checked");
        elem.value=Math.abs(elem.value-1);
}

function getCurrentPage() {
    var url = window.location.href;
    var host = "http://"+window.location.host+"/";

    return url.substr(host.length);
}

var start=document.getElementById("startSearch");
var date=document.getElementById("Date");
var views=document.getElementById("byViews");
var key=document.getElementById("searchKey");
var pr_page=getCurrentPage();
var map_needed=false;

views.value=0;
date.value=0;
views.addEventListener('click',swit);
date.addEventListener('click',swit);


    start.addEventListener('click',function(){
        var val = key.value;
        var vw=views.value;
        var dt=date.value;
        if (pr_page == "" ) {
            map_needed=$('#show_video_map').prop('checked');
        }

        if(val=="") val=" ";
        $.ajax({
                       url:"/startSearch",
                       type:"GET",
                       dataType:"html",
                       data: {
                            ask:val,
                            view:vw,
                            dat:dt
                       },
                       success:function(response)
                       {
                            var placer="";
                            var plus=false;
                            response=$.parseHTML(response);
                            var tempDom = $('search').append(response);
                            var maine=$('#Main', tempDom);
                            $(tempDom).empty();
                            $("#Main").html($(maine).html());
                       },
                       error:function(){}
        });
        if (pr_page != "") {
            $.getScript("https://api-maps.yandex.ru/2.1/?lang=ru_RU", function () {$.getScript('/static/videos_map.js');});
        }
        else {
            $.getScript('/static/videos_map.js');
        }
        pr_page="";

    });
