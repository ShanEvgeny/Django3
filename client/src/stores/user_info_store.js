import { defineStore } from "pinia";
import { ref, onBeforeMount } from "vue";
import axios from 'axios';
import Cookies from 'js-cookie';

export const useUserInfoStore = defineStore("userInfoStore", () => {
    const username = ref();
    const is_authenticated = ref();
    const is_staff = ref();
    const permissions = ref([]);
    const second = ref(null)

    async function fetchUserInfo(){
        const r = await axios.get('/api/users/my/');
        username.value = r.data.username;
        is_authenticated.value = r.data.is_authenticated;
        is_staff.value = r.data.is_staff;
        permissions.value = r.data.permissions;
        if (is_authenticated.value == true){
            second.value = r.data.second
        }
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
        is_staff,
        second,
        fetchUserInfo,
        hasPermissions
    }
})