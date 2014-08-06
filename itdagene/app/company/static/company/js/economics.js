$(document).ready(function() {

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = $.trim(cookies[i]);
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    $(".is-billed-button").click(function(){
        var span = $(this).children("span");
        if(span.attr("alt") == "yes"){
            setBilledStatus(false, $(this).attr("data-company-id"));
            // We assume 100% success rate
            $(this).removeClass("btn-success");
            $(this).addClass("btn-danger");
            span.removeClass("glyphicon-ok");
            span.addClass("glyphicon-remove");
            span.attr("alt", "no");
        } else {
            setBilledStatus(true, $(this).attr("data-company-id"));
            $(this).removeClass("btn-danger");
            $(this).addClass("btn-success");
            span.removeClass("glyphicon-remove");
            span.addClass("glyphicon-ok");
            span.attr("alt", "yes");
        }

    });

    function setBilledStatus(value, id){
        if(value){
            var url = "/bdb/economics/" + id + "/billed/"
        } else {
            var url = "/bdb/economics/" + id + "/not-billed/"
        }
        $.ajax({
            url: url,
            type: "POST",
            crossdomain: false,
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
            },
            success: function(msg){

            },
            error: function(msg){
                $('#ajax-error').html("<ul class=\"errorlist\"><li>" + msg.statusText + "</li></ul>");
            },
            complete: function(){

            }

        });
    }
    $(".is-paid-button").click(function(){
        var span = $(this).children("span");
        if(span.attr("alt") == "yes"){
            setPaidStatus(false, $(this).attr("data-company-id"));
            $(this).removeClass("btn-success");
            $(this).addClass("btn-danger");
            span.removeClass("glyphicon-ok");
            span.addClass("glyphicon-remove");
            span.attr("alt", "no");
        } else {
            setPaidStatus(true, $(this).attr("data-company-id"));
            $(this).removeClass("btn-danger");
            $(this).addClass("btn-success");
            span.removeClass("glyphicon-remove");
            span.addClass("glyphicon-ok");
            span.attr("alt", "yes");
        }

    });

    function setPaidStatus(value, id){
        if(value){
            var url = "/bdb/economics/" + id + "/paid/"
        } else {
            var url = "/bdb/economics/" + id + "/not-paid/"
        }
        $.ajax({
            url: url,
            type: "POST",
            crossdomain: false,
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
            },
            success: function(msg){

            },
            error: function(msg){
                $('#ajax-error').html("<ul class=\"errorlist\"><li>" + msg.statusText + "</li></ul>");
            },
            complete: function(){

            }

        });
    }
});