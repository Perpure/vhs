var opened=false;
$('#mHolder').click(function(){
    if(opened)
    {
        $('.nav-menu__nav-men').hide();
        $(this).css('backgroundColor', 'rgba(240, 203, 142,0)');
        opened=false;
    }
    else
    {
        $('.nav-menu__nav-men').show();
        $(this).css('backgroundColor', 'rgb(73, 69, 59)');
        opened=true;
    }
});

if(screen.width<570)
{
  $('.nav-menu__nav-men_nav-clast').click(function()
  {
      if($(this).css('height') != '50px')
      {
          $(this).css('height', '50px');
      }
      else
      {
          var height = $(this).find('.nav-menu__sub-btn').length * 50 + 60 + "px";
          $(this).css('height', height);
      }
  });
  $('.nav-menu__nav-men_nav-clast').mouseout(function()
  {
      $(this).css('height', '50px');
  });
}
