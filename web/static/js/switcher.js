jQuery(function($) {
    $('.switcher__radio').change(function () {
        var me = $(this);
        me.parent().parent().addClass('switcher__arm_inv');
        me.parent().parent().parent().children('.switcher__arm').each(function(index){
            var radio = $(this).children('.switcher__label').children('.switcher__radio');
            if(radio.get(0).checked == false)
            {
                $(this).removeClass('switcher__arm_inv');
                $('#' + radio.val()).show();
            }
            else
            {
                $('#' + radio.val()).hide();
            }
        });
        me.parent().parent().parent().trigger('action');
    });
});
