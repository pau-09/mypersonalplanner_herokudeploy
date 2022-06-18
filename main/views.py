import json
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from users.models import BookList, MovieList


@login_required(login_url="login")
def mainView(request):
    STATES = {
        "Completados": ["Completado", "Completada"],
        "En proceso": ["En proceso", "En proceso"],
        "Abandonados": ["Abandonado", "Abandonada"],
        "En espera": ["En espera", "En espera"],
    }
    summaryData = [
        ["Estado", "Libros", "Películas"],
    ]

    user = request.user
    total_book_count = BookList.objects.filter(user_id=user.id).count()
    total_movie_count = MovieList.objects.filter(user_id=user.id).count()

    for state in STATES:
        book_count = BookList.objects.filter(
            user_id=user.id, state=STATES[state][0]
        ).count()
        movie_count = MovieList.objects.filter(
            user_id=user.id, state=STATES[state][1]
        ).count()
        summaryData.append([state, book_count, movie_count])

    summaryData = json.dumps(summaryData)
    context = {
        "summaryData": summaryData,
        "total_book_count": total_book_count,
        "total_movie_count": total_movie_count,
    }

    return render(request, "main.html", context)
