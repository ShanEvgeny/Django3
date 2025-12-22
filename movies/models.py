from django.db import models
from datetime import datetime
from django.core.validators import MinValueValidator, MaxValueValidator

class TypeMovie(models.Model):
    title = models.TextField("Название")
    description = models.TextField("Описание", null = True)
    class Meta:
        verbose_name = "Тип произведения"
        verbose_name_plural = "Типы произведений"
    def __str__(self) -> str:
        return self.title  
class Director(models.Model):
    full_name = models.TextField("ФИО")
    date_of_birth  = models.DateField("Дата рождения", null = True)
    short_biography = models.TextField("Краткая биография", null = True)
    class Meta:
        verbose_name = "Режиссер"
        verbose_name_plural = "Режиссеры"
    def __str__(self) -> str:
        return self.full_name
class Genre(models.Model):
    title = models.TextField("Название")
    description = models.TextField("Описание", null = True)
    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"
    def __str__(self) -> str:
        return self.title
class Movie(models.Model):
    title = models.TextField("Название")
    year_of_release = models.PositiveIntegerField("Год выхода", validators=[MinValueValidator(1895), MaxValueValidator(datetime.now().year)])
    brief_information = models.TextField("Краткая информация", null = True)
    type_movie = models.ForeignKey('TypeMovie', on_delete = models.CASCADE,verbose_name='Тип произведения', null = True)
    directors = models.ManyToManyField('Director', related_name='movie_directors',verbose_name = 'Участники съемки')
    genres = models.ManyToManyField('Genre', related_name = 'movie_genres',verbose_name="Жанры")
    class Meta:
        verbose_name = "Кино"
        verbose_name_plural = "Кино"
    def __str__(self) -> str:
        return self.title
class RatingMovie(models.Model):
    rating_value = models.PositiveIntegerField("Оценка", validators=[MinValueValidator(1), MaxValueValidator(10)])
    movie = models.ForeignKey('Movie', on_delete = models.CASCADE, verbose_name = "Название произведения", null = True)
    user = models.ForeignKey('auth.User',on_delete = models.CASCADE, verbose_name='Пользователь',null = True)
    class Meta:
        unique_together = ['movie','user']
        verbose_name = "Оценка"
        verbose_name_plural = "Оценки"