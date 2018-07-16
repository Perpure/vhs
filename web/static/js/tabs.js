jQuery(function($){
    $('.tabs__tab').click(function(){
        $('.tabs__tab').removeClass('tabs__tab_open');
        $(this).addClass('tabs__tab_open');
        $('.section').removeClass('section_open');
        var id = $(this).data('value');
        $('#' + id).addClass('section_open');
    });
    $('.tabs__tab')[$("#Tabs").data('value')].click();
});
