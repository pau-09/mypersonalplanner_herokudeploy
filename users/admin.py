from django.contrib import admin

from .models import User, BookList, MovieList
# Register your models here.
admin.site.register(User)
admin.site.register(BookList)
admin.site.register(MovieList)