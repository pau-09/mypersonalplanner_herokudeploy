from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Movie
from users.models import MovieList

# Create your views here.
@login_required(login_url='login')
def moviesView(request):
    usermovies = MovieList.objects.filter(user_id=request.user.id)
    movies = [Movie.objects.get(id=movie.movie_id) for movie in usermovies]

    context = {
        'movies': movies
    }

    # return render(request, 'list_summary.html', context)
    return render(request, 'detail_list.html', context)
    
@login_required(login_url='login')
def movieListDetailView(request, state):
    STATES = {
        'completas' : ['Completado','completadas'],
        'en-proceso' : ['En proceso', 'en proceso'],
        'abandonadas' : ['Abandonado', 'abandonadas'],
        'en-espera' : ['En espera', 'en lista de espera'],
    }

    usermovies = MovieList.objects.filter(user_id=request.user.id, state=STATES[state][0])
    movies = [Movie.objects.get(id=movie.movie_id) for movie in usermovies]

    context = {
        'title': STATES[state][1],
        'movies': movies
    }

    return render(request, 'detail_list.html', context)
