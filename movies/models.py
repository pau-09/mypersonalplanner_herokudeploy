from django.db import models

class Movie(models.Model):

    GENRES=[
        ('Acción', 'Acción'),
        ('Aventuras', 'Aventuras'),
        ('Ciencia Ficción', 'Ciencia Ficción'),
        ('Comedia', 'Comedia'),
        ('Fantasía', 'Fantasía'),
        ('Documental', 'Documental'),
        ('Drama', 'Drama'),
        ('Musical', 'Musical'),
        ('Suspense', 'Suspense'),
        ('Terror', 'Terror'),
        ('Animación', 'Animación'),
        ('Romance', 'Romance'),
    ]

    title = models.CharField(max_length=80,unique=True)
    director = models.CharField(max_length=50, default='Anónimo')
    year = models.PositiveSmallIntegerField()
    genre = models.CharField(max_length=20, choices=GENRES)

    def __str__(self):
        return self.title