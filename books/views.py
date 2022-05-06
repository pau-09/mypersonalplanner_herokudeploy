from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Book
from users.models import BookList

# Create your views here.
@login_required(login_url='login')
def booksView(request):
    userbooks = BookList.objects.filter(user_id=request.user.id)
    books = [Book.objects.get(id=book.book_id) for book in userbooks]

    context = {
        'books': books
    }

    # return render(request, 'list_summary.html', context)
    return render(request, 'detail_list.html', context)
    
@login_required(login_url='login')
def bookListDetailView(request, state):
    STATES = {
        'completos' : ['Completado','completados'],
        'en-proceso' : ['En proceso', 'en proceso'],
        'abandonados' : ['Abandonado', 'abandonados'],
        'en-espera' : ['En espera', 'en lista de espera'],
    }

    userbooks = BookList.objects.filter(user_id=request.user.id, state=STATES[state][0])
    books = [Book.objects.get(id=book.book_id) for book in userbooks]

    context = {
        'title': STATES[state][1],
        'books': books
    }

    return render(request, 'detail_list.html', context)
