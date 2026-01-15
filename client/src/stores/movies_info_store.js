import { defineStore } from "pinia";
import { ref, onBeforeMount } from "vue";
import axios from 'axios';
import Cookies from 'js-cookie';

export const useMoviesInfoStore = defineStore('moviesInfoStore', () => {
    const movies = ref([]);
    const typeMovies = ref([]);
    const directors = ref([]);
    const genres = ref([]);
    const ratingMovies = ref([]);

    async function fetchDirectors(){
        const r = await axios.get("/api/directors/")
        directors.value = r.data
    }
    async function fetchGenres(){
        const r = await axios.get("/api/genres/")
        genres.value = r.data
    }
    async function fetchTypeMovies(){
        const r = await axios.get("/api/type_movies/")
        typeMovies.value = r.data
    }
    async function fetchMovies(){
        const r = await axios.get("/api/movies/")
        movies.value = r.data
    }
    async function fetchRatingMovies(){
        const r = await axios.get("/api/ratings/")
        ratingMovies.value = r.data
    }
    return {
        movies,
        typeMovies,
        directors,
        genres,
        ratingMovies,
        fetchMovies,
        fetchTypeMovies,
        fetchDirectors,
        fetchGenres,
        fetchRatingMovies,
    } 
})