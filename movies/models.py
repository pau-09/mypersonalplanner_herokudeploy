from django.db import models
# from users.models import User

# Create your models here.
class Movie(models.Model):

    GENRES=[
        ('Accion', 'Acción'),
        ('Aventuras', 'Aventuras'),
        ('Ciencia Ficcion', 'Ciencia Ficción'),
        ('Comedia', 'Comedia'),
        ('Fantasia', 'Fantasía'),
        ('Documental', 'Documental'),
        ('Drama', 'Drama'),
        ('Musical', 'Musical'),
        ('Suspense', 'Suspense'),
        ('Terror', 'Terror'),
        ('Animacion', 'Animación'),
        ('Romance', 'Romance'),
    ]

    title = models.CharField(max_length=80,unique=True)
    director = models.CharField(max_length=50, default='Anónimo')
    year = models.PositiveSmallIntegerField()
    genre = models.CharField(max_length=20, choices=GENRES)

    def __str__(self):
        return self.title