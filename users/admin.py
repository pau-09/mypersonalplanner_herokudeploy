from django.contrib import admin
from .models import User, BookList, MovieList


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "is_staff", "date_joined")


@admin.register(BookList)
class BookListAdmin(admin.ModelAdmin):
    list_display = ("user", "book", "state")


@admin.register(MovieList)
class MovieListAdmin(admin.ModelAdmin):
    list_display = ("user", "movie", "state")
