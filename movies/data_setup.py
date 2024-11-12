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
    


    # Movies
        # Created by: NO
        # Crew[]: YES
        # Jobs[Writer, Director]
    # Series
        # Created by: YES
        # Crew[]: YES
        # Jobs[Producer, Novel]

    def setup_item_details(item_id, media_type, user):
        itemDetails = []
        productionCompanies = []
        seriesCreators = []
        movieCreators = []
        top4Cast = []

        videoTrailer = None
        
        queryData = TMDBClient.search_item_details(item_id, media_type)
        creditsData = TMDBClient.fetch_credits(item_id, media_type)
        videoData = TMDBClient.search_item_videos(item_id, media_type)

        crewData = creditsData.get('crew', [])

        if media_type == 'tv':
            seriesCreators = queryData.get('created_by', [])
        else:
            for crew in crewData:
                exists = False
                for creator in movieCreators:
                    if crew['name'] == creator['name']:
                        exists = True
                        break
                if (crew['job'] == 'Writer' or crew['job'] == 'Director' or crew['job'] == 'Producer') and exists == False:
                    movieCreators.append({
                        'name':crew['name'],
                        'job': crew['job'],
                        'popularity': crew['popularity'],
                    })                

        movieCreators = sorted(movieCreators, key=lambda x: x['popularity'], reverse=True)
            
        for video in videoData:
            if video['type'] == 'Trailer' and video['site'] == 'YouTube':
                videoTrailer = video['key']
                break

        poster_url = f"https://image.tmdb.org/t/p/w500{queryData['poster_path']}"
        
        for company in queryData['production_companies']:
            company_logo = f"https://image.tmdb.org/t/p/w500{company['logo_path']}"

            productionCompanies.append({
                'id': company['id'],
                'company_name': company['name'],
                'company_logo': company_logo or None,
            })

        backdrop_url = f"https://image.tmdb.org/t/p/w1280{queryData['backdrop_path']}"

        if Watchlist.objects.filter(username=user, itemID=queryData.get('id')).exists():
            on_watchlist = True
        else:
            on_watchlist = False

        itemDetails = {
            'item_id': queryData['id'],
            'title': queryData.get('title') or queryData.get('name'),
            'release_date': queryData.get('release_date') or queryData.get('first_air_date'),
            'vote_average': queryData.get('vote_average'),
            'genre': queryData['genres'],
            'overview': queryData['overview'],
            'poster_url': poster_url,
            'backdrop_img': backdrop_url,
            'runtimeHours': queryData.get('runtime') or None,
            'runtimeMinutes': queryData.get('runtime') or None,
            'number_of_seasons': queryData.get('number_of_seasons') or None,
            'number_of_episodes': queryData.get('number_of_episodes') or None,
            'media_type': media_type,
            'on_watchlist': on_watchlist,
            'video_url': videoTrailer,
            'production_companies': productionCompanies,
            'movieCreators': movieCreators[slice(3)],
            'seriesCreators': seriesCreators
        }

        if itemDetails['media_type'] == 'movie':
            movieHours = queryData['runtime']//60
            movieMinutes = queryData['runtime']%60

            itemDetails['runtimeHours'] = movieHours
            itemDetails['runtimeMinutes'] = movieMinutes

        release_date = datetime.strptime(itemDetails['release_date'], "%Y-%m-%d")
        itemDetails['release_date'] = release_date.strftime("%d %B %Y")
        
        return itemDetails