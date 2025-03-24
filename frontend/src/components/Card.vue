<script setup>
import { defineProps } from 'vue';

defineProps({
    heading: String,
    subheading: String
});
</script>

<template>
    <div class="card my-5 mx-auto">
        <div class="d-flex flex-column mx-auto align-items-start mt-3">
            <h3 v-if="subheading" class="h6 card-subtitle text-body-secondary">{{ subheading }}</h3>
            <h2 class="card-title card-body display-6 ps-0 pt-0 mb-0">{{ heading }}</h2>
        </div>
        <div class="card-body">
            <slot></slot>
        </div>
    </div>
</template>