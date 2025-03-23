<script setup>
import { defineProps } from 'vue';

defineProps({
    heading: String
});
</script>

<template>
    <div class="card my-5 mx-auto">
        <h2 class="card-title text-center card-body display-6 mb-0">{{ heading }}</h2>
        <div class="card-body">
            <slot></slot>
        </div>
    </div>
</template>