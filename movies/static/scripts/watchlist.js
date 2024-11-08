//add btn click
$(document).on('click', '.watchlist-add-btn', function(){

    var item_id = $(this).data('item-id');
    var media_type = $(this).data('media-type');
    var item_title = $(this).data('item-title');
    var item_poster = $(this).data('item-poster');
    var item_rating = $(this).data('item-rating');

    var btnClicked = $(this);

    if(loggedIn == false){
        window.location.href = loginURL;
        return;
    }

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
            $(btnClicked).hide();
            $(btnClicked.prev()).show();
        }
    });
});

//remove btn click
$(document).on('click', '.watchlist-remove-btn', function(){
    const windowLocation = window.location.href;
    //temporal solution
    const watchlistURL = "http://127.0.0.1:8000/watchlist/"

    var item_id = $(this).data('item-id');
    var item_title = $(this).data('item-title');
    var btnClicked = $(this);
    
    var deletePrompt = window.confirm(`Remove "${item_title}" from the watchlist?`);
    
    if (deletePrompt){
        $.ajax({
            type: "POST",
            url: removeFromWatchlistURL,
            data: {
                "item_id":item_id,
            },
            headers: {
                "X-CSRFToken": csrfToken
            },
            success: function (response) {
                if (windowLocation === watchlistURL)
                    btnClicked.closest('.item-card').remove();
                else{
                    $(btnClicked).hide();
                    $(btnClicked.next()).show();
                }
            }
        });
    }     
});