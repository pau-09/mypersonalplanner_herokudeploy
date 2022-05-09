from django.urls import path

from books.views import booksView, bookListDetailView

urlpatterns = [
    path('', booksView, name='books'),
    path('<str:state>/', bookListDetailView, name='bookList'),
    # path('<int:book_id>/<str:new_state>/', bookListDetailView, name='bookList')
]
