var flashMessage = function(message, type) {
    $('#page-content-wrapper').prepend("<div class=\"alert alert-" + type + "\">" +
        "<button type=\"button\" class=\"close\" data-dismiss=\"alert\" aria-hidden=\"true\">&times;</button>" + message +
        "</div>");
};

$(document).ready(function() {
    $('#flush-cache').click(function() {
        if (confirm('Are you sure you want to flush the cache?')) {
            $.ajax({
                type: 'GET',
                url: '/api/admin/cache/flush'
            }).success(function(data) {
                flashMessage("Cache cleared", "success");
            }).error(function(data) {
                flashMessage("Something went wrong: " + data, "danger");
            })
        }
    });
});