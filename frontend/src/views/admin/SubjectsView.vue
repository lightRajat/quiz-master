<script setup>
import Card from '@/components/Card.vue';
import { reactive, onMounted, ref } from 'vue';
import { api } from '@/utils/auth';
import { RouterLink } from 'vue-router';
import DisabledInput from '@/components/DisabledInput.vue';
import EditButton from '@/components/EditButton.vue';
import DeleteButton from '@/components/DeleteButton.vue';

const state = reactive({
    subjects: []
});

const btnData = {
    text: "Add Subject",
    modalId: 'modal',
}

const editData = async (id) => {
    const subject = state.subjects.find((item) => item.id == id);
    subject.editable = !subject.editable;

    // update data on server
    if (!subject.editable) {
        try {
            const { editable: value, ...dataToSend } = subject;
            console.log(dataToSend);
            const response = await api.put(`/subject/${id}`, dataToSend);
            console.log(response.data);
            window.showToast("Subject Successfully Updated", 'success');
        } catch (error) {
            console.log(error.response.data);
        }
    }
};

const deleteData = (id) => {
    // delete data on frontend
    const itemIndex = state.subjects.findIndex((item) => item.id == id);
    state.subjects.splice(itemIndex, 1);
};

const formElem = ref(null);
const modalCloseBtnElem = ref(null);
const addData = async () => {
    // send data to server
    const formData = new FormData(formElem.value);
    try {
        const response = await api.post("/subjects", formData);
        window.showToast("Subject Successfully Added", 'success');
        modalCloseBtnElem.value.click();
        formElem.value.reset();

        // add data to frontend
        state.subjects.unshift(response.data.data);
    } catch (error) {
        window.showToast("Can't Add Subject", 'danger', error.response.data.info);
    }
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
                            <DisabledInput :text="row.name" :editable="row.editable"
                            @input-change="(newValue) => row.name = newValue" />
                        </td>
                        <td>
                            <DisabledInput :text="row.description" :editable="row.editable"
                            @input-change="(newValue) => row.description = newValue" />
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

                                <DeleteButton :editable="row.editable" :id="row.id"
                                resource-type="subject" @delete-success="deleteData(row.id)" />
                            </div>
                        </td>
                    </tr>
                    <tr v-if="state.subjects.length === 0">
                        <td colspan="4" class="text-center lead">No Data Available</td>
                    </tr>
                </tbody>
            </table>
        </Card>

        <div class="modal fade" id="modal" tabindex="-1" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <h1 class="modal-title fs-5" id="exampleModalLabel">Add Subject</h1>
                        <button ref="modalCloseBtnElem" type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>

                    <!-- body -->
                    <div class="modal-body">
                        <form ref="formElem" id="add-subject" @submit.prevent="addData">
                            <!-- name -->
                            <div class="mb-3">
                                <label class="form-label" for="name">Name*</label>
                                <input name="name" type="text" class="form-control"
                                :placeholder="state.subjects[0]?.name" id="name" required>
                            </div>

                            <!-- description -->
                            <div class="mb-3">
                                <label class="form-label" for="description">Description</label>
                                <textarea name="description" type="text" class="form-control"
                                :placeholder="state.subjects[0]?.description"
                                id="description"></textarea>
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                        <button type="submit" form="add-subject" class="btn btn-success">
                            <i class="bi bi-plus-lg me-1"></i>
                            Add
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>