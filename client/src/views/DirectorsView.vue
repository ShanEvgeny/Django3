<script setup>
    import { computed, onBeforeMount, ref } from 'vue';
    import axios from 'axios';
    import Cookies from 'js-cookie';
    import _ from 'lodash';
    import { useUserInfoStore } from '@/stores/user_info_store';

    const userInfoStore = useUserInfoStore();
    const directors = ref({});
    const directorToAdd = ref({});
    const directorToEdit = ref({});
    const directorsPictureRef = ref();
    const directorsEditPictureRef = ref();
    const directorAddImageURL = ref();
    const directorEditImageURL = ref();
    const directorModalImageURL = ref();
    const directorModalShortBiography = ref();
    
    async function fetchDirectors(){
        const r = await axios.get("/api/directors/")
        console.log(r.data)
        directors.value = r.data
    }
    async function onDirectorAdd() {
        const formData = new FormData();
        if (directorsPictureRef.value.files[0]){
            formData.append('picture',directorsPictureRef.value.files[0]);
        }
        formData.set('full_name',directorToAdd.value.full_name);
        formData.append('date_of_birth',directorToAdd.value.date_of_birth);
        formData.set('short_biography',directorToAdd.value.short_biography);
        await axios.post("/api/directors/", formData, {
            headers:{
                'Content-Type': 'multipart/form-data'
            }
            // ...directorToAdd.value
        });
        await fetchDirectors();
        directorToAdd.value = {}
        directorsPictureRef.value.value = ''
        directorAddImageURL.value = ''
    }
    async function onDirectorDelete(director){
        console.log(director);
        await axios.delete(`/api/directors/${director.id}/`);
        await fetchDirectors();
    }
    async function onDirectorEdit(director){
        directorsEditPictureRef.value.value = ''
        directorToEdit.value = {...director};
        directorEditImageURL.value = directorToEdit.value.picture
    }
    async function onDirectorUpdate(){
        const formData = new FormData();
        if (directorsEditPictureRef.value.files[0]){
            formData.append('picture',directorsEditPictureRef.value.files[0]);
        }
        formData.set('full_name',directorToEdit.value.full_name);
        formData.append('date_of_birth', directorToEdit.value.date_of_birth);
        formData.set('short_biography',directorToEdit.value.short_biography);
        await axios.put(`/api/directors/${directorToEdit.value.id}/`, formData, {
            // ...directorToEdit.value,
            headers:{
                'Content-Type': 'multipart/form-data'
            }
        });
        await fetchDirectors();
        directorToEdit.value = {}
    }
    async function directorAddPictureChange(){
        directorAddImageURL.value = URL.createObjectURL(directorsPictureRef.value.files[0])
    }
    async function directorEditPictureChange(){
        console.log(123)
        directorEditImageURL.value = URL.createObjectURL(directorsEditPictureRef.value.files[0])
    }
    async function onClickDirectorPicture(picture){
        console.log(picture)
        directorModalImageURL.value = picture
    }
    async function onClickDirectorShortBiography(short_biography) {
        directorModalShortBiography.value = short_biography
    }

    onBeforeMount(async () => {
        axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
        await fetchDirectors();
    })
</script>

<template>
    <div class="container">
        <div class = "p-2">
            <form @submit.prevent.stop = "onDirectorAdd()" v-if = "userInfoStore.hasPermissions('general.can_create_objects')">
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
                    <div class = "col-auto">
                        <input class = "form-control" type="file" ref = "directorsPictureRef" @change="directorAddPictureChange()">
                    </div>
                    <div class = "col-auto">
                        <img :src="directorAddImageURL" style = "max-height: 60px;" alt="">
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
            </form>
            <div v-for="item in directors" class = 'director-item'>
                <b>{{ item.full_name }}</b> 
                <b>
                    <div class = 'short-biography' data-bs-toggle="modal" 
                        data-bs-target="#shortBiographyModal"
                        @click = "onClickDirectorShortBiography(item.short_biography)">
                        {{ item.short_biography }}
                    </div>
                </b>
                <b>{{ item.date_of_birth }}</b>
                <div v-show = "item.picture" data-bs-toggle="modal" data-bs-target="#pictureModal">
                    <img :src="item.picture" style = "max-height: 60px;" @click="onClickDirectorPicture(item.picture)">
                </div> 
                <button v-if = "userInfoStore.hasPermissions('general.can_update_objects')"
                    class = 'btn btn-success' @click="onDirectorEdit(item)"
                    data-bs-toggle="modal" 
                    data-bs-target="#editDirectorModal">
                    <i class="bi bi-pen-fill"></i>
                </button>
                <button v-if = "userInfoStore.hasPermissions('general.can_delete_objects')"
                    class = 'btn btn-danger' @click="onDirectorDelete(item)">
                    <i class="bi bi-x-lg"></i>
                </button>
            </div>
        </div>
    </div>
    <div v-if = "userInfoStore.hasPermissions('general.can_update_objects')" class="modal fade" id="editDirectorModal" tabindex="-1">
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
                            <div class = "col-auto">
                                <input class = "form-control" type="file" ref = "directorsEditPictureRef" @change="directorEditPictureChange()">
                            </div>
                            <div class = "col-auto">
                                <img :src="directorEditImageURL" style = "max-height: 60px;" alt="">
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
    <div class="modal fade" id="pictureModal" tabindex="-1">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Изображение</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Закрыть"></button>
                </div>
                <div v-show = "directorModalImageURL" class="modal-body">
                    <img :src="directorModalImageURL" style = "max-height: 500px;" alt="">
                </div>
            </div>
        </div>
    </div>
    <div class="modal fade" id="shortBiographyModal" tabindex="-1">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Краткая биография</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Закрыть"></button>
                </div>
                <div class="modal-body">
                    <b>{{ directorModalShortBiography }}</b>
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
        grid-template-columns: 0.5fr 1fr auto auto auto auto;
        column-gap: 10px;
        justify-content: space-between;
    }
    .short-biography {
        display: -webkit-box;
        line-clamp: 1;
        -webkit-line-clamp: 1;
        -webkit-box-orient: vertical;
        overflow: hidden
    }
</style>