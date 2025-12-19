from django.test import TestCase
from rest_framework.test import APIClient
from model_bakery import baker

from movies.models import Genre, Director, Movie, TypeMovie, RatingMovie

class GenresViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        genre = baker.make("Genre")
        r = self.client.get('/api/genres/')
        data = r.json()
        print(data)
        assert genre.id == data[0]['id']
        assert genre.title == data[0]['title']
        assert genre.description == data[0]['description']

    def test_create(self):
        r = self.client.post("/api/genres/",{
            'title': "Жанр",
            'description': "Описание"
        })
        new_genre_id = r.json()['id']
        genres = Genre.objects.all()
        assert len(genres) == 1
        new_genre = Genre.objects.filter(id = new_genre_id).first()
        assert new_genre.title == "Жанр"
        assert new_genre.description == "Описание"

    def test_delete(self):
        genres = baker.make("Genre",10)
        r = self.client.get('/api/genres/')
        data = r.json()
        assert len(data) == 10
        genre_id_to_delete = genres[3].id
        self.client.delete(f'/api/genres/{genre_id_to_delete}/')
        r = self.client.get('/api/genres/')
        data = r.json()
        assert len(data) == 9
        assert genre_id_to_delete not in [i['id'] for i in data]

    def test_update(self):
        genres = baker.make("Genre",10)
        genre: Genre = genres[2]
        r = self.client.get(f'/api/genres/{genre.id}/')
        data = r.json()
        assert data['title'] == genre.title
        r = self.client.patch(f'/api/genres/{genre.id}/',{
            'title': 'Жанр'
        })
        assert r.status_code == 200
        r = self.client.get(f'/api/genres/{genre.id}/')
        data = r.json()
        assert data['title'] == "Жанр"
        genre.refresh_from_db()
        assert data['title'] == genre.title

class DirectorsViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        director = baker.make("movies.Director",date_of_birth = '2025-12-15')
        r = self.client.get('/api/directors/')
        data = r.json()
        print(data)
        assert director.id == data[0]['id']
        assert director.full_name == data[0]['full_name']
        assert director.date_of_birth == data[0]['date_of_birth']

    def test_create(self):
        r = self.client.post("/api/directors/",{
            'full_name': "Режиссер",
            'date_of_birth': "1995-12-15"
        })
        new_drctr_id = r.json()['id']
        drctrs = Director.objects.all()
        assert len(drctrs) == 1
        new_drctr = Director.objects.filter(id = new_drctr_id).first()
        assert new_drctr.full_name == "Режиссер"
        assert str(new_drctr.date_of_birth) == "1995-12-15"

    def test_delete(self):
        directors = baker.make("Director",10)
        r = self.client.get('/api/directors/')
        data = r.json()
        assert len(data) == 10
        director_id_to_delete = directors[3].id
        self.client.delete(f'/api/directors/{director_id_to_delete}/')
        r = self.client.get('/api/directors/')
        data = r.json()
        assert len(data) == 9
        assert director_id_to_delete not in [i['id'] for i in data]

    def test_update(self):
        directors = baker.make("Director", 10)
        director: Director = directors[2]
        r = self.client.get(f'/api/directors/{director.id}/')
        data = r.json()
        assert data['full_name'] == director.full_name
        r = self.client.patch(f'/api/directors/{director.id}/',{
            'full_name': 'Режиссер'
        })
        assert r.status_code == 200
        r = self.client.get(f'/api/directors/{director.id}/')
        data = r.json()
        assert data['full_name'] == "Режиссер"
        director.refresh_from_db()
        assert data['full_name'] == director.full_name

class TypeMoviesViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        type_movie = baker.make("movies.TypeMovie")
        r = self.client.get('/api/type_movies/')
        data = r.json()
        print(data)
        assert type_movie.id == data[0]['id']
        assert type_movie.title == data[0]['title']
        assert type_movie.description == data[0]['description']
        
    def test_create(self):
        r = self.client.post("/api/type_movies/",{
            'title': "Тип кино",
            'description': "Описание"
        })
        new_type_movie_id = r.json()['id']
        type_movies = TypeMovie.objects.all()
        assert len(type_movies) == 1
        new_type_movie = TypeMovie.objects.filter(id = new_type_movie_id).first()
        assert new_type_movie.title == "Тип кино"
        assert new_type_movie.description == "Описание"

    def test_delete(self):
        type_movies = baker.make("TypeMovie",10)
        r = self.client.get('/api/type_movies/')
        data = r.json()
        assert len(data) == 10
        type_movie_id_to_delete = type_movies[3].id
        self.client.delete(f'/api/type_movies/{type_movie_id_to_delete}/')
        r = self.client.get('/api/type_movies/')
        data = r.json()
        assert len(data) == 9
        assert type_movie_id_to_delete not in [i['id'] for i in data]

    def test_update(self):
        type_movies = baker.make("TypeMovie",10)
        type_movie: TypeMovie = type_movies[2]
        r = self.client.get(f'/api/type_movies/{type_movie.id}/')
        data = r.json()
        assert data['title'] == type_movie.title
        r = self.client.patch(f'/api/type_movies/{type_movie.id}/',{
            'title': 'Тип кино'
        })
        assert r.status_code == 200
        r = self.client.get(f'/api/type_movies/{type_movie.id}/')
        data = r.json()
        assert data['title'] == "Тип кино"
        type_movie.refresh_from_db()
        assert data['title'] == type_movie.title

class MoviesViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        t_m = baker.make('TypeMovie')
        director1 = baker.make("movies.Director",date_of_birth = '2025-12-15')
        director2 = baker.make("movies.Director",date_of_birth = '2025-12-14')
        genre1 = baker.make("Genre")
        genre2 = baker.make("Genre")
        movie = baker.make("movies.Movie", type_movie = t_m)
        movie.directors.add(director1, director2)
        movie.genres.add(genre1, genre2)
        r = self.client.get('/api/movies/')
        data = r.json()
        print(data)
        assert movie.id == data[0]['id']
        assert movie.title == data[0]['title']
        assert movie.brief_information == data[0]['brief_information']
        assert movie.type_movie.id == data[0]['type_movie']
        assert movie.directors.count() == 2
        assert movie.genres.count() == 2
        directors_list_id = list(movie.directors.values_list('id', flat=True))
        genres_list_id = list(movie.genres.values_list('id', flat=True))
        assert directors_list_id == data[0]['directors']
        assert genres_list_id == data[0]['genres']

    def test_create(self):
        director1 = baker.make("movies.Director",date_of_birth = '2025-12-15')
        director2 = baker.make("movies.Director",date_of_birth = '2025-12-14')
        genre1 = baker.make("Genre")
        genre2 = baker.make("Genre")
        directors = [director1.id,director2.id]
        genres = [genre1.id,genre2.id]
        t_m = baker.make('TypeMovie')
        r = self.client.post("/api/movies/",{
            'title': "Кино",
            'year_of_release': 1999,
            'brief_information': "Краткий сюжет",
            'type_movie': t_m.id,
            'directors': directors,
            'genres': genres
        })
        new_mv_id = r.json()['id']
        mvs = Movie.objects.all()
        assert len(mvs) == 1
        new_mv = Movie.objects.filter(id = new_mv_id).first()
        assert new_mv.title == "Кино"
        assert new_mv.year_of_release == 1999
        assert new_mv.brief_information == "Краткий сюжет"
        assert new_mv.type_movie == t_m
        directors_list_id = list(new_mv.directors.values_list('id', flat=True))
        genres_list_id = list(new_mv.genres.values_list('id', flat=True))
        assert directors_list_id == directors
        assert genres_list_id == genres

    def test_delete(self):
        movies = baker.make("Movie",10)
        r = self.client.get('/api/movies/')
        data = r.json()
        assert len(data) == 10
        movie_id_to_delete = movies[3].id
        self.client.delete(f'/api/movies/{movie_id_to_delete}/')
        r = self.client.get('/api/movies/')
        data = r.json()
        assert len(data) == 9
        assert movie_id_to_delete not in [i['id'] for i in data]

    def test_update(self):
        movies = baker.make("Movie",10)
        movie: Movie = movies[2]
        r = self.client.get(f'/api/movies/{movie.id}/')
        data = r.json()
        assert data['title'] == movie.title
        r = self.client.patch(f'/api/movies/{movie.id}/',{
            'title': 'Кино'
        })
        assert r.status_code == 200
        r = self.client.get(f'/api/movies/{movie.id}/')
        data = r.json()
        assert data['title'] == "Кино"
        movie.refresh_from_db()
        assert data['title'] == movie.title

class RatingMoviesViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
    def test_get_list(self):
        mv = baker.make('Movie')
        type_movie = baker.make("movies.RatingMovie", movie = mv)
        r = self.client.get('/api/ratings/')
        data = r.json()
        print(data)
        assert type_movie.id == data[0]['id']
        assert type_movie.rating_value == data[0]['rating_value']
        assert type_movie.movie.id == data[0]['movie']
    
    def test_create(self):
        mv = baker.make('Movie')
        r = self.client.post("/api/ratings/",{
            'rating_value': 8,
            'movie': mv.id
        })
        new_rating_movie_id = r.json()['id']
        type_movies = RatingMovie.objects.all()
        assert len(type_movies) == 1
        new_type_movie = RatingMovie.objects.filter(id = new_rating_movie_id).first()
        assert new_type_movie.rating_value == 8
        assert new_type_movie.movie == mv

    def test_delete(self):
        rating_movies = baker.make("RatingMovie",10)
        r = self.client.get('/api/ratings/')
        data = r.json()
        assert len(data) == 10
        rating_movie_id_to_delete = rating_movies[3].id
        self.client.delete(f'/api/ratings/{rating_movie_id_to_delete}/')
        r = self.client.get('/api/ratings/')
        data = r.json()
        assert len(data) == 9
        assert rating_movie_id_to_delete not in [i['id'] for i in data]
    
    def test_update(self):
        rating_movies = baker.make("RatingMovie",10)
        rating_movie: RatingMovie = rating_movies[2]
        r = self.client.get(f'/api/ratings/{rating_movie.id}/')
        data = r.json()
        assert data['rating_value'] == rating_movie.rating_value
        r = self.client.patch(f'/api/ratings/{rating_movie.id}/',{
            'rating_value': 8
        })
        assert r.status_code == 200
        r = self.client.get(f'/api/ratings/{rating_movie.id}/')
        data = r.json()
        assert data['rating_value'] == 8
        rating_movie.refresh_from_db()
        assert data['rating_value'] == rating_movie.rating_value