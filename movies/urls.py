from django.urls import path

from .views import moviesView, movieListDetailView

urlpatterns = [
    path('', moviesView, name='movies'),
    path('<str:state>/', movieListDetailView, name='movieList')
]
