import { createRouter, createWebHistory } from 'vue-router'
import MoviesView from '@/views/MoviesView.vue'
import DirectorsView from '@/views/DirectorsView.vue'
import GenresView from '@/views/GenresView.vue'
import TypeMoviesView from '@/views/TypeMoviesView.vue'
import RatingMoviesView from '@/views/RatingMoviesView.vue'
import StatsView from '@/views/StatsView.vue'
import Login from '@/views/Login.vue'
import { useUserInfoStore } from '@/stores/user_info_store'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/login",
      name: "Login",
      component: Login
    },
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
    {
      path:'/stats',
      name: "StatsView",
      component: StatsView
    },
  ],
})

router.beforeEach(async (to, from) => {
  const userInfoStore = useUserInfoStore();
  await userInfoStore.fetchUserInfo();
  if (!userInfoStore.is_authenticated && to.name !== 'Login'){
    return {
      name: 'Login'
    }
  }
})

export default router
