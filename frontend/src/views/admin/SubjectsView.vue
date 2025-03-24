<script setup>
import Card from '@/components/Card.vue';
import { reactive, onMounted } from 'vue';
import { api } from '@/utils/auth';
import { RouterLink } from 'vue-router';
import DisabledInput from '@/components/DisabledInput.vue';
import EditButton from '@/components/EditButton.vue';

const state = reactive({
    subjects: []
});

const btnData = {
    text: "Add Subject",
    func: () => {
        alert("hi");
    }
}

const editData = (id) => {
    const subject = state.subjects.find((item) => item.id == id);
    subject.editable = !subject.editable;
};

onMounted(async () => {
    try {
        // fetch subjects
        const response = await api.get('/subjects');
        state.subjects = response.data.data;
        state.subjects.forEach((item) => item.editable = false);
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
                    <tr v-for="(row, rowIndex) in state.subjects" :key="rowIndex">
                        <th scope="row">{{ rowIndex + 1 }}</th>
                        <td>
                            <DisabledInput :text="row.name"
                            :editable="row.editable" />
                        </td>
                        <td>
                            <DisabledInput :text="row.description"
                            :editable="row.editable" />
                        </td>
                        <td class="d-flex">
                            <RouterLink :to="`/admin/subject/${row.id}`"
                            class="btn btn-primary d-flex me-3"
                            style="width: fit-content;">
                                <i class="bi bi-file-earmark me-1"></i>
                                View Chapters
                            </RouterLink>
                            <div class="btn-group" role="group">
                                <EditButton :editable="row.editable"
                                :func="() => editData(row.id)" />
                                <button class="btn btn-outline-danger"
                                :disabled="row.editable">
                                    <i class="bi bi-trash me-1"></i>
                                    Delete
                                </button>
                            </div>
                        </td>
                    </tr>
                    <tr v-if="state.subjects.length === 0">
                        <td colspan="4" class="text-center lead">No Data Available</td>
                    </tr>
                </tbody>
            </table>
        </Card>
    </div>
</template>