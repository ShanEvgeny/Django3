<script setup>
    import { useUserInfoStore } from '@/stores/user_info_store';
    const userInfoStore = useUserInfoStore();
</script>

<template>
    Оценки
    {{ userInfoStore.username }}
</template>

<style scoped>
    
</style>