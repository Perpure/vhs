jQuery(function($){
    $(".slider__btn").click(function(){
        $(this).parent().children(".slider__content").slideToggle("slow", function(){});
    });
});
