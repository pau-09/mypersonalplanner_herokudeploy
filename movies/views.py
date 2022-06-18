import json

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from users.models import MovieList
from .models import Movie


@login_required(login_url="login")
def moviesView(request):
    """
    Movies general view.
    Will display 3 grafics:
        1. Count of movies on each list states.
        2. Count of distinct directors added on each state lists.
        3. Count of each movie genres added.
    """

    statesData = _get_movies_states_count_as_json(request.user)
    directorsData = _get_directors_count_as_json(request.user)
    genresData = _get_genres_count_as_json(request.user)
    total_count = MovieList.objects.filter(user_id=request.user.id).count()

    context = {
        "entry_type": "películas",
        "statesData": statesData,
        "directorsData": directorsData,
        "genresData": genresData,
        "total_count": total_count,
    }

    return render(request, "list_summary.html", context)


@login_required(login_url="login")
def movieListDetailView(request, state):
    """
    Movies list detail view.
    Will display a table of movies added in list of given state,
    each row displays a movie and will include
    adding, editing and deleting functionalities.
    """

    STATES = {
        "completas": ["Completada", "completadas"],
        "en-proceso": ["En proceso", "en proceso"],
        "abandonadas": ["Abandonada", "abandonadas"],
        "en-espera": ["En espera", "en lista de espera"],
    }
    current_state = STATES[state][0]
    title = f"Películas {STATES[state][1]}"
    toast_title = ""
    user_movielist = list()
    user = request.user

    if request.method == "POST":
        request_keys = request.POST.keys()

        if "movie_id" in request_keys and "new_state" in request_keys:
            movie_id = request.POST["movie_id"]
            new_state = request.POST["new_state"]
            toast_title = _update_movie_state(user, movie_id, new_state)

        elif "delete_id" in request_keys:
            movie_id = request.POST["delete_id"]
            toast_title = _delete_movie_from_list(user, movie_id)

        elif "new_movie_id" in request_keys and "state" in request_keys:
            movie_id = request.POST["new_movie_id"]
            state = request.POST["state"]
            toast_title = _add_movie_to_list(user, movie_id, state)

        user_movielist = MovieList.objects.filter(
            user_id=user.id, state=current_state
        )

        if "order_by" in request_keys:
            column = request.POST["order_by"]
            if column != "id":
                user_movielist = user_movielist.order_by(f"movie__{column}")

    if not user_movielist:
        user_movielist = MovieList.objects.filter(
            user_id=user.id, state=current_state
        )

    movies = [Movie.objects.get(id=movie.movie_id) for movie in user_movielist]
    movies_not_in_user = MovieList.objects.filter(user_id=user.id).values_list(
        "movie_id", flat=True
    )
    queryset_movies_to_add = Movie.objects.exclude(id__in=movies_not_in_user)
    movies_to_add = dict()

    for movie in queryset_movies_to_add:
        movies_to_add[movie.id] = movie.title

    context = {
        "state": current_state,
        "title": title,
        "movies": movies,
        "movies_to_add": movies_to_add,
        "toast_title": toast_title,
    }

    return render(request, "detail_list.html", context)


def _update_movie_state(user, movie_id, new_state):
    """
    Updates the state of a movielist object given:
        1. User.
        2. Movie object id.
        3. New state.

    Checks new state and returns success toast title as string if it's valid,
    doesn't do nothig if it's invalid.
    """
    state_options = ("Completada", "En proceso", "Abandonada", "En espera")

    if new_state in state_options:

        movie = Movie.objects.get(id=movie_id)

        movielist_object = MovieList.objects.get(
            user_id=user.id, movie_id=movie_id
        )
        movielist_object.state = new_state
        movielist_object.save()
        user.save()

        return f"'{movie.title}' ha sido editado con éxito."


def _delete_movie_from_list(user, movie_id):
    """
    Deletes movie as movielist object given:
        1. User.
        2. Movie object id.

    Returns success toast title as string
    """
    movie = Movie.objects.get(id=movie_id)
    user.movies.remove(movie)
    user.save()

    return f"'{movie.title}' ha sido eliminado con éxito."


def _add_movie_to_list(user, movie_id, state):
    """
    Adds movielist object given:
        1. User.
        2. Movie object id.
        3. State.

    Checks new state and returns success toast title as string if it's valid,
    doesn't do nothig if it's invalid.
    """

    state_options = ("Completada", "En proceso", "Abandonada", "En espera")

    if state in state_options:
        movie = Movie.objects.get(id=movie_id)
        user.movies.add(movie)
        movie_in_user_movielist = MovieList.objects.get(
            user_id=user.id, movie_id=movie.id
        )
        movie_in_user_movielist.state = state
        movie_in_user_movielist.save()
        user.save()
        return f"'{movie.title}' ha sido añadido con éxito"


def _get_movies_states_count_as_json(user):
    """
    Gets the count of movies for each state given the user.
    Returns it as json.
    """

    STATES = {
        "Completadas": "Completada",
        "En proceso": "En proceso",
        "Abandonadas": "Abandonada",
        "En espera": "En espera",
    }
    statesData = [
        ["Estado", "Películas"],
    ]

    for state in STATES:
        movie_count = MovieList.objects.filter(
            user_id=user.id, state=STATES[state]
        ).count()
        statesData.append([state, movie_count])

    statesData = json.dumps(statesData)
    return statesData


def _get_directors_count_as_json(user):
    """
    Gets the count of movies for each state given the user.
    Returns it as json.
    """

    STATES = {
        "Completadas": "Completada",
        "En proceso": "En proceso",
        "Abandonadas": "Abandonada",
        "En espera": "En espera",
    }
    directorsData = [
        ["Directores", "Completadas", "En proceso", "Abandonadas", "En espera"],
    ]

    movielist_directors_queryset = MovieList.objects.filter(
        user_id=user.id
    ).values_list("movie_id__director", flat=True)
    distinct_movielist_directors = list(set(movielist_directors_queryset))

    for director in distinct_movielist_directors:
        director_count = [
            director,
        ]
        for state in STATES:
            author_state_count = MovieList.objects.filter(
                user_id=user.id,
                movie_id__director=director,
                state=STATES[state],
            ).count()
            director_count.append(author_state_count)

        directorsData.append(director_count)

    directorsData = json.dumps(directorsData)
    return directorsData


def _get_genres_count_as_json(user):
    GENRES = {
        "Acción": "Acción",
        "Aventuras": "Aventuras",
        "Ciencia Ficción": "Ciencia Ficción",
        "Comedia": "Comedia",
        "Fantasía": "Fantasía",
        "Documental": "Documental",
        "Drama": "Drama",
        "Musical": "Musical",
        "Suspense": "Suspense",
        "Terror": "Terror",
        "Animación": "Animación",
        "Romance": "Romance",
    }

    genres_data = [
        ["Género", "Pekículas"],
    ]

    for genre in GENRES:
        genre_movie_count = MovieList.objects.filter(
            user_id=user.id, movie_id__genre=genre
        ).count()
        genres_data.append([genre, genre_movie_count])

    genres_data = json.dumps(genres_data)
    return genres_data
