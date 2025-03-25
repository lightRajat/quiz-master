<script setup>
import Card from '@/components/Card.vue';
import { RouterLink, useRoute } from 'vue-router';
import { onMounted, reactive } from 'vue';
import { api } from '@/utils/auth';
import DisabledInput from '@/components/DisabledInput.vue';
import EditButton from '@/components/EditButton.vue';
import DeleteButton from '@/components/DeleteButton.vue';

const route = useRoute();

const state = reactive({
    chapters: [],
    subject: {name: '', id: ''},
});

const btnData = {
    text: "Add Chapter",
    func: () => {
        alert("chapter added");
    }
}

const editData = async (id) => {
    const chapter = state.chapters.find((item) => item.id === id);
    chapter.editable = !chapter.editable;

    // update data on server
    if (!chapter.editable) {
        try {
            const { editable: value, ...dataToSend } = chapter;
            console.log(dataToSend);
            const response = await api.put(`/chapter/${id}`, dataToSend);
            console.log(response.data);
            window.showToast("Chapter Successfully Updated", 'success');
        } catch (error) {
            console.log(error.response?.data || error);
        }
    }
};

const deleteData = (id) => {
    // delete data on frontend
    const itemIndex = state.chapters.findIndex((item) => item.id == id);
    state.chapters.splice(itemIndex, 1);
};

onMounted(async () => {
    const pathSplit = route.path.split('/');
    state.subject.id = pathSplit[pathSplit.length - 1];
    try {
        // fetch chapters
        let response = await api.get(`/chapters?subject_id=${state.subject.id}`);
        state.chapters = response.data.data;
        state.chapters.forEach((item) => item.editable = false);

        // fetch subject name
        response = await api.get(`/subject/${state.subject.id}`);
        state.subject.name = response.data.data.name;
        document.title = state.subject.name;
    } catch (error) {
        console.log(error);
    }
});
</script>

<template>
    <div class="m-5">
        <Card :heading="state.chapters.length ? 'Chapters' : 'No Chapters Available'"
        :subheading="state.subject.name"
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
                    <tr v-for="(row, rowIndex) in state.chapters" :key="rowIndex">
                        <th scope="row">{{ rowIndex + 1 }}</th>
                        <td>
                            <DisabledInput :text="row.name" :editable="row.editable"
                            @input-change="(newValue) => row.name = newValue" />
                        </td>
                        <td>
                            <DisabledInput :text="row.description" :editable="row.editable"
                            @input-change="(newValue) => row.description = newValue" />
                        </td>
                        <td class="d-flex">
                            <RouterLink :to="`/admin/subject/${state.subject.id}/${row.id}`"
                            class="btn btn-primary d-flex me-3">
                                <i class="bi bi-question-square me-1"></i>
                                View Questions
                            </RouterLink>
                            <div class="btn-group" role="group">
                                <EditButton :editable="row.editable"
                                :func="() => editData(row.id)" />

                                <DeleteButton :editable="row.editable" :id="row.id"
                                resource-type="chapter" @delete-success="deleteData" />
                            </div>
                        </td>
                    </tr>
                    <tr v-if="!state.chapters.length">
                        <td colspan="4" class="text-center lead">No Data Available</td>
                    </tr>
                </tbody>
            </table>
        </Card>
    </div>
</template>