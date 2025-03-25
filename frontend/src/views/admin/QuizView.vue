<script setup>
import Card from '@/components/Card.vue';
import DisabledInput from '@/components/DisabledInput.vue';
import EditButton from '@/components/EditButton.vue';
import DeleteButton from '@/components/DeleteButton.vue';
import { api } from '@/utils/auth';
import { onMounted, reactive, ref } from 'vue';

const state = reactive({
    quizzes: [],
    subjects: [],
    chapters: [],
    form: {
        scope: 'subject',
        subjectId: '',
    },
});

const btnData = {
    text: "Add Quiz",
    modalId: 'modal',
}

const editData = async (id) => {
    const quiz = state.quizzes.find((item) => item.id == id);
    quiz.editable = !quiz.editable;

    // update data on server
    if (!quiz.editable) {
        try {
            // prepare data
            const { editable: value, subject_name: value2, ...dataToSend } = quiz;
            if (dataToSend.chapter_name) {
                delete dataToSend.chapter_id;
            }
            
            const response = await api.put(`/quiz/${id}`, dataToSend);
            window.showToast("Quiz Successfully Updated", 'success');
        } catch (error) {
            console.log(error.response?.data || error);
        }
    }
};

const deleteData = (id) => {
    // delete data on frontend
    const itemIndex = state.quizzes.findIndex((item) => item.id == id);
    state.quizzes.splice(itemIndex, 1);
};

const formElem = ref(null);
const modalCloseBtnElem = ref(null);
const addData = async () => {
    // prepare data
    const formData = new FormData(formElem.value);
    if (formData.get('scope') === 'chapter') {
        formData.delete('subject_id');
    }

    // send data to server
    try {
        const response = await api.post("/quizzes", formData);
        window.showToast("Quiz Successfully Added", 'success');
        modalCloseBtnElem.value.click();
        formElem.value.reset();

        // add data to frontend
        state.quizzes.unshift(response.data.data);
        updateScopeNames();
    } catch (error) {
        window.showToast("Can't Add Quiz", 'danger', error.response.data.info);
    }
};

const updateScopeNames = () => {
    state.quizzes.forEach((quiz) => {
        let chapter;
        if (quiz.scope === 'chapter') {
            chapter = state.chapters.find((chapter) => chapter.id == quiz.chapter_id);
            quiz.chapter_name = chapter.name;
        }
        const subjectId = quiz.scope === 'subject' ? quiz.subject_id : chapter.subject_id;

        const subject = state.subjects.find((subject) => subject.id == subjectId);
        quiz.subject_name = subject.name;
    });
};

onMounted(async () => {
    try {
        // fetch subjects
        let response = await api.get('/subjects');
        state.subjects = response.data.data;

        // fetch chapters
        response = await api.get('/chapters');
        state.chapters = response.data.data;

        // fetch quizzes
        response = await api.get('/quizzes');
        state.quizzes = response.data.data;
        state.quizzes.forEach((item) => item.editable = false);
        updateScopeNames();
    } catch (error) {
        console.log(error.response?.data || error);
    }
});
</script>

