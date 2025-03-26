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
    <input v-else type="text" :value="text" @change="updateProp">
</template>

<style scoped>
input {
    border: none;
    padding: 2px 6px;
    outline: none;
    width: 100%;;
    font-family: inherit;
    font-size: inherit;
    color: #000;
    cursor: text;
    background-color: #f4fcff;
    border-radius: 6px;
    
}
</style>