$(document).ready(function(){
    var now = new Date();
    // init time value
    $("#releasetime").val(getTimeString(now));
    
    // init clockpicker
    $("#releasetime").clockpicker({
      donetext: 'Okay',
      autoclose:true
    });
    
    // callback on change the time
    $("input#releasetime").change(function(e){
      e.preventDefault();
      var timestr = $(this).val();
      var now = new Date();
      if(!isValidTimeString(timestr)){
        $(this).val(getTimeString(now));
      }
      // create a date for release, to compare ...
      var release = new Date();
      release.setHours(parseInt(timestr.split(":")[0]));
      release.setMinutes(parseInt(timestr.split(":")[1]));
      release.setSeconds(0);
      console.log(release);
      console.log(now);
      // ... with now
      if(now >= release){
        $("body").addClass("valid").removeClass("invalid");
      }else{
        $("body").addClass("invalid").removeClass("valid");
      }
    });
    
    // click to open...
    $(".input-group.clockpicker").click(function(e){
      e.stopPropagation();
      $("#releasetime").clockpicker('show');
    });
    
    // init first validation 
    $("input#releasetime").trigger("change");
    
    // set interval for validation after time
    setInterval(function(){ 
      $("input#releasetime").trigger("change");
    },1000);
    
  }); // end document ready
  
  // helper: get string from date (format: hh:mm)
  function getTimeString(datetime){
    var hours = datetime.getHours();
    var minutes = datetime.getMinutes();
    if(parseInt(hours) < 10){
      hours = "0" + hours;
    }
    if(parseInt(minutes) < 10){
      minutes = "0" + minutes;
    }
    return hours + ":"  + minutes;
  };
  
  // helper: is time string valid? (format: hh:mm)
  function isValidTimeString(timestr){
    var hours = timestr.split(":")[0];
    var minutes = timestr.split(":")[1];
    if(parseInt(hours) >= 0 && parseInt(hours) <= 24 && parseInt(minutes) >= 0 && parseInt(minutes) <=59 ){
      return true;
    }
    return false;
  };