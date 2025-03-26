<script setup>
import { api } from '@/utils/auth';

const props = defineProps({
    editable: Boolean,
    id: Number,
    resourceType: String,
});

const emit = defineEmits(['deleteSuccess']);

const deleteData = async (id) => {
    const deleteConfirm = window.confirm("Are you sure you want to delete this item?");
    if (deleteConfirm) {
        const resourceName = props.resourceType[0].toUpperCase() + props.resourceType.slice(1)
        try {
            const response = await api.delete(`/${props.resourceType}/${props.id}`);
            console.log(response.data);
            emit('deleteSuccess', props.id);
            window.showToast(`${resourceName} Successfully Deleted`, 'success');
        } catch (error) {
            console.log(error.response?.data || error);
            window.showToast(`Can't Delete ${resourceName}`, 'danger', error.response.data.info);
        }
    }
};
</script>

<template>
    <button class="btn btn-outline-danger" :disabled="editable"
    @click="deleteData(id)">
        <i class="bi bi-trash me-1"></i>
        Delete
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