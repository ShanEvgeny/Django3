import { defineStore } from "pinia";
import { ref, onBeforeMount } from "vue";
import axios from 'axios';
import Cookies from 'js-cookie';

export const useUserInfoStore = defineStore("userInfoStore", () => {
    const username = ref();
    const is_authenticated = ref();
    const permissions = ref([]);

    async function fetchUserInfo(){
        const r = await axios.get('/api/users/my/');
        username.value = r.data.username;
        is_authenticated.value = r.data.is_authenticated;
        permissions.value = r.data.permissions;
        axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");
    }
    function hasPermissions(name){
        return permissions.value.includes(name)
    }
    onBeforeMount(async () => {
        await fetchUserInfo();
    })
    return {
        username,
        is_authenticated,
        fetchUserInfo,
        hasPermissions
    }
})