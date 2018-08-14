function search(word, date, name, geo)
{
    date = date || 0;
    name = name || 0;
    geo = geo || false;
    word = word || "___empty___";
    var result;
    $.ajax({
        url: "/search_videos",
        type: "POST",
        dataType: "json",
        async: false,
        data:
        {
            search: word,
            date: date,
            name: name,
            geo_need: geo
        },
        success: function(response) {
            result = response;
        }
    });
    return result;
};
