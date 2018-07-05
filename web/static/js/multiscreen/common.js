var wait_time=5000;

$(document).ready(function(){
    $("#instructionBtn").click(function(){
    $("#instruction").slideToggle("slow",function(){});
  });});

  function fullscreen() {
      var isInFullScreen = (document.fullscreenElement && document.fullscreenElement !== null) ||
          (document.webkitFullscreenElement && document.webkitFullscreenElement !== null) ||
          (document.mozFullScreenElement && document.mozFullScreenElement !== null) ||
          (document.msFullscreenElement && document.msFullscreenElement !== null);

      var docElm = document.documentElement;
      if (!isInFullScreen) {
          if (docElm.requestFullscreen) {
              docElm.requestFullscreen();
          } else if (docElm.mozRequestFullScreen) {
              docElm.mozRequestFullScreen();
          } else if (docElm.webkitRequestFullScreen) {
              docElm.webkitRequestFullScreen();
          } else if (docElm.msRequestFullscreen) {
              docElm.msRequestFullscreen();
          }
      } else {
          if (document.exitFullscreen) {
              document.exitFullscreen();
          } else if (document.webkitExitFullscreen) {
              document.webkitExitFullscreen();
          } else if (document.mozCancelFullScreen) {
              document.mozCancelFullScreen();
          } else if (document.msExitFullscreen) {
              document.msExitFullscreen();
          }
      }
  }

$("#fullS").click(fullscreen);

$(document).ready(function() {
    var ratio = window.devicePixelRatio || 1;
    var width = screen.width * ratio;
    var height = screen.height * ratio;
    $.ajax({
        url: '/tellRes',
        contentType: "application/json; charset=utf-8",
        type: "POST",
        dataType:"json",
        data: JSON.stringify({ "width": width, "height" : height }),
        success: function () {
            console.log(JSON.stringify({ "width": width, "height" : height }));},
    });
});

function countDown(Time)
{
    $('#cod').css("margin-top","10px");
    setTimeout(function step(){
        Time--;
        $('#cod').html("<h5>Показ начнётся через: " + Time + "с</h5>");
        if(Time)setTimeout(step,1000);
        else $('#cod').empty();
    },1000);
}
