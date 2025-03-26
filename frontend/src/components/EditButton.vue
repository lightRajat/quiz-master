<script setup>
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

<style scoped>
button {
    opacity: 0;
    transition: all 0.2s ease-out;
}
tr:hover button {
    opacity: 1;
    transition: none;
}
</style>