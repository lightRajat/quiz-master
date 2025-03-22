<script setup>
import { useRouter } from 'vue-router';
import { onMounted, ref } from 'vue';

const router = useRouter();
const timeLeft = ref(3);

onMounted(() => {
    const intervalRef = setInterval(() => {
        timeLeft.value--;
        if (timeLeft.value == 0) {
            router.push('/');
            clearInterval(intervalRef);
        }
    }, 1000);
});
</script>

<template>
    <div class="container">
        <h1 class="text-danger">401 - Unauthorized</h1>
        <p class="lead">You don't have permission to access this page.</p>
        <img src="/src/assets/images/cat.jpg" alt="Unauthorized Access" class="img-fluid mt-3">
        <p class="text-muted mt-4">Redirecting to login in {{ timeLeft }} seconds ...</p>
    </div>
</template>

<style scoped>
body {
    background-color: #f8f9fa;
    text-align: center;
    padding: 50px;
}
.container {
    max-width: 500px;
    margin: auto;
    background: white;
    padding: 30px;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
img {
    width: 256px;
    height: 256px;
    border-radius: 10px;
}
</style>