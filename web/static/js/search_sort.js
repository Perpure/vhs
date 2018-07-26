$('#sort').click(function() {
    var date = $("input[name=byDate]:checked").val();
    var name = $("input[name=byName]:checked").val();
    var sort = "";

    switch (date) {
      case '1':
        sort += "date";
        break;
      case '2':
          sort += "date_asc";
    }
    switch (name) {
      case '1':
          sort += "name";
          break;
      case '2':
          sort += "name_asc";
    }

    search(cur_search, sort);
});
