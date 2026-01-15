<script setup>;
    import axios from 'axios';
    import { useUserInfoStore } from './stores/user_info_store';
    import { storeToRefs } from 'pinia';
    import { useRouter } from 'vue-router';
    
    const router = useRouter();
    const userInfoStore = useUserInfoStore();
    const {
        username,
        is_authenticated,
        second
    } = storeToRefs(userInfoStore)

    async function onLogout() {
        const r = await axios.post('/api/users/logout/');
        await userInfoStore.fetchUserInfo();
        router.push('/login');
    }
    
</script>

<template>
    <div class="container-fluid">
        <nav class="navbar navbar-expand-lg navbar-light bg-light">
            <div class="container">
                <a class="navbar-brand"><i class="bi bi-film"></i></a>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarNav">
                    <ul class="navbar-nav">
                        <li class="nav-item">
                            <router-link class="nav-link active" to="/">Кино</router-link>
                        </li>
                        <li class="nav-item">
                            <router-link class="nav-link active" to="/directors">Режиссеры</router-link>
                        </li>
                        <li class="nav-item">
                            <router-link class="nav-link active" to="/genres">Жанры</router-link>
                        </li>
                        <li class="nav-item">
                            <router-link class="nav-link active" to="/type_movies">Типы кино</router-link>
                        </li>
                        <li class="nav-item">
                            <router-link class="nav-link active" to="/ratings">Оценки</router-link>
                        </li>
                        <li class="nav-item">
                            <router-link class="nav-link active" to="/stats">Статистика</router-link>
                        </li>
                        <li v-if = "second != true" class="nav-item">
                            <router-link class="nav-link active" to="/second-login">Второй фактор</router-link>
                        </li>
                    </ul>
                    <ul class = 'navbar-nav'>
                        <li class = "nav-item dropdown">
                            <a class = "nav-link dropdown-toggle" href="#" role = "button" data-bs-toggle="dropdown">
                                Пользователь
                            </a>
                            <ul class = 'dropdown-menu'>
                                <li>
                                    <a class = "dropdown-item" href="/admin">Админка</a>
                                </li>
                            </ul>
                        </li>
                        <li>
                            <button @click = "onLogout()" v-if="is_authenticated" class = "btn btn-danger">
                                Выйти
                            </button>
                        </li>
                    </ul>
                </div>
            </div>
        </nav>
    </div>
    <div class = "container">
        <b v-if = "second == false">
            Приветствую, {{ username }}! Для возможности редактирования, активируйте второй фактор
        </b>
        <router-view/>
    </div>
</template>

<style scoped>
    
</style>
