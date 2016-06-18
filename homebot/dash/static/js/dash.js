/**
 * Created by syamil on 18/6/16.
 */
var reloadHour = 4;
var secondsSinceLoad = 0;

function StartTime() {
    var today = new Date();

    $("div.clock").html(today.getHours() + ":" + ToDoubleDigits(today.getMinutes()));
    $("a.date").html(today.toDateString());

    if (today.getHours() == reloadHour && today.getMinutes() == 0 && secondsSinceLoad > 600) {	// The extra checks besides reloadHour are to make sure we don't reload every second when we hit reloadHour
        window.location.reload(true);
    }

    secondsSinceLoad++;

    setTimeout(function () {
        StartTime()
    }, 1000);
}

function ToDoubleDigits(i) {
    if (i < 10) {
        i = "0" + i
    }
    return i;
}

StartTime();