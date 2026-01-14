<script setup>
    import { computed, onBeforeMount, ref } from 'vue';
    import axios from 'axios';
    import Cookies from 'js-cookie';
    import _ from 'lodash';
    import { useUserInfoStore } from '@/stores/user_info_store';
    import { storeToRefs } from 'pinia';

    const userInfoStore = useUserInfoStore();
    const {
        second
    } = storeToRefs(userInfoStore)
    const ratingMovies = ref({})
    const movies = ref({})
    const ratingMovieToAdd = ref({});
    const ratingMovieToEdit = ref({});
    const movieById = computed(() => {
        return _.keyBy(movies.value, x => x.id)
    })
    async function fetchRatingMovies(){
        const r = await axios.get("/api/ratings/")
        console.log(r.data)
        ratingMovies.value = r.data
    } 
    async function fetchMovies(){
        const r = await axios.get("/api/movies/")
        console.log(r.data)
        movies.value = r.data
    }
    async function onRatingMovieAdd() {
        await axios.post("/api/ratings/", {
            ...ratingMovieToAdd.value
        });
        await fetchRatingMovies();
        ratingMovieToAdd.value = {};
    }
    async function onRatingMovieDelete(rating_movie){
        console.log(rating_movie);
        await axios.delete(`/api/ratings/${rating_movie.id}/`);
        await fetchRatingMovies();
    }
    async function onRatingMovieEdit(rating_movie){
        ratingMovieToEdit.value = {...rating_movie};
    }
    async function onRatingMovieUpdate(){
        await axios.put(`/api/ratings/${ratingMovieToEdit.value.id}/`,{
            ...ratingMovieToEdit.value,
        });
        await fetchRatingMovies();
    }

    onBeforeMount(async () => {
        axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
        await fetchRatingMovies();
        await fetchMovies();
    }) 
</script>

<template>
    Оценки
    {{ userInfoStore.username }}
    <div class="container">
        <div class = "p-2">
            <form @submit.prevent.stop = "onRatingMovieAdd()">
                <div class = "row">
                    <div class = "col-3">
                        <div class = 'form-floating'>
                            <input type="number" min = "1" max = "10" class = 'form-control' v-model="ratingMovieToAdd.rating_value" required>
                            <label for="floatingInput">Оценка</label>
                        </div>
                    </div>
                    <div class = "col">
                        <div class = 'form-floating'>
                            <select name="" id="" class = 'form-select' v-model="ratingMovieToAdd.movie" required>
                                <option :value="movie.id" v-for = "movie in movies">{{movie.title}}</option>
                            </select>
                            <label for="floatingInput">Кино</label>
                        </div>
                    </div>
                    <div class = "col-auto">
                        <button class = 'btn btn-primary'>Добавить</button>
                    </div>
                </div>
                <div v-for="item in ratingMovies" class = 'ratingMovie-item'>
                    <b>{{ item.rating_value }}</b> 
                    <b>{{ movieById[item.movie]?.title }}</b>
                    <b>{{ item.user }}</b> 
                    <button v-if = "second == true" class = 'btn btn-success' @click="onRatingMovieEdit(item)"
                        data-bs-toggle="modal" 
                        data-bs-target="#editRatingMovieModal">
                        <i class="bi bi-pen-fill"></i>
                    </button>
                    <button class = 'btn btn-danger' @click="onRatingMovieDelete(item)"><i class="bi bi-x-lg"></i></button>
                </div>
            </form>
        </div>
    </div>
    <div class="modal fade" id="editRatingMovieModal" tabindex="-1">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="exampleModalLabel">Редактирование</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Закрыть"></button>
                </div>
                <div class="modal-body">
                    <div class = 'p-2'>
                        <div class = "row">
                            <div class = "col-3">
                                <div class = 'form-floating'>
                                    <input type="number" min = "1" max = "10" class = 'form-control' v-model="ratingMovieToEdit.rating_value" required>
                                    <label for="floatingInput">Оценка</label>
                                </div>
                            </div>
                            <div class = "col">
                                <div class = 'form-floating'>
                                    <select name="" id="" class = 'form-select' v-model="ratingMovieToEdit.movie" required>
                                        <option :value="movie.id" v-for = "movie in movies">{{movie.title}}</option>
                                    </select>
                                    <label for="floatingInput">Кино</label>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
                    <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click = "onRatingMovieUpdate()">
                        Сохранить изменения
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
    .ratingMovie-item{
        padding: 0.5rem;
        margin: 1rem 0;
        border: 1px solid silver;
        border-radius: 8px;
        display: grid;
        grid-template-columns: 1fr 1fr auto auto auto;
        column-gap: 10px;
        justify-content: space-between;
    }
</style>