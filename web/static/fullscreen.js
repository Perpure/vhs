$(document).ready(function(){
$("img, div").click(function() {
  var doc = window.document;
  var docEl = doc.documentElement;
  
  var requestFullScreen = docEl.requestFullscreen || docEl.mozRequestFullScreen || docEl.webkitRequestFullScreen;
  var cancelFullScreen = doc.exitFullscreen || doc.mozCancelFullScreen || doc.webkitExitFullscreen;
  
  if(!doc.fullscreenElement && !doc.mozFullScreenElement && !doc.webkitFullscreenElement) { 
    requestFullScreen.call(docEl);
  }
  else {
    cancelFullScreen.call(doc);  
  }
});
});
