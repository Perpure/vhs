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

var map_needed=false;

var date = $("#Date");
var views = $("#byViews");

views.val(0);
date.val(0);

views.click(swit);
date.click(swit);

function search(word,sort)
{
    if(sort == null || sort == "")
    {
        sort = "empty";
    }
    if(word == "" || word == null)
    {
        word = "empty";
    }
    word = word.replace('#', '*');
    window.location="/search/" + word + "/" + sort;
}

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

    search(val, sort);
});
