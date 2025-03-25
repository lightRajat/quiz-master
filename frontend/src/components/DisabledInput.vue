<script setup>

defineProps({
    text: String,
    editable: Boolean,
});

const emit = defineEmits(['inputChange']);

const updateProp = (event) => {
    emit('inputChange', event.target.value);
};
</script>

<template>
    <span v-if="!editable">{{ text || '--- No Data ---' }}</span>
    <input v-else type="text" :value="text" @input="updateProp">
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