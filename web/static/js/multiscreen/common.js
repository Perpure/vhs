var wait_time=5000;

$(document).ready(function(){
    $("#instructionBtn").click(function(){
    $("#instruction").slideToggle("slow",function(){});
  });});

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
