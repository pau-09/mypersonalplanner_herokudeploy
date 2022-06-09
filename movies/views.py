import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from users.models import MovieList
from .models import Movie

# Create your views here.
@login_required(login_url='login')
def moviesView(request):
    statesData = _get_movies_states_count_as_json(request.user)
    directorsData = _get_directors_count_as_json(request.user)
    genresData = _get_genres_count_as_json(request.user)

    context = {
        'entry_type': 'películas',
        'statesData': statesData,
        'authorsData': directorsData,
        'genresData': genresData,
    }

    return render(request, 'list_summary.html', context)
    # return render(request, 'detail_list.html', context)
    
@login_required(login_url='login')
def movieListDetailView(request, state):
    STATES = {
        'completas' : ['Completada','completadas'],
        'en-proceso' : ['En proceso', 'en proceso'],
        'abandonadas' : ['Abandonada', 'abandonadas'],
        'en-espera' : ['En espera', 'en lista de espera'],
    }
    toast = ''
    user_movielist = list()

    if request.method == 'POST':
        user = request.user
        toast_title = ''
        request_keys = request.POST.keys()

        if 'movie_id' in request_keys and request.POST['new_state'] in ('Completada', 'En proceso', 'Abandonada', 'En espera'):
            movie_id = request.POST['movie_id']
            movie = MovieList.objects.get(user_id=user.id, movie_id=movie_id)

            movie.state = request.POST['new_state']
            movie.save()
            user.save()
            toast_title = f"'{Movie.objects.get(id=movie_id).title}' ha sido editada con éxito."
            print(request.POST);

        elif 'delete_id' in request_keys:
            movie_id = request.POST['delete_id']
            movie = Movie.objects.get(id=movie_id)
            user.movies.remove(movie)
            user.save()
            toast_title = f"'{movie.title}' ha sido eliminada con éxito."

        elif 'new_movie_id' in request_keys and request.POST['state'] in ('Completada', 'En proceso', 'Abandonada', 'En espera'):
            movie = Movie.objects.get(id=request.POST['new_movie_id'])
            user.movies.add(movie)
            movie_in_user_movielist = MovieList.objects.get(user_id=user.id, movie_id=movie.id)
            movie_in_user_movielist.state = request.POST['state']
            movie_in_user_movielist.save()
            user.save()
            toast_title = f"'{movie.title}' ha sido añadida con éxito."
        
        if toast_title:
            toast = '''Swal.mixin({{
                        title: "{toast_title}",
                        toast: true,
                        position: 'bottom-right',
                        showConfirmButton: false,
                        timer: 3000,
                        timerProgressBar: true,
                        didOpen: (toast) => {{
                            toast.addEventListener('mouseenter', Swal.stopTimer)
                            toast.addEventListener('mouseleave', Swal.resumeTimer)
                        }},
                        customClass: {{
                            container: 'toast',
                        }},
                        background: '#CDF8B8',
                        color: '#958CAB',
                        target: '#toast_target'
                    }})'''.format_map({'toast_title': toast_title, })

        if 'order_by' in request_keys:
            column = request.POST['order_by']
            if column == 'id':
                user_movielist = MovieList.objects.filter(user_id=request.user.id, state=STATES[state][0])
            else:
                user_movielist = MovieList.objects.filter(user_id=request.user.id, state=STATES[state][0]).order_by(f"movie__{column}")

    if not user_movielist:
        user_movielist = MovieList.objects.filter(user_id=request.user.id, state=STATES[state][0])

    movies = [Movie.objects.get(id=movie.movie_id) for movie in user_movielist]

    movies_not_in_user = MovieList.objects.filter(user_id=request.user.id).values_list('movie_id', flat=True)
    queryset_movies_to_add = Movie.objects.exclude(id__in=movies_not_in_user).order_by('title')
    movies_to_add = {}

    for movie in queryset_movies_to_add:
        movies_to_add[movie.id] = movie.title

    context = {
        'state': STATES[state][0],
        'title': STATES[state][1],
        'movies': movies,
        'movies_to_add': movies_to_add,
        'toast': toast,
    }

    return render(request, 'detail_list.html', context)

def _get_movies_states_count_as_json(user):
    STATES = {
             'Completadas': 'Completada',
             'En proceso': 'En proceso', 
             'Abandonadas': 'Abandonada', 
             'En espera': 'En espera'
             }
    statesData = [['Estado', 'Películas'],]

    for state in STATES:
        movie_count = MovieList.objects.filter(user_id=user.id, state=STATES[state]).count()
        statesData.append([state, movie_count])
    
    statesData = json.dumps(statesData)
    return statesData

def _get_directors_count_as_json(user):
    STATES = {
             'Completadas': 'Completada',
             'En proceso': 'En proceso', 
             'Abandonadas': 'Abandonada', 
             'En espera': 'En espera'
             }
    directorsData = [['Directores', 'Completados', 'En proceso', 'Abandonados', 'En espera'],]

    movielist_directors_queryset = MovieList.objects.filter(user_id=user.id).values_list('movie_id__director', flat=True)
    distinct_movielist_directors = list(set(movielist_directors_queryset))

    for director in distinct_movielist_directors:
        director_count = [director, ]
        for state in STATES:
            author_state_count = MovieList.objects\
                                            .filter(
                                                    user_id=user.id, 
                                                    movie_id__director=director, 
                                                    state=STATES[state]
                                                    )\
                                            .count()
            director_count.append(author_state_count)
        
        directorsData.append(director_count)
    
    directorsData = json.dumps(directorsData)
    return directorsData

def _get_genres_count_as_json(user):
    GENRES={
        'Acción': 'Acción',
        'Aventuras': 'Aventuras',
        'Ciencia Ficción': 'Ciencia Ficción',
        'Comedia': 'Comedia',
        'Fantasía': 'Fantasía',
        'Documental': 'Documental',
        'Drama': 'Drama',
        'Musical': 'Musical',
        'Suspense': 'Suspense',
        'Terror': 'Terror',
        'Animación': 'Animación',
        'Romance': 'Romance',
    }

    genres_data = [['Género', 'Pekículas'],]
    for genre in GENRES:
        genre_movie_count = MovieList.objects.filter(user_id = user.id, movie_id__genre=genre).count()
        genres_data.append([genre, genre_movie_count])

    genres_data = json.dumps(genres_data)
    return genres_data