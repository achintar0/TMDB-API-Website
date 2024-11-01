$(document).on('click', '.watchlist-add-btn', function(){
    var item_id = $(this).data('item-id');
    var media_type = $(this).data('media-type');
    var item_title = $(this).data('item-title');
    var item_poster = $(this).data('item-poster');
    var item_rating = $(this).data('item-rating');

    $.ajax({
        type: "POST",
        url: addToWatchlistURL,
        data: {
            "item_id":item_id,
            "title": item_title,
            "media_type":media_type,
            "vote_average": item_rating,
            "poster_url": item_poster,
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

$(document).on('click', '.watchlist-remove-btn', function(){
    var item_id = $(this).data('item-id');
    var media_type = $(this).data('media-type');
    var item_title = $(this).data('item-title');
    var item_poster = $(this).data('item-poster');
    var item_rating = $(this).data('item-rating');

    $.ajax({
        type: "POST",
        url: addToWatchlistURL,
        data: {
            "item_id":item_id,
            "title": item_title,
            "media_type":media_type,
            "vote_average": item_rating,
            "poster_url": item_poster,
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