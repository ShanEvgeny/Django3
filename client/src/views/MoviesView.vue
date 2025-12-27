<script setup>
    import { computed, onBeforeMount, ref } from 'vue';
    import axios from 'axios';
    import Multiselect from 'vue-multiselect';
    import Cookies from 'js-cookie';
    import _ from 'lodash';

    const movies = ref([]);
    const typeMovies = ref({});
    const directors = ref({});
    const genres = ref({});
    const movieToAdd = ref({});
    const movieToEdit = ref({});
    const typeMovieById = computed(() => {
        return _.keyBy(typeMovies.value, x => x.id)
    })
    const directorById = computed(() => {
        return _.keyBy(directors.value, x => x.id)
    })
    const genreById = computed(() => {
        return _.keyBy(genres.value, x => x.id)
    })
    
    async function fetchDirectors(){
        const r = await axios.get("/api/directors/")
        console.log(r.data)
        directors.value = r.data
    }
    async function fetchGenres(){
        const r = await axios.get("/api/genres/")
        console.log(r.data)
        genres.value = r.data
    }
    async function fetchTypeMovies(){
        const r = await axios.get("/api/type_movies/")
        console.log(r.data)
        typeMovies.value = r.data
    }
    async function fetchMovies(){
        const r = await axios.get("/api/movies/")
        console.log(r.data)
        movies.value = r.data
    } 
    async function onMovieAdd() {
        await axios.post("/api/movies/", {
            ...movieToAdd.value,
            directors: movieToAdd.value.directors.map(dir => dir.id),
            genres: movieToAdd.value.genres.map(gnr => gnr.id)
        });
        await fetchMovies();
    }
    async function onMovieDelete(movie){
        console.log(movie);
        await axios.delete(`/api/movies/${movie.id}/`);
        await fetchMovies();
    }
    async function onMovieEdit(movie){
        movieToEdit.value = {...movie};
        movieToEdit.value.directors = movieToEdit.value.directors.map(id => directorById.value[id]).filter(Boolean);
        movieToEdit.value.genres = movieToEdit.value.genres.map(id => genreById.value[id]).filter(Boolean);
    }
    async function onMovieUpdate(){
        await axios.put(`/api/movies/${movieToEdit.value.id}/`,{
            ...movieToEdit.value,
            directors: movieToEdit.value.directors.map(dir => dir.id),
            genres: movieToEdit.value.genres.map(gnr => gnr.id)
            
        });
        await fetchMovies();
    }

    onBeforeMount(async () => {
        axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
        await fetchMovies();
        await fetchTypeMovies();
        await fetchDirectors();
        await fetchGenres();
    })
</script>

