<script setup>
import Card from '@/components/Card.vue';
import { ref, onMounted } from 'vue';
import { api } from '@/utils/auth';
import { RouterLink } from 'vue-router';

const subjects = ref([]);

const btnData = {
    text: "Add Subject",
    func: () => {
        alert("hi");
    }
}

onMounted(async () => {
    try {
        const response = await api.get('/subjects');
        subjects.value = response.data.data;
    } catch (error) {
        console.log(error);
    }
});
</script>

<template>
    <div class="m-5">
        <Card heading="All Subjects" :btn="btnData">
            <table class="table table-striped table-hover align-middle">
                <thead>
                    <tr>
                        <th scope="col">#</th>
                        <th scope="col">Name</th>
                        <th scope="col">Description</th>
                        <th scope="col">Action</th>
                    </tr>
                </thead>
                <tbody class="table-group-divider">
                    <tr v-for="(row, rowIndex) in subjects" :key="rowIndex">
                        <th scope="row">{{ rowIndex + 1 }}</th>
                        <td>{{ row.name }}</td>
                        <td>{{ row.description || "--- No Description Set ---" }}</td>
                        <td class="d-flex">
                            <RouterLink :to="`/admin/subject/${row.id}`" class="btn btn-primary d-flex me-3" style="width: fit-content;">
                                <i class="bi bi-file-earmark me-1"></i>
                                View Chapters
                            </RouterLink>
                            <div class="btn-group" role="group">
                                <button class="btn btn-outline-secondary">
                                    <i class="bi bi-pencil me-1"></i>
                                    Edit
                                </button>
                                <button class="btn btn-outline-danger">
                                    <i class="bi bi-trash me-1"></i>
                                    Delete
                                </button>
                            </div>
                        </td>
                    </tr>
                    <tr v-if="subjects.length === 0">
                        <td colspan="4" class="text-center lead">No Data Available</td>
                    </tr>
                </tbody>
            </table>
        </Card>
    </div>
</template>