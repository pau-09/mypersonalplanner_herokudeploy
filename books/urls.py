from django.urls import path

from books.views import booksView, bookListDetailView

urlpatterns = [
    path('', booksView, name='books'),
    path('<str:state>/', bookListDetailView, name='bookList'),
    # path('en-proceso/', booksStartedView, name='booksProgress'),
    # path('abandonados/', booksDroppedView, name='booksDropped'),
    # path('en-espera/', booksWaitingView, name='booksWaiting'),
]
