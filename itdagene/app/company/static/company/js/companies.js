$(document).ready(function () {
    $("#status").change(function () {
        filter_companies();
        return false;
    });
    function filter_companies() {
        var show = $("#status option:selected").text();
        $("table.filtered").children().children("tr").each(function () {
            if (show == "All") {
                $(this).removeClass("hidden");
            }
            else if ($(this).children("td:nth-child(2)").text().indexOf(show) != -1) {
                    $(this).removeClass("hidden");
            } else if ($(this).is(":first-child")) {
                $(this).removeClass("hidden");
            } else {
                $(this).addClass("hidden");
            }
        });
    }
});