$(document).ready(function(){
    $('.tabs__tab').click(function(){
        $('.tabs__tab').removeClass('tabs__tab_open');
        this.classList.add('tabs__tab_open');
        $('.section').removeClass('section_open');
        var id=$(this).attr('value');
        $('#' + id).addClass('section_open');
    });
});
