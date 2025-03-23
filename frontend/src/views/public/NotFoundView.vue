<script setup>
import { useRouter } from 'vue-router';
import { onMounted, ref } from 'vue';

const router = useRouter();
const timeLeft = ref(3);

onMounted(() => {
    const intervalRef = setInterval(() => {
        timeLeft.value--;
        if (timeLeft.value == 0) {
            router.go(-1);
            clearInterval(intervalRef);
        }
    }, 1000);
});
</script>

<template>
    <div class="container">
        <h1 class="text-danger">404 - Page Not Found</h1>
        <p class="lead">Oops! Looks like you've wandered into the void.</p>
        <img :src="'src/assets/images/cat.jpg'" alt="Cat" class="img-fluid mt-3">
        <p class="mt-4">
            <button @click="() => router.go(-1)" class="btn btn-primary">Go Back</button>
        </p>
        <p id="countdown-text" class="text-muted">Going back in {{ timeLeft }} seconds...</p>
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