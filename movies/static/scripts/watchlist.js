$(document).on('click', '.watchlist-add-btn', function(){
    var item_id = $(this).data('item-id');
    var media_type = $(this).data('media-type');


    $.ajax({
        type: "POST",
        url: "add-to-watchlist/",
        data: {
            "item_id":item_id,
            "media_type":media_type,
        },
        headers: {
            "X-CSRFToken": csrfToken
        },
        success: function (response) {
            if (response.success)
                alert(response.message);
            else
                alert(response.message);
        }
    });
});