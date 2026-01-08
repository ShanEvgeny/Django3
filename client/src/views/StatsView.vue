<script setup>
    import { computed, onBeforeMount, ref } from 'vue';
    import axios from 'axios';
    import Cookies from 'js-cookie';
    import _ from 'lodash';
    const moviesStats = ref({});
    const directorsStats = ref({});
    const genresStats = ref({});
    const typeMoviesStats = ref({});
    const ratingMoviesStats = ref({});
    async function fetchMoviesStats() {
        const r = await axios.get("/api/movies/stats/")
        console.log(123)
        console.log(r.data)
        moviesStats.value = r.data
    }
    async function fetchDirectorsStats(){
        const r = await axios.get("/api/directors/stats/")
        console.log(r.data)
        directorsStats.value = r.data
    }
    async function fetchGenresStats(){
        const r = await axios.get("/api/genres/stats/")
        console.log(r.data)
        genresStats.value = r.data
    }
    async function fetchTypeMoviesStats(){
        const r = await axios.get("/api/type_movies/stats/")
        console.log(r.data)
        typeMoviesStats.value = r.data
    }
    async function fetchRatingMoviesStats(){
        const r = await axios.get("/api/ratings/stats/")
        console.log(r.data)
        ratingMoviesStats.value = r.data
    }
    onBeforeMount(async () => {
        axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
        await fetchMoviesStats();
        await fetchTypeMoviesStats();
        await fetchDirectorsStats();
        await fetchGenresStats();
        await fetchRatingMoviesStats();
    })
</script>

<template>
    <div class="container">
        <div class="p-2">
            <h2>Статистика по кино</h2>
            <div class = "stats">
                <b>Число киноработ:<br>{{ moviesStats.count_movies }}</b>
                <b>Средний год выхода киноработ:<br>{{ moviesStats.avg_year_of_release.toFixed(1) }}</b>
                <b>Самая старая вышел в:<br>{{ moviesStats.oldest_movie }}</b>
                <b>Самая новая вышел в:<br>{{ moviesStats.newest_movie }}</b>
                <b>Лучший фильм по оценкам:<br>{{ moviesStats.best_movie }}</b>
            </div>
            <h2>Статистика по режиссерам</h2>
            <div class = "stats">
                <b>Число режиссеров: {{ directorsStats.count_directors }}</b>
                <b>Средний год рождения: {{ directorsStats.avg_birthday.toFixed(1) }}</b>
                <b>Самый ранний год рождения режиссера: {{ directorsStats.earliest_birthday }}</b>
                <b>Самый поздний год рождения: {{ directorsStats.latest_birthday }}</b>
                <b>Наибольшее количество киноработ срежиссировал: {{ directorsStats.most_productive_director }}</b>
            </div>
            <h2>Статистика по жанрам</h2>
            <div class="stats2">
                <b>Число жанров: {{ genresStats.count }}</b>
                <b>Минимальное число фильмов в жанре: {{ genresStats.min }}</b>
                <b>Максимальное число фильмов в жанре: {{ genresStats.max }}</b>
                <b>Самый популярный жанр: {{ genresStats.most_popular_genre }}</b>
            </div>
            <h2>Статистика по типам кино</h2>
            <div class="stats2">
                <b>Число типов кино: {{ typeMoviesStats.count }}</b>
                <b>Минимальное число фильмов типа: {{ typeMoviesStats.min }}</b>
                <b>Максимальное число фильмов типа: {{ typeMoviesStats.max }}</b>
                <b>Самый популярный тип кино: {{ typeMoviesStats.most_popular_type_movie }}</b>
            </div>
            <h2>Статистика по оценкам</h2>
            <div class="stats2">
                <b>Число оценок: {{ ratingMoviesStats.count_ratings }}</b>
                <b>Средняя оценка: {{ ratingMoviesStats.avg_rating.toFixed(1) }}</b>
                <b>Минимальная оценка: {{ ratingMoviesStats.min_rating }}</b>
                <b>Максимальная оценка: {{ ratingMoviesStats.max_rating }}</b>
            </div>
        </div>
    </div>
</template>

<style scoped>
    .stats{
        padding: 0.5rem;
        margin: 1rem 0;
        border: 1px solid silver;
        border-radius: 8px;
        display: grid;
        grid-template-columns: 0.5fr 0.5fr 0.5fr 0.5fr 0.5fr;
        column-gap: 10px;
        justify-content: space-between;
        /* background-color: rgb(182, 136, 182); */
    }
    .stats2{
        padding: 0.5rem;
        margin: 1rem 0;
        border: 1px solid silver;
        border-radius: 8px;
        display: grid;
        grid-template-columns: 0.5fr 0.5fr 0.5fr 0.5fr;
        column-gap: 10px;
        justify-content: space-between;
        /* background-color: rgb(182, 136, 182); */
    }
</style>