import { createRouter, createWebHistory } from 'vue-router'
import MoviesView from '@/views/MoviesView.vue'
import DirectorsView from '@/views/DirectorsView.vue'
import GenresView from '@/views/GenresView.vue'
import TypeMoviesView from '@/views/TypeMoviesView.vue'
import RatingMoviesView from '@/views/RatingMoviesView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "MoviesView",
      component: MoviesView
    },
    {
      path: "/directors",
      name: "DirectorsView",
      component: DirectorsView
    },
    {
      path: "/genres",
      name: "GenresView",
      component: GenresView
    },
    {
      path: "/type_movies",
      name: "TypeMoviesView",
      component: TypeMoviesView
    },
    {
      path: "/ratings",
      name: "RatingMoviesView",
      component: RatingMoviesView
    },
  ],
})

export default router
