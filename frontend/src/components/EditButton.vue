<script setup>
import { defineProps } from 'vue';

defineProps({
    editable: Boolean,
    func: Object,
});
</script>

<template>
    <button class="btn" @click="func"
    :class="`btn-${editable ? 'success' : 'outline-secondary'}`">
        <i class="bi me-1"
        :class="`bi-${editable ? 'check-lg' : 'pencil'}`"></i>
        {{ editable ? 'Done' : 'Edit' }}
    </button>
</template>