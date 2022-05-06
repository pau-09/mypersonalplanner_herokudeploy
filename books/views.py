from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from books.models import Book

# Create your views here.
@login_required(login_url='login')
def booksView(request):
    userbooks = request.user.books.through.objects.all()
    books = [Book.objects.get(id=book.book_id) for book in userbooks]

    context = {
        'books': books
    }

    return render(request, 'books_list.html', context)
    
@login_required(login_url='login')
def bookListDetailView(request, state):
    STATES = {
        'completos' : ['Completado','completados'],
        'en-proceso' : ['En proceso', 'en proceso'],
        'abandonados' : ['Abandonado', 'abandonados'],
        'en-espera' : ['En espera', 'en lista de espera'],
    }

    userbooks = request.user.books.through.objects.filter(state=STATES[state][0])
    books = [Book.objects.get(id=book.book_id) for book in userbooks]

    context = {
        'title': STATES[state][1],
        'books': books
    }

    return render(request, 'books_list.html', context)