<template>
    <div class="m-5">
        <Card heading="All Quizzes" :btn="btnData">
            <table class="table table-striped table-hover align-middle">
                <!-- table head -->
                <thead>
                    <tr>
                        <th scope="col">#</th>
                        <th scope="col">Scope</th>
                        <th scope="col">Time</th>
                        <th scope="col">Description</th>
                        <th scope="col">Action</th>
                    </tr>
                </thead>
                <!-- table body -->
                <tbody class="table-group-divider">
                    <tr v-for="(row, index) in state.quizzes" :key="index">
                        <!-- id -->
                        <th scope="row">{{ index + 1 }}</th>

                        <!-- scope name -->
                        <td>
                            <h6 v-if="row.scope === 'chapter'" class="text-secondary">
                                {{ row.subject_name }}
                            </h6>
                            <h5>
                                {{ row.scope === 'subject' ? row.subject_name : row.chapter_name }}
                            </h5>
                        </td>

                        <!-- time -->
                        <td>
                            <DisabledInput :text="row.time" :editable="row.editable"
                            @input-change="(newValue) => row.time = newValue" /> mins
                        </td>

                        <!-- description -->
                        <td>
                            <DisabledInput :text="row.description" :editable="row.editable"
                            @input-change="(newValue) => row.description = newValue" />
                        </td>
                        <td class="d-flex">
                            <RouterLink :to="`#`"
                            class="btn btn-primary d-flex me-3"
                            style="width: fit-content;">
                                <i class="bi bi-question-square me-1"></i>
                                View Questions
                            </RouterLink>
                            <div class="btn-group" role="group">
                                <EditButton :editable="row.editable"
                                :func="() => editData(row.id)" />

                                <DeleteButton :editable="row.editable" :id="row.id"
                                resource-type="quiz" @delete-success="deleteData(row.id)" />
                            </div>
                        </td>
                    </tr>
                    <tr v-if="state.quizzes.length === 0">
                        <td colspan="4" class="text-center lead">No Data Available</td>
                    </tr>
                </tbody>
            </table>
        </Card>

        <div class="modal fade" id="modal" tabindex="-1" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <!-- header -->
                    <div class="modal-header">
                        <h1 class="modal-title fs-5" id="exampleModalLabel">Add Quiz</h1>
                        <button ref="modalCloseBtnElem" type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>

                    <!-- body -->
                    <div class="modal-body">
                        <form ref="formElem" id="add-data" @submit.prevent="addData">

                            <!-- scope -->
                            <div class="mb-3">
                                <span class="me-4">Scope*</span>
                                <div class="form-check form-check-inline">
                                    <input class="form-check-input" type="radio" required
                                    name="scope" id="scope_chapter" v-model="state.form.scope"
                                    value="chapter" @change="fetchScopesForForm">
                                    <label class="form-check-label" for="scope_chapter">Chapter</label>
                                </div>
                                <div class="form-check form-check-inline">
                                    <input class="form-check-input" type="radio" required
                                    name="scope" id="scope_subject" v-model="state.form.scope"
                                    value="subject" @change="fetchScopesForForm">
                                    <label class="form-check-label" for="scope_subject">Subject</label>
                                </div>
                            </div>

                            <!-- select subject -->
                            <div class="mb-3">
                                <label class="form-label">Select Subject*</label>
                                <select class="form-select" name="subject_id" id="subject_id"
                                v-model="state.form.subjectId">
                                    <option v-for="(item, index) in state.subjects" :key="index"
                                    :value="item.id">
                                        {{ item.name }}
                                    </option>
                                </select>
                            </div>

                            <!-- select chapter -->
                            <div class="mb-3" v-if="state.form.scope === 'chapter'">
                                <label class="form-label">Select Chapter*</label>
                                <select class="form-select" name="chapter_id">
                                    <option v-for="(item, index) in state.chapters.filter((chapter) => chapter.subject_id == state.form.subjectId)" :key="index"
                                    :value="item.id">
                                        {{ item.name }}
                                    </option>
                                </select>
                            </div>

                            <!-- time -->
                            <div class="mb-3">
                                <label class="form-label" for="time">Time*</label>
                                <input name="time" type="number" class="form-control"
                                :placeholder="state.quizzes[0]?.time" id="time" required>
                            </div>

                            <!-- description -->
                            <div class="mb-3">
                                <label class="form-label" for="description">Description</label>
                                <textarea name="description" type="text" class="form-control"
                                :placeholder="state.quizzes[0]?.description" id="description"></textarea>
                            </div>
                        </form>
                    </div>

                    <!-- footer -->
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary"
                        data-bs-dismiss="modal">Cancel</button>

                        <button type="submit" form="add-data" class="btn btn-success">
                            <i class="bi bi-plus-lg me-1"></i>
                            Add
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
h5, h6 {
    padding: 0;
    margin: 0;
}

h6 {
    font-size: 0.8rem;
}

h5 {
    font-size: 1.4rem;
}
</style>