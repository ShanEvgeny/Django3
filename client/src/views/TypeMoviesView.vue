<script setup>
    import { computed, onBeforeMount, ref } from 'vue';
    import axios from 'axios';
    import Cookies from 'js-cookie';
    import _ from 'lodash';

    const typeMovies = ref({});
    const typeMovieToAdd = ref({});
    const typeMovieToEdit = ref({});
    
    async function fetchTypeMovies(){
        const r = await axios.get("/api/type_movies/")
        console.log(r.data)
        typeMovies.value = r.data
    }
    async function onTypeMovieAdd() {
        await axios.post("/api/type_movies/", {
            ...typeMovieToAdd.value
        });
        await fetchTypeMovies();
    }
    async function onTypeMovieDelete(typeMovie){
        console.log(typeMovie);
        await axios.delete(`/api/type_movies/${typeMovie.id}/`);
        await fetchTypeMovies();
    }
    async function onTypeMovieEdit(typeMovie){
        typeMovieToEdit.value = {...typeMovie};
    }
    async function onTypeMovieUpdate(){
        await axios.put(`/api/type_movies/${typeMovieToEdit.value.id}/`,{
            ...typeMovieToEdit.value,
        });
        await fetchTypeMovies();
    }

    onBeforeMount(async () => {
        axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
        await fetchTypeMovies();
    })
</script>

<template>
    <div class="container">
        <div class = "p-2">
            <form @submit.prevent.stop = "onTypeMovieAdd()">
                <div class = "row">
                    <div class = "col-3">
                        <div class = 'form-floating'>
                            <input type="text" class = 'form-control' v-model="typeMovieToAdd.title" required>
                            <label for="floatingInput">Название</label>
                        </div>
                    </div>
                    <div class = "col">
                        <div class = 'form-floating'>
                            <input type="text" class = 'form-control' v-model="typeMovieToAdd.description">
                            <label for="floatingInput">Описание</label>
                        </div>
                    </div>
                    <div class = "col-auto">
                        <button class = 'btn btn-primary'>Добавить</button>
                    </div>
                </div>
                <div v-for="item in typeMovies" class = 'typeMovie-item'>
                    <b>{{ item.title }}</b> 
                    <b>{{ item.description }}</b> 
                    <button class = 'btn btn-success' @click="onTypeMovieEdit(item)"
                        data-bs-toggle="modal" 
                        data-bs-target="#editTypeMovieModal">
                        <i class="bi bi-pen-fill"></i>
                    </button>
                    <button class = 'btn btn-danger' @click="onTypeMovieDelete(item)"><i class="bi bi-x-lg"></i></button>
                </div>
            </form>
        </div>
    </div>
    <div class="modal fade" id="editTypeMovieModal" tabindex="-1">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="exampleModalLabel">Редактирование</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Закрыть"></button>
                </div>
                <div class="modal-body">
                    <div class = "p-2">
                        <div class = "row">
                            <div class = "col-3">
                                <div class = 'form-floating'>
                                    <input type="text" class = 'form-control' v-model="typeMovieToEdit.title" required>
                                    <label for="floatingInput">Название</label>
                                </div>
                            </div>
                            <div class = "col">
                                <div class = 'form-floating'>
                                    <input type="text" class = 'form-control' v-model="typeMovieToEdit.description">
                                    <label for="floatingInput">Описание</label>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
                    <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click = "onTypeMovieUpdate()">
                        Сохранить изменения
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
    .typeMovie-item{
        padding: 0.5rem;
        margin: 1rem 0;
        border: 1px solid silver;
        border-radius: 8px;
        display: grid;
        grid-template-columns: 1fr 1fr auto auto;
        column-gap: 10px;
        justify-content: space-between;
    }
</style>