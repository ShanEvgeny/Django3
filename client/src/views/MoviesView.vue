<script setup>
    import { computed, onBeforeMount, ref } from 'vue';
    import axios from 'axios';
    import Multiselect from 'vue-multiselect';
    import Cookies from 'js-cookie';
    import _ from 'lodash';
    import { useUserInfoStore } from '@/stores/user_info_store';
    import { storeToRefs } from 'pinia';

    const userInfoStore = useUserInfoStore();
    const {
        second,
        is_staff
    } = storeToRefs(userInfoStore)
    const movies = ref([]);
    const typeMovies = ref([]);
    const directors = ref([]);
    const genres = ref([]);
    const movieToAdd = ref({});
    const movieToEdit = ref({});
    const moviesPictureRef = ref();
    const moviesEditPictureRef = ref();
    const movieAddImageURL = ref();
    const movieEditImageURL = ref();
    const movieModalImageURL = ref();
    const movieModalBriefInfo = ref();
    const typeMovieToFilter = ref('Все');
    const directorToFilter = ref('Все');
    const genreToFilter = ref('Все');
    const typeMovieById = computed(() => {
        return _.keyBy(typeMovies.value, x => x.id)
    })
    const directorById = computed(() => {
        return _.keyBy(directors.value, x => x.id)
    })
    const genreById = computed(() => {
        return _.keyBy(genres.value, x => x.id)
    })
    const filteredMovies = computed(() => {
        return movies.value.filter(movie => {
            return (movie.type_movie === typeMovieToFilter.value || typeMovieToFilter.value === 'Все') &&
            (movie.directors.some(dir => dir == directorToFilter.value) || directorToFilter.value === 'Все') &&
            (movie.genres.some(gnr => gnr == genreToFilter.value) || genreToFilter.value === 'Все')
        })
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
        const formData = new FormData();
        const selectedGenres = movieToAdd.value.genres.map(gnr => gnr.id);
        const selectedDirectors = movieToAdd.value.directors.map(dir => dir.id);
        if (moviesPictureRef.value.files[0]){
            formData.append('picture',moviesPictureRef.value.files[0]);
        }
        formData.set('title', movieToAdd.value.title);
        formData.append('year_of_release', movieToAdd.value.year_of_release);
        formData.set('brief_information', movieToAdd.value.brief_information || '');
        formData.append('type_movie', movieToAdd.value.type_movie || '');
        selectedGenres.forEach(genreId => {
            formData.append('genres', genreId);
        });
        selectedDirectors.forEach(directorId => {
            formData.append('directors', directorId);
        });
        await axios.post("/api/movies/", formData, {
            headers:{
                'Content-Type': 'multipart/form-data'
            }
        });
        await fetchMovies();
        movieToAdd.value = {}
        moviesPictureRef.value.value = ''
        movieAddImageURL.value = ''
    }
    async function onMovieDelete(movie){
        console.log(movie);
        await axios.delete(`/api/movies/${movie.id}/`);
        await fetchMovies();
    }
    async function onMovieEdit(movie){
        moviesEditPictureRef.value.value = ''
        movieToEdit.value = {...movie};
        movieToEdit.value.directors = movieToEdit.value.directors.map(id => directorById.value[id]).filter(Boolean);
        movieToEdit.value.genres = movieToEdit.value.genres.map(id => genreById.value[id]).filter(Boolean);
        movieEditImageURL.value = movieToEdit.value.picture
    }
    async function onMovieUpdate(){
        const formData = new FormData();
        const selectedGenres = movieToEdit.value.genres?.map(gnr => gnr.id);
        const selectedDirectors = movieToEdit.value.directors?.map(dir => dir.id);
        if (moviesEditPictureRef.value.files[0]){
            formData.append('picture',moviesEditPictureRef.value.files[0]);
        }
        formData.set('title', movieToEdit.value.title);
        formData.append('year_of_release', movieToEdit.value.year_of_release);
        formData.set('brief_information', movieToEdit.value.brief_information || '');
        formData.append('type_movie', movieToEdit.value.type_movie);
        selectedGenres.forEach(genreId => {
            formData.append('genres', genreId);
        });
        selectedDirectors.forEach(directorId => {
            formData.append('directors', directorId);
        });
        await axios.put(`/api/movies/${movieToEdit.value.id}/`, formData ,{
            headers:{
                'Content-Type': 'multipart/form-data'
            }
        });
        await fetchMovies();
        movieToEdit.value = {}
    }
    async function movieAddPictureChange(){
        movieAddImageURL.value = URL.createObjectURL(moviesPictureRef.value.files[0])
    }
    async function movieEditPictureChange(){
        movieEditImageURL.value = URL.createObjectURL(moviesEditPictureRef.value.files[0])
    }
    async function onClickMoviePicture(picture){
        console.log(picture)
        movieModalImageURL.value = picture
    }
    async function onClickMovieBriefInfo(brief_info) {
        movieModalBriefInfo.value = brief_info
    }
    async function onExportToExcel(){
        await axios.get('/api/movies/to-excel/')
        window.open('/api/movies/to-excel/', '_blank');
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
            <form @submit.prevent.stop="onMovieAdd()" v-if = "userInfoStore.hasPermissions('general.can_create_objects')">
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
                            placeholder="Режиссеры" required></multiselect>
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
                            placeholder="Жанры" required></multiselect>
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
                        <input class = "form-control" type="file" ref = "moviesPictureRef" @change="movieAddPictureChange()">
                    </div>
                    <div class = "col-auto">
                        <img :src="movieAddImageURL" style = "max-height: 60px;" alt="">
                    </div>
                    <div class = "col-auto">
                        <button class = 'btn btn-primary'>Добавить</button>
                    </div>
                </div>
            </form>
            <br>
            <div class = 'row'>
                <div class = 'col'>
                    <div class = 'form-floating'>
                        <select id="" class = 'form-select' v-model = "typeMovieToFilter">
                            <option value="Все">Все</option>
                            <option :value="t_m.id" v-for = "t_m in typeMovies">{{t_m.title}}</option>
                        </select>
                        <label for="floatingInput">Тип</label>
                    </div>
                </div>
                <div class = 'col'>
                    <div class = 'form-floating'>
                        <select id="" class = 'form-select' v-model = "directorToFilter">
                            <option value="Все">Все</option>
                            <option :value="dir.id" v-for = "dir in directors">{{dir.full_name}}</option>
                        </select>
                        <label for="floatingInput">Режиссер</label>
                    </div>
                </div>
                <div class = 'col'>
                    <div class = 'form-floating'>
                        <select id="" class = 'form-select' v-model = "genreToFilter">
                            <option value="Все">Все</option>
                            <option :value="gnr.id" v-for = "gnr in genres">{{gnr.title}}</option>
                        </select>
                        <label for="floatingInput">Жанр</label>
                    </div>
                </div>
                <div class="col-auto" v-if = "is_staff">
                    <button @click="onExportToExcel()" class = "btn btn-info">
                        <i class="bi bi-file-earmark-arrow-down"></i> Экспортировать в Excel
                    </button>
                </div>
            </div>
            <div v-for="item in filteredMovies" class = 'movie-item'>
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
                <b>
                    <div class = 'brief-information' data-bs-toggle="modal" 
                        data-bs-target="#briefInfoModal"
                        @click = "onClickMovieBriefInfo(item.brief_information)">
                        {{ item.brief_information }}
                    </div>
                </b>
                <div v-if = "item.avg_rating" class = "rating" :class="{
                    'rating-good': item.avg_rating >= 7,
                    'rating-medium': item.avg_rating < 7 && item.avg_rating >= 4,
                    'rating-bad': item.avg_rating < 4
                }">
                    <b>{{ item.avg_rating.toFixed(1) }}</b>
                </div>
                <b v-if = "!item.avg_rating">-</b>
                <div v-show = "item.picture" data-bs-toggle="modal" data-bs-target="#pictureModal">
                    <img :src="item.picture" style = "max-height: 60px;" @click="onClickMoviePicture(item.picture)">
                </div>
                <button v-if = "userInfoStore.hasPermissions('general.can_update_objects') && second == true" 
                    class = 'btn btn-success' @click="onMovieEdit(item)"
                    data-bs-toggle="modal" 
                    data-bs-target="#editMovieModal">
                    <i class="bi bi-pen-fill"></i>
                </button>
                <button v-if = "userInfoStore.hasPermissions('general.can_delete_objects')"
                    class = 'btn btn-danger' @click="onMovieDelete(item)"><i class="bi bi-x-lg"></i></button>
            </div>
        </div>
    </div>
    <!-- Модальное окно -->
    <div v-if = "userInfoStore.hasPermissions('general.can_update_objects')" class="modal fade" id="editMovieModal" tabindex="-1">
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
                            <div class = "col-auto">
                                <input class = "form-control" type="file" ref = "moviesEditPictureRef" @change="movieEditPictureChange()">
                            </div>
                            <div class = "col-auto">
                                <img :src="movieEditImageURL" style = "max-height: 60px;" alt="">
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
    <!-- Модальное окно с изображением -->
    <div class="modal fade" id="pictureModal" tabindex="-1">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Изображение</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Закрыть"></button>
                </div>
                <div v-show = "movieModalImageURL" class="modal-body">
                    <img :src="movieModalImageURL" style = "max-height: 500px;" alt="">
                </div>
            </div>
        </div>
    </div>
    <div class="modal fade" id="briefInfoModal" tabindex="-1">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Краткое описание</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Закрыть"></button>
                </div>
                <div class="modal-body">
                    <b>{{ movieModalBriefInfo }}</b>
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
        grid-template-columns: 0.5fr 0.35fr 0.5fr 0.5fr 0.5fr auto auto auto auto;
        column-gap: 10px;
        justify-content: space-between;
    }
    .brief-information {
        display: -webkit-box;
        line-clamp: 2;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }
    .rating{
        // background-color: green; 
        color: white; 
        border-radius: 8px; 
        padding: 0.5rem; 
        text-align: center;
        &-good {
            background-color: rgb(18, 122, 67);
        }
        &-medium {
            background-color: rgb(139, 138, 41);
        }
        &-bad {
            background-color: rgb(138, 38, 38);
        }
    }
</style>
<style src="vue-multiselect/dist/vue-multiselect.css"></style>