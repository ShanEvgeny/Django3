<script setup>
    import { ref } from 'vue';
    import axios from 'axios';
    import { useUserInfoStore } from '@/stores/user_info_store';
    import { storeToRefs } from 'pinia';
    import { useRouter } from 'vue-router';

    const key = ref()
    const userInfoStore = useUserInfoStore()

    async function OnActivateSecondFactor() {
        await axios.post('/api/users/second-login/', {
            key: key.value
        });
        await userInfoStore.fetchUserInfo();
    }
</script>

<template>
    <div class = 'container'>
        <form @submit.stop.prevent="OnActivateSecondFactor()" class="form d-flex flex-column p-3" style = "gap: 8px">
            <input placeholder="Уникальный код" class = 'form-control' type="text" v-model="key" required>
            <button class = 'btn btn-primary'>Активировать второй фактор</button>
        </form>
    </div>
</template>

<style scoped>

</style>