var geo_videos = false;
jQuery(function($) {
  $('#videos_map').on('ready', function(){
    function Search(request, date, name)
    {
      var video_pack = search(request, date, name, 1);
      add_geotags(JSON.parse(video_pack[1]));
      video_pack[0] = JSON.parse(video_pack[0])

      var table_section = $('#all');
      table_section.empty();
      for(var i in video_pack[0])
      {
          var cur = video_pack[0][i];
          var video = $('<div class="video"></div>');
          var prev = $('<div class="video__preview"><a href="' + cur['link'] + '"><img src="' + cur['preview'] + '" href="' + cur['link'] + '" class="video__preview-img"></a></div>');
          var text = $('<div></div>');
          var title = $('<a href="' + cur['link'] + '"><p class="video__title" title="' + cur['title'] + '">' + cur['title'] + '</p></a>');
          var data = $('<a href="/cabinet/' + cur['author_login'] + '"><p class="italic">' + cur['author'] + '<br>' + cur['views'] + ' просмотров <br>' + cur['date'] + '</p></a>')
          video.append(prev);
          text.append(title);
          text.append(data);
          video.append(text);
          table_section.append(video);
      }
    }

    $('#startSearch').click(function() {
        var request = $('#searchKey').val();
        var date = $("input[name=byDate]:checked").val();
        var name = $("input[name=byName]:checked").val();

        Search(request, date, name);
    });

      if(presearch)
        {
            Search(presearch, 0, 0, 1);
        }
    });
});
