<script setup>
    import { computed, onBeforeMount, ref } from 'vue';
    import axios from 'axios';
    import Cookies from 'js-cookie';
    import { useUserInfoStore } from '@/stores/user_info_store';
    import { storeToRefs } from 'pinia';
    import { useRouter } from 'vue-router';

    const username = ref();
    const password = ref();
    const userInfoStore = useUserInfoStore();
    const {
        is_authenticated
    } = storeToRefs(userInfoStore)
    const router = useRouter()

    async function onLoginFormSublit(){
        const r = await axios.post('/api/users/login/',{
            username: username.value,
            password: password.value,
        })
        username.value = '';
        password.value = '';
        await userInfoStore.fetchUserInfo();
        if (is_authenticated.value){
            router.push('/')
        }
    }
</script>

<template>
    <div class = 'container'>
        <form @submit.stop.prevent="onLoginFormSublit()" class="form d-flex flex-column p-3" style = "gap: 8px">
            <input placeholder="логин" class = 'form-control' type="text" v-model="username">
            <input placeholder="пароль" class = 'form-control' type="password" v-model="password">
            <button class = 'btn btn-primary'>Войти</button>
        </form>
    </div>
</template>

<style scoped>

</style>