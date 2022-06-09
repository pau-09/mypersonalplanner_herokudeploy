from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include

from main.views import mainView, searchView
from users.views import loginView, logoutUserView, registerView, addEntryView

urlpatterns = [
    path('', lambda _:redirect('login')),
    path('admin/', admin.site.urls),
    path('registro/', registerView, name='register'),
    path('iniciar-sesion/', loginView, name='login'),
    path('salir/', logoutUserView, name='logout'),
    path('principal/', mainView, name='main'),
    path('libros/', include('books.urls')),
    path('peliculas/', include('movies.urls')),
    path('añadir/', addEntryView, name='addEntry')
    # path('buscar/', searchView, name='search')
]
