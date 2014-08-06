$(document).ready(function () {
    $("input[name=type]").change(function () {
        filter();
        return false;
    });

    $("select[name=place]").change(function () {
        filter();
        return false;
    });
    function filter() {
        var type = $("input[name=type]:checked").attr("value");
        var place = $("select[name=place]").val();
        $("#joblistingstable").children("tbody").children("tr").each(function () {
            if (type == "all" && place == "all") {
                $(this).removeClass("hidden");
            }
            else if (type == "all") {
                if ($(this).attr("data-job-place").indexOf(place) != -1) {
                    $(this).removeClass("hidden");
                } else {
                    $(this).addClass("hidden");
                }
            }
            else if (place == "all") {
                if ($(this).attr("data-job-type") == type) {
                    $(this).removeClass("hidden");
                } else {
                    $(this).addClass("hidden");
                }
            }
            else {
                if ($(this).attr("data-job-place").indexOf(place) != -1 && $(this).attr("data-job-type") == type) {
                    $(this).removeClass("hidden");
                } else {
                    $(this).addClass("hidden");
                }
            }
        });
    }
    filter();
});