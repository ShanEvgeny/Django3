<script setup>
    import { onBeforeMount, ref } from 'vue';
    import axios from 'axios';
    import _ from 'lodash';
    import { useUserInfoStore } from '@/stores/user_info_store';
    import { storeToRefs } from 'pinia';
    import { useMoviesInfoStore } from '@/stores/movies_info_store';

    const userInfoStore = useUserInfoStore();
    const moviesInfoStore = useMoviesInfoStore();
    const {
        second
    } = storeToRefs(userInfoStore)
    const {
        genres
    } = storeToRefs(moviesInfoStore);
    const genreToAdd = ref({});
    const genreToEdit = ref({});
    
    async function onGenreAdd() {
        await axios.post("/api/genres/", {
            ...genreToAdd.value
        });
        await moviesInfoStore.fetchGenres();
        genreToAdd.value = {};
    }
    async function onGenreDelete(genre){
        console.log(genre);
        await axios.delete(`/api/genres/${genre.id}/`);
        await moviesInfoStore.fetchGenres();
    }
    async function onGenreEdit(genre){
        genreToEdit.value = {...genre};
    }
    async function onGenreUpdate(){
        await axios.put(`/api/genres/${genreToEdit.value.id}/`,{
            ...genreToEdit.value,
        });
        await moviesInfoStore.fetchGenres();
    }

    onBeforeMount(async () => {
        //axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
        await moviesInfoStore.fetchGenres();
    })
</script>

<template>
    <div class="container">
        <div class = "p-2">
            <form @submit.prevent.stop = "onGenreAdd()" v-if = "userInfoStore.hasPermissions('general.can_create_objects')">
                <div class = "row">
                    <div class = "col-3">
                        <div class = 'form-floating'>
                            <input type="text" class = 'form-control' v-model="genreToAdd.title" required>
                            <label for="floatingInput">Название</label>
                        </div>
                    </div>
                    <div class = "col">
                        <div class = 'form-floating'>
                            <input type="text" class = 'form-control' v-model="genreToAdd.description">
                            <label for="floatingInput">Описание</label>
                        </div>
                    </div>
                    <div class = "col-auto">
                        <button class = 'btn btn-primary'>Добавить</button>
                    </div>
                </div>
            </form>
            <div v-for="item in genres" class = 'genre-item'>
                <b>{{ item.title }}</b> 
                <b>{{ item.description }}</b> 
                <button v-if = "userInfoStore.hasPermissions('general.can_update_objects') && second == true"
                    class = 'btn btn-success' @click="onGenreEdit(item)"
                    data-bs-toggle="modal" 
                    data-bs-target="#editGenreModal">
                    <i class="bi bi-pen-fill"></i>
                </button>
                <button v-if = "userInfoStore.hasPermissions('general.can_delete_objects')"
                    class = 'btn btn-danger' @click="onGenreDelete(item)">
                    <i class="bi bi-x-lg"></i>
                </button>
            </div>
        </div>
    </div>
    <div v-if = "userInfoStore.hasPermissions('general.can_update_objects')" class="modal fade" id="editGenreModal" tabindex="-1">
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
                                    <input type="text" class = 'form-control' v-model="genreToEdit.title" required>
                                    <label for="floatingInput">Название</label>
                                </div>
                            </div>
                            <div class = "col">
                                <div class = 'form-floating'>
                                    <input type="text" class = 'form-control' v-model="genreToEdit.description">
                                    <label for="floatingInput">Описание</label>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
                    <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click = "onGenreUpdate()">
                        Сохранить изменения
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
    .genre-item{
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