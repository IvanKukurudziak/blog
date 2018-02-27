$(document).ready(function(){
    $("#search-form").keyup(function () {

        var form = $(this);
        var data = form.serializeArray();
        var url = '/search'
        var q = $("#q").val();
        var searchResults = $("#searchResults");
        $.ajax({
            method: 'GET',
            url:url,
            data:data,
            success: function (data) {
                searchResults.html(data);
                return (data);
            }
        })
    });

    $('#search-form').submit(function() {
        return false;
    });
});
