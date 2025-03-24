<script setup>
import Card from '@/components/Card.vue';
import { RouterLink, useRoute } from 'vue-router';
import { ref, onMounted } from 'vue';
import { api } from '@/utils/auth';

const route = useRoute();

const chapters = ref([]);
const subjectName = ref('');
const subjectId = ref('0');

const btnData = {
    text: "Add Chapter",
    func: () => {
        alert("chapter added");
    }
}

onMounted(async () => {
    const pathSplit = route.path.split('/');
    subjectId.value = pathSplit[pathSplit.length - 1];
    try {
        // fecth chapters
        let response = await api.get(`/chapters?subject_id=${subjectId.value}`);
        console.log(response.data.data);
        chapters.value = response.data.data;

        // fecth subject name
        response = await api.get(`/subject/${subjectId.value}`);
        subjectName.value = response.data.data.name;
        document.title = subjectName.value;
    } catch (error) {
        console.log(error);
    }
});
</script>

<template>
    <div class="m-5">
        <Card :heading="chapters.length ? 'Chapters' : 'No Chapters Available'"
        :subheading="subjectName"
        :btn="btnData">
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
                    <tr v-for="(row, rowIndex) in chapters" :key="rowIndex">
                        <th scope="row">{{ rowIndex + 1 }}</th>
                        <td>{{ row.name }}</td>
                        <td>{{ row.description || "--- No Description Set ---" }}</td>
                        <td class="d-flex">
                            <RouterLink :to="`/admin/subject/${subjectId}/${row.id}`" class="btn btn-primary d-flex me-3">
                                <i class="bi bi-question-square me-1"></i>
                                View Questions
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
                    <tr v-if="chapters.length === 0">
                        <td colspan="4" class="text-center lead">No Data Available</td>
                    </tr>
                </tbody>
            </table>
        </Card>
    </div>
</template>