// This is required to build the css
require("./../styl/itdagene.styl");

$(document).ready(function() {
  $(window).scroll(function() {
    if ($(".navbar").offset().top > 50) {
      $(".navbar-fixed-top").addClass("top-nav-collapse");
    } else {
      $(".navbar-fixed-top").removeClass("top-nav-collapse");
    }
  });

  var companiesContainer = $(".companies-holder");
  if (companiesContainer.length == 1) {
    var buttons = $(".btn-days");
    buttons.click(function(e) {
      var self = $(this);
      buttons.removeClass("active");
      self.addClass("active");
    });
  }
});
