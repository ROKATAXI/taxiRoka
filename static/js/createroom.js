$(document).ready(function(){
    $("input[name='seat_num']").change(function() {
        // Reset all images
        $(".seat-option img").attr("src", "{% static 'img/seat.png' %}");
        
        // Change image for selected option
        var selectedSeat = $(this).val();
        $(".seat-option:nth-child(" + selectedSeat + ") img").attr("src", "{% static 'img/selected_seat.png' %}");
    });