

$(document).ready(function(){
    const searchUrl = $('#searchInput').data('url');

    $('#searchInput').on('keyup', function(){
        let query = $(this).val();

        if (query.length > 0){
            $.ajax({
                url: searchUrl,
                data: {
                    'query':query,
                },
                dataType: 'json',
                success: function(data){
                    console.log(data)
                    $('#movieResults').empty();
                    data.searchMovies.slice(0,4).forEach(function(movie){
                        $('#movieResults').append(
                            `<a href="${"movie/"+movie.movie_id}" class="search-bar-item">
                            <div class="dynamic-search-img">
                                <img src="${movie.poster_url}" alt="">
                            </div>
                            <div class="dynamic-search-info">
                                <span class="dynamic-search-title">${movie.title}</span>
                                <span class="dynamic-search-date">${movie.formatted_release_date}</span>
                            </div>
                            </a>`
                        );
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