<script setup>
    import { computed, onBeforeMount, ref } from 'vue';
    import axios from 'axios';
    import Cookies from 'js-cookie';
    import _ from 'lodash';

    const directors = ref({});
    const directorToAdd = ref({});
    const directorToEdit = ref({});
    
    async function fetchDirectors(){
        const r = await axios.get("/api/directors/")
        console.log(r.data)
        directors.value = r.data
    }
    async function onDirectorAdd() {
        await axios.post("/api/directors/", {
            ...directorToAdd.value
        });
        await fetchDirectors();
    }
    async function onDirectorDelete(director){
        console.log(director);
        await axios.delete(`/api/directors/${director.id}/`);
        await fetchDirectors();
    }
    async function onDirectorEdit(director){
        directorToEdit.value = {...director};
    }
    async function onDirectorUpdate(){
        await axios.put(`/api/directors/${directorToEdit.value.id}/`,{
            ...directorToEdit.value,
        });
        await fetchDirectors();
    }

    onBeforeMount(async () => {
        axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
        await fetchDirectors();
    })
</script>

<template>
    <div class="container">
        <div class = "p-2">
            <form @submit.prevent.stop = "onDirectorAdd()">
                <div class = "row">
                    <div class = "col">
                        <div class = 'form-floating'>
                            <input type="text" class = 'form-control' v-model="directorToAdd.full_name" required>
                            <label for="floatingInput">ФИО</label>
                        </div>
                    </div>
                    <div class = "col-auto">
                        <div class = 'form-floating'>
                            <input type="date" class = 'form-control' v-model="directorToAdd.date_of_birth">
                            <label for="floatingInput">Дата рождения</label>
                        </div>
                    </div>
                </div>
                <br>
                <div class = "row">
                    <div class = "col">
                        <div class = 'form-floating'>
                            <input type="text" class = 'form-control' v-model="directorToAdd.short_biography">
                            <label for="floatingInput">Краткая биография</label>
                        </div>
                    </div>
                    <div class = "col-auto">
                        <button class = 'btn btn-primary'>Добавить</button>
                    </div>
                </div>
                <div v-for="item in directors" class = 'director-item'>
                    <b>{{ item.full_name }}</b> 
                    <b>{{ item.short_biography }}</b>
                    <b>{{ item.date_of_birth }}</b> 
                    <button class = 'btn btn-success' @click="onDirectorEdit(item)"
                        data-bs-toggle="modal" 
                        data-bs-target="#editDirectorModal">
                        <i class="bi bi-pen-fill"></i>
                    </button>
                    <button class = 'btn btn-danger' @click="onDirectorDelete(item)"><i class="bi bi-x-lg"></i></button>
                </div>
            </form>
        </div>
    </div>
    <div class="modal fade" id="editDirectorModal" tabindex="-1">
        <div class="modal-dialog modal-xl">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="exampleModalLabel">Редактирование</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Закрыть"></button>
                </div>
                <div class="modal-body">
                    <div class = "p-2">
                        <div class = "row">
                            <div class = "col">
                                <div class = 'form-floating'>
                                    <input type="text" class = 'form-control' v-model="directorToEdit.full_name" required>
                                    <label for="floatingInput">ФИО</label>
                                </div>
                            </div>
                            <div class = "col-auto">
                                <div class = 'form-floating'>
                                    <input type="date" class = 'form-control' v-model="directorToEdit.date_of_birth">
                                    <label for="floatingInput">Дата рождения</label>
                                </div>
                            </div>
                        </div>
                        <br>
                        <div class = "row">
                            <div class = "col">
                                <div class = 'form-floating'>
                                    <input type="text" class = 'form-control' v-model="directorToEdit.short_biography">
                                    <label for="floatingInput">Краткая биография</label>
                                </div>
                            </div>
                        </div>    
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
                    <button type="button" class="btn btn-primary" data-bs-dismiss="modal" @click = "onDirectorUpdate()">
                        Сохранить изменения
                    </button>
                </div>
            </div>
        </div>
    </div>  
</template>

<style scoped>
    .director-item{
        padding: 0.5rem;
        margin: 1rem 0;
        border: 1px solid silver;
        border-radius: 8px;
        display: grid;
        grid-template-columns: 0.5fr 1fr auto auto auto;
        column-gap: 10px;
        justify-content: space-between;
    }
</style>