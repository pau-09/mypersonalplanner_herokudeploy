import json

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from users.models import BookList, MovieList

# Create your views here.
@login_required(login_url='login')
def mainView(request):
    BOOK_STATES = {"Completados": 'Completado', 'En proceso': 'En proceso', 
                   "Abandonados": 'Abandonado', 'En espera': 'En espera'}
    MOVIE_STATES = {'Completadas': 'Completada', 'En proceso': 'En proceso', 
                   'Abandonadas': 'Abandonada', 'En espera': 'En espera'}

    books = [['Estado', 'Libros'],]
    movies = [['Estado', 'Películas'],]
    user = request.user
    for state in BOOK_STATES:
        book_count = BookList.objects.filter(user_id=user.id, state=BOOK_STATES[state]).count()
        books.append([state, book_count])

    for state in MOVIE_STATES:
        movie_count = MovieList.objects.filter(user_id=user.id, state=MOVIE_STATES[state]).count()
        movies.append([state, movie_count])
    
    books = json.dumps(books)
    movies = json.dumps(movies)

    context = {
        'books': books,
        'movies': movies

    }
    return render(request, 'main.html', context)
    