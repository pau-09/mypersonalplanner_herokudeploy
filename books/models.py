from django.db import models
# from users.models import User

# Create your models here.
class Book(models.Model):

    GENRES=[
        ('Acción', 'Acción'),
        ('Novela', 'Novela'),
        ('Aventuras', 'Aventuras'),
        ('Ciencia Ficcion', 'Ciencia Ficción'),
        ('Tragedia', 'Tragedia'),
        ('Fantasía', 'Fantasía'),
        ('Documental', 'Documental'),
        ('Drama', 'Drama'),
        ('Musical', 'Musical'),
        ('Comedia', 'Comedia'),
        ('Suspense', 'Suspense'),
        ('Terror', 'Terror'),
        ('Juvenil', 'Juvenil'),
        ('Romance', 'Romance'),
        ('Autobiografía','Autobiografía'),
    ]

    title = models.CharField(max_length=80,unique=True)
    author = models.CharField(max_length=50, default='Anónimo')
    year = models.PositiveSmallIntegerField()
    genre = models.CharField(max_length=20, choices=GENRES)

    def __str__(self):
        return self.title