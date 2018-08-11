jQuery(function($) {
    $('.switcher__radio').change(function () {
        var switcherRadio = $(this),
            switcher = switcherRadio.parents('.switcher');
        switcher.find('.switcher__arm')
            .removeClass('switcher__arm_inv');
        switcherRadio.parents('.switcher__arm')
            .addClass('switcher__arm_inv');
        switcher.trigger('switch', [switcherRadio.val()]);
    });
});
