from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from books.models import Book
from movies.models import Movie

# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=15, unique=True, validators=[AbstractUser.username_validator],)
    email = models.EmailField('email address', blank=True, unique=True)
    books = models.ManyToManyField(Book, through='BookList')
    movies = models.ManyToManyField(Movie, through='MovieList')

    class Meta:
        db_table='auth_user'

class BookList(models.Model):
    STATES = [
        ('Completado','Completado'),
        ('En proceso','En proceso'),
        ('Abandonado','Abandonado'),
        ('En espera','En espera')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    state = models.CharField(max_length=20, choices=STATES)

    class Meta:
        models.UniqueConstraint(fields=['book', 'user'], name='unique_book_per_user')

    def __str__(self):
        return f'{self.user} - {self.book} -----------> {self.state}'

class MovieList(models.Model):
    STATES = [
        ('Completada','Completada'),
        ('En proceso','En proceso'),
        ('Abandonada','Abandonada'),
        ('En espera','En espera')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    state = models.CharField(max_length=20, choices=STATES)

    class Meta:
        models.UniqueConstraint(fields=['book', 'user'], name='unique_book_per_user')
    
    def __str__(self):
        return f'{self.user} - {self.movie} -----------> {self.state}'