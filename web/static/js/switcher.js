jQuery(function($) {
    $('.switcher__radio').change(function () {
        var me = $(this);
        me.parents('.switcher__arm').addClass('switcher__arm_inv');
        me.parents('.switcher').children('.switcher__arm').each(function(index){
            var radio = $(this).children('.switcher__label').children('.switcher__radio');
            if(radio.is(':checked') == false)
            {
                $(this).removeClass('switcher__arm_inv');
            }
        });
        me.parents('.switcher').trigger('action');
    });
});
