<script setup>
    import { RouterView } from 'vue-router';
</script>

<template>
    <main class="container my-5">
        <h1 class="display-2 text-center my-4">Quiz Master</h1>
        <div class="card mx-auto">
            <RouterView />
        </div>
    </main>
</template>

<style scoped>
    main > div {
        width: fit-content;
    }
</style>