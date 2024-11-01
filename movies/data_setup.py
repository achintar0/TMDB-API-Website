from datetime import datetime
from .api_services import TMDBClient
from accounts.models import Watchlist

class DataSetup:
    def setup_response_data(queryData, genre_map, poster_quality, user):
        items = []
        for item in queryData:
                poster_url = f"https://image.tmdb.org/t/p/{poster_quality}{item.get('poster_path')}"
                genre_names = [genre_map.get(genre_id, 'Unknown') for genre_id in item.get('genre_ids', [])]

                if Watchlist.objects.filter(username=user, itemID=item.get('id')).exists():
                     on_watchlist = True
                else:
                     on_watchlist = False

                items.append({
                    'item_id': item.get('id'),
                    'title': item.get('title') or item.get('name'),
                    'release_date': item.get('release_date') or item.get('first_air_date'),
                    'media_type': item.get('media_type'),
                    'vote_average': item.get('vote_average'),
                    'poster_url': poster_url,
                    'genres': genre_names,
                    'popularity': item.get('popularity') or None,
                    'on_watchlist': on_watchlist,
                })

        for item in items:
            if item['release_date']:
                release_date = datetime.strptime(item['release_date'], "%Y-%m-%d")
                item['release_date'] = release_date.strftime("%d %B %Y")
        
        return items

    def setup_item_details(item_id, media_type, user):
        movieDetails = []
        tvshowDetails = []
        
        if media_type == 'movie':
            queryData = TMDBClient.search_movie_details(item_id)

            poster_url = f"https://image.tmdb.org/t/p/w500{queryData['poster_path']}"
            backdrop_url = f"https://image.tmdb.org/t/p/w1280{queryData['backdrop_path']}"

            if Watchlist.objects.filter(username=user, itemID=queryData.get('id')).exists():
                on_watchlist = True
            else:
                on_watchlist = False

            movieDetails = {
                'item_id': queryData['id'],
                'title': queryData['title'],
                'release_date': queryData.get('release_date'),
                'vote_average': queryData.get('vote_average'),
                'genre': queryData['genres'],
                'overview': queryData['overview'],
                'poster_url': poster_url,
                'backdrop_img': backdrop_url,
                'runtimeHours': queryData['runtime'],
                'runtimeMinutes': queryData['runtime'],
                'media_type': media_type,
                'on_watchlist': on_watchlist,
            }

            movieHours = queryData['runtime']//60
            movieMinutes = queryData['runtime']%60

            movieDetails['runtimeHours'] = movieHours
            movieDetails['runtimeMinutes'] = movieMinutes

            release_date = datetime.strptime(movieDetails['release_date'], "%Y-%m-%d")
            movieDetails['release_date'] = release_date.strftime("%d %B %Y")
            
            return movieDetails
        
        else:
            queryData = TMDBClient.search_series_details(item_id)

            poster_url = f"https://image.tmdb.org/t/p/w500{queryData['poster_path']}"
            backdrop_url = f"https://image.tmdb.org/t/p/w1280{queryData['backdrop_path']}"\
            
            if Watchlist.objects.filter(username=user, itemID=queryData.get('id')).exists():
                on_watchlist = True
            else:
                on_watchlist = False

            tvshowDetails = {
                'title': queryData['name'],
                'release_date': queryData['first_air_date'],
                'vote_average': queryData['vote_average'],
                'genre': queryData['genres'],
                'overview': queryData['overview'],
                'poster_url': poster_url,
                'backdrop_img': backdrop_url,
                'number_of_seasons': queryData['number_of_seasons'],
                'number_of_episodes': queryData['number_of_episodes'],
                'media_type': media_type,
                'on_watchlist': on_watchlist,
            }

            release_date = datetime.strptime(tvshowDetails['release_date'], "%Y-%m-%d")
            tvshowDetails['release_date'] = release_date.strftime("%d %B %Y")

            return tvshowDetails