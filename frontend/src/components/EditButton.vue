<script setup>
defineProps({
    editable: Boolean,
    func: Function,
});
</script>

<template>
    <button class="btn" @click="func"
    :class="{'btn-success': editable, 'btn-outline-secondary edit-btn' : !editable}">
        <i class="bi me-1"
        :class="`bi-${editable ? 'check-lg' : 'pencil'}`"></i>
        {{ editable ? 'Done' : 'Edit' }}
    </button>
</template>

<style scoped>
.edit-btn {
    opacity: 0.6;
    transition: all 0.2s ease-out;
}
tr:hover .edit-btn {
    opacity: 1;
    transition: none;
}
</style>