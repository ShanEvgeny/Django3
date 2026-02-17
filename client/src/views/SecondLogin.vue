<script setup>
    import { ref, watch } from 'vue';
    import axios from 'axios';
    import { useUserInfoStore } from '@/stores/user_info_store';
    import { storeToRefs } from 'pinia';
    import { useRouter } from 'vue-router';
    import QRCode from 'qrcode';


    const key = ref();
    const userInfoStore = useUserInfoStore();
    const totpURL = ref();
    const qrcodeURL = ref();
    const {
        second
    } = storeToRefs(userInfoStore)
    const router = useRouter();

    watch(totpURL, async () => {
        qrcodeURL.value = await QRCode.toDataURL(totpURL.value);
    })
    async function onActivateSecondFactor() {
        await axios.post('/api/users/second-login/', {
            key: key.value
        });
        await userInfoStore.fetchUserInfo();
        if (second.value == true){
            router.push('/')
        }
    }
    async function getTotpKey() {
        let r = await axios.get('/api/users/get-totp/');
        totpURL.value = r.data.url;
    }
</script>

<template>
    <div class = 'container'>
        <div>{{ totpURL }}</div>
        <div style = "text-align: center;">
            <img :src="qrcodeURL" alt="">
        </div>
        <div class="d-flex flex-column p-3" style = "gap: 8px">
            <input placeholder="Уникальный код" class = 'form-control' type="text" v-model="key">
            <button @click = "onActivateSecondFactor()" class = 'btn btn-primary'>Активировать второй фактор</button>
            <button @click="getTotpKey" class = 'btn btn-success'>Запросить ключ</button>
        </div>
    </div>
</template>

<style scoped>

</style>