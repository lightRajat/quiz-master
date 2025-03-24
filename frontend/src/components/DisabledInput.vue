<script setup>
import { defineProps } from 'vue';

defineProps({
    text: String,
    editable: Boolean,
});
</script>

<template>
    <span v-if="!editable">{{ text || '--- No Data ---' }}</span>
    <input v-else type="text" :value="text">
</template>

<style scoped>
input {
    border: none;
    padding: 2px;
    outline: none;
    width: 100%;;
    font-family: inherit;
    font-size: inherit;
    color: inherit;
    cursor: text;
}
</style>