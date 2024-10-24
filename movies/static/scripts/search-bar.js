$(document).ready(function(){
    const searchURL = $('#searchInput').data('url');

    $('#searchInput').on('keyup', function(){
        let query = $(this).val();
        let movieName;

        if (query.length > 0){
            $.ajax({
                url: searchURL,
                data: {
                    'query':query,
                },
                dataType: 'json',
                success: function(data){
                    $('#movieResults').empty();
                    data.searchBarItems.slice(0,4).forEach(function(item){
                        $('#movieResults').append(
                            `<a href="" class="search-bar-item" data-id="${item.item_id}" data-type="${item.media_type}">
                            <div class="dynamic-search-img">
                                <img src="${item.poster_url}" alt="">
                            </div>
                            <div class="dynamic-search-info" >
                                <span class="dynamic-search-title">${item.title}</span>
                                <span class="dynamic-search-date">${item.release_date}</span>
                                <span class="dynamic-search-mtype">${item.media_type}</span>
                            </div>
                            </a>`
                        );
                    });
                    $('.search-bar-item').on('click', function(e) {
                        e.preventDefault(); // Prevent default anchor behavior

                        let id = $(this).data('id');
                        let type = $(this).data('type');

                        // Construct absolute path for movie or TV show
                        let targetUrl = `/${type}/${id}/`;

                        // Redirect to the correct detail page
                        window.location.href = targetUrl;
                    });
                }
            });
            $('#movieResults').show();
        }
        else{
            $('#movieResults').hide();
            $('#movieResults').empty();
        }
    });
});

$(document).click(function (event) { 
    if (event.target !== ($('#searchInput') && $('#movieResults'))){
        $('#movieResults').hide();
    }
});