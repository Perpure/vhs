jQuery(function($){
    $('.tabs__tab').click(function(){
        $(this).parent().children('.tabs__tab_open').each(function(el){
            $(this).removeClass('tabs__tab_open');
            var id = $(this).data('value');
            $('#' + id).removeClass('section_open');
        });
        $(this).addClass('tabs__tab_open');
        var id = $(this).data('value');
        $('#' + id).addClass('section_open');
    });
    $('.tabs').each(function(){
        var id = $(this).data('value');
        $(this).children('label:eq('+id+')').click();
    });
});