<template>
    <div class="container">
        <div class = 'p-2'>
            <form @submit.prevent.stop="onMovieAdd()">
                <div class = 'row'>
                    <div class = 'col-3'>
                        <div class = 'form-floating'>
                            <input type="text" class = 'form-control' v-model="movieToAdd.title" required>
                            <label for="floatingInput">Название</label>
                        </div>
                    </div>
                    <div class = 'col-2'>
                        <div class = 'form-floating'>
                            <input type="number" min="1895" step="1" 
                                class = 'form-control' 
                                v-model="movieToAdd.year_of_release" 
                                required>
                            <label for="floatingInput">Год выхода</label>
                        </div>
                    </div>
                    <div class = 'col-1'>
                        <div class = 'form-floating'>
                            <select name="" id="" class = 'form-select' v-model="movieToAdd.type_movie">
                                <option :value="t_m.id" v-for = "t_m in typeMovies">{{t_m.title}}</option>
                            </select>
                            <label for="floatingInput">Тип</label>
                        </div>
                    </div>
                    <div class = 'col-3'>
                        <div class = 'multiselect'>
                            <multiselect
                            v-model="movieToAdd.directors"
                            :options="directors"
                            :multiple="true"
                            :close-on-select="false"
                            label="full_name"
                            track-by="id"
                            placeholder="Режиссеры"></multiselect>
                        </div>
                    </div>
                    <div class = 'col-3'>
                        <div class = 'multiselect'>
                            <multiselect
                            v-model="movieToAdd.genres"
                            :options="genres"
                            :multiple="true"
                            :close-on-select="false"
                            label="title"
                            track-by="id"
                            placeholder="Жанры"></multiselect>
                        </div>
                    </div>
                </div>
                <br>
                <div class = 'row'>
                    <div class = 'col'>
                        <div class = 'form-floating'>
                            <input type="text" class = 'form-control' v-model="movieToAdd.brief_information">
                            <label for="floatingInput">Краткое описание</label>
                        </div>
                    </div>
                    <div class = "col-auto">
                        <button class = 'btn btn-primary'>Добавить</button>
                    </div>
                </div>
                <div v-for="item in movies" class = 'movie-item'>
                    <b>{{ item.title }} ({{ item.year_of_release }})</b> 
                    <b>{{ typeMovieById[item.type_movie]?.title }}</b>
                    <b>
                        <div v-for="director in item.directors">
                            {{ directorById[director]?.full_name }}
                        </div>
                    </b>
                    <b>
                        <div v-for="genre in item.genres">
                            {{ genreById[genre]?.title }}
                        </div>
                    </b>
                    <b>{{ item.brief_information }}</b>
                    <button class = 'btn btn-success' @click="onMovieEdit(item)"
                        data-bs-toggle="modal" 
                        data-bs-target="#editMovieModal">
                        <i class="bi bi-pen-fill"></i>
                    </button>
                    <button class = 'btn btn-danger' @click="onMovieDelete(item)"><i class="bi bi-x-lg"></i></button>
                </div>
            </form>
        </div>
    </div>
    <!-- Модальное окно -->
    <div class="modal fade" id="editMovieModal" tabindex="-1">
        <div class="modal-dialog modal-xl">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="exampleModalLabel">Редактирование</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Закрыть"></button>
                </div>
                <div class="modal-body">
                    <div class = 'p-3'>
                        <div class = 'row'>
                            <div class = 'col-3'>
                                <div class = 'form-floating'>
                                    <input type="text" class = 'form-control' v-model="movieToEdit.title">
                                    <label for="floatingInput">Название</label>
                                </div>
                            </div>
                            <div class = 'col-2'>
                                <div class = 'form-floating'>
                                    <input type="number" min="1895" step="1" 
                                        class = 'form-control' 
                                        v-model="movieToEdit.year_of_release">
                                    <label for="floatingInput">Год выхода</label>
                                </div>
                            </div>
                            <div class = 'col-1'>
                                <div class = 'form-floating'>
                                    <select name="" id="" class = 'form-select' v-model="movieToEdit.type_movie">
                                        <option :value="t_m.id" v-for = "t_m in typeMovies">{{t_m.title}}</option>
                                    </select>
                                    <label for="floatingInput">Тип</label>
                                </div>
                            </div>
                            <div class = 'col-3'>
                                <div class = 'multiselect'>
                                    <multiselect
                                    v-model="movieToEdit.directors"
                                    :options="directors"
                                    :multiple="true"
                                    :close-on-select="false"
                                    label="full_name"
                                    track-by="id"
                                    placeholder="Режиссеры"></multiselect>
                                </div>
                            </div>
                            <div class = 'col-3'>
                                <div class = 'multiselect'>
                                    <multiselect
                                    v-model="movieToEdit.genres"
                                    :options="genres"
                                    :multiple="true"
                                    :close-on-select="false"
                                    label="title"
                                    track-by="id"
                                    placeholder="Жанры"></multiselect>
                                </div>
                            </div>
                        </div>
                        <br>
                        <div class = 'row'>
                            <div class = 'col'>
                                <div class = 'form-floating'>
                                    <input type="text" class = 'form-control' v-model="movieToEdit.brief_information">
                                    <label for="floatingInput">Краткое описание</label>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
                    <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click = "onMovieUpdate()">
                        Сохранить изменения
                    </button>
                </div>
            </div>
        </div>
    </div>  
</template>

<style lang = "scss" scoped>
    .movie-item{
        padding: 0.5rem;
        margin: 1rem 0;
        border: 1px solid silver;
        border-radius: 8px;
        display: grid;
        grid-template-columns: 0.5fr 0.35fr 0.5fr 0.5fr 0.5fr auto auto;
        column-gap: 10px;
        justify-content: space-between;
    }
</style>
<style src="vue-multiselect/dist/vue-multiselect.css"></style>