var searching = false;
var searcher = $("#searcher");

$('#Search').click(function(){
    if(searching)
    {
        searcher.hide();
        searching = false;
    }
    else
    {
        if(screen.width > 570)
        {
            searcher.css('display', "flex");
        }
        else
        {
            searcher.show();
        }
        searching = true;
    }
});

function swit(e){
    var elem = $(e.currentTarget);
    elem.toggleClass("searcher__field_checked");
    elem.val(Math.abs(elem.val() - 1));
}

function getCurrentPage() {
    var url = window.location.href;
    var host = "http://"+window.location.host+"/";

    return url.substr(host.length);
}

var pr_page=getCurrentPage();
var map_needed=false;

var date = $("#Date");
var views = $("#byViews");

views.val(0);
date.val(0);

views.click(swit);
date.click(swit);

$('#startSearch').click(function(){
    var val = $("#searchKey").val();
    var vw = views.val();
    var dt = date.val();
    var sort = "";

    if( dt != 0)
    {
        sort += "date";
    }
    if(vw != 0)
    {
        sort += "views";
    }
    if(! sort)
    {
        sort = "empty";
    }

    val = val.replace('#', '*');

    if(val == "")
    {
        window.location="/";
    }
    else
    {
        window.location="/search/" + val + "/" + sort;
    }

    /*if (pr_page == "" ) {
        map_needed = $('#show_video_map').prop('checked');
    }
    if (pr_page != "") {
        $.getScript("https://api-maps.yandex.ru/2.1/?lang=ru_RU", function () {$.getScript('/static/videos_map.js');});
    }
    else {
        $.getScript('/static/videos_map.js');
    }
    pr_page="";*/
});
