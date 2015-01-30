/** @jsx React.DOM */

var React = require('react');

$(document).ready(function() {
    $(window).scroll(function () {
        console.log($(".navbar").offset().top);
        if ($(".navbar").offset().top > 50) {
            $(".navbar-fixed-top").addClass("top-nav-collapse");
        } else {
            $(".navbar-fixed-top").removeClass("top-nav-collapse");
        }
    });
});
