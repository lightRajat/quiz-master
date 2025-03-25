<script setup>
import Card from '@/components/Card.vue';
import { onMounted, reactive, ref } from 'vue';
import { api } from '@/utils/auth';
import { useRoute } from 'vue-router';
import DisabledInput from '@/components/DisabledInput.vue';
import EditButton from '@/components/EditButton.vue';
import DeleteButton from '@/components/DeleteButton.vue';

const route = useRoute();

const state = reactive({
    questions: [],
    chapter: {name: '', id: ''},
});

const btnData = {
    text: "Add Question",
    modalId: 'modal',
}

const editData = async (id) => {
    const question = state.questions.find((item) => item.id == id);
    question.editable = !question.editable;

    // update data on server
    if (!question.editable) {
        try {
            const { editable: value, ...dataToSend } = question;
            dataToSend.correct_option = dataToSend.correct_option.toLowerCase();
            console.log(question);
            const response = await api.put(`/question/${id}`, dataToSend);
            console.log(response.data);
            window.showToast("Question Successfully Updated", 'success');
        } catch (error) {
            console.log(error.response?.data || error);
        }
    }
};

const deleteData = (id) => {
    // delete data on frontend
    const itemIndex = state.questions.findIndex((item) => item.id == id);
    state.questions.splice(itemIndex, 1);
};

const formElem = ref(null);
const modalCloseBtnElem = ref(null);
const addData = async () => {
    // prepare data
    const formData = new FormData(formElem.value);
    formData.set('chapter_id', state.chapter.id);
    try {
        const response = await api.post("/questions", formData);
        window.showToast("Question Successfully Added", 'success');
        modalCloseBtnElem.value.click();
        formElem.value.reset();

        // add data to frontend
        state.questions.unshift(response.data.data);
    } catch (error) {
        window.showToast("Can't Add Question", 'danger', error.response.data.info);
    }
};

onMounted(async () => {
    const pathSplit = route.path.split('/');
    state.chapter.id = pathSplit[pathSplit.length - 1];
    try {
        // fetch questions
        let response = await api.get(`/questions?chapter_id=${state.chapter.id}`);
        state.questions = response.data.data;
        state.questions.forEach((item) => item.editable = false);

        // fetch chapter name
        response = await api.get(`/chapter/${state.chapter.id}`);
        state.chapter.name = response.data.data.name;
        document.title = state.chapter.name;
    } catch (error) {
        console.log(error);
    }
});
</script>

<template>
    <div class="m-3">
        <Card :heading="state.questions.length ? 'Questions' : 'No Questions Available'"
        :subheading="state.chapter.name" :btn="btnData">
            <div v-for="(question, index) in state.questions" :key="index" class="card m-5">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-center">
                        <!-- question -->
                        <p class="h5">
                            <span class="me-3">{{ index + 1 }}.</span>
                            <DisabledInput :text="question.question"
                            :editable="question.editable"
                            @input-change="(newValue) => question.question = newValue" />
                        </p>

                        <!-- edit delete buttons -->
                        <div class="btn-group" role="group">
                            <EditButton :editable="question.editable"
                            :func="() => editData(question.id)" />

                            <DeleteButton :editable="question.editable" :id="question.id"
                            @delete-success="deleteData(question.id)" resource-type="question" />
                        </div>
                    </div>

                    <!-- options -->
                    <ul>
                        <div>
                            <li>
                                <div>A. </div>
                                <div>
                                    <DisabledInput :text="question.option_a"
                                    :editable="question.editable"
                                    @input-change="(newValue) => question.option_a = newValue" />
                                </div>
                            </li>
                            <li>
                                <div>B. </div>
                                <div>
                                    <DisabledInput :text="question.option_b"
                                    :editable="question.editable"
                                    @input-change="(newValue) => question.option_b = newValue" />
                                </div>
                            </li>
                        </div>
                        <div v-if="question.option_c || question.option_d || question.editable">
                            <li>
                                <div>C. </div>
                                <div>
                                    <DisabledInput :text="question.option_c"
                                    :editable="question.editable"
                                    @input-change="(newValue) => question.option_c = newValue" />
                                </div>
                            </li>
                            <li>
                                <div>D. </div>
                                <div>
                                    <DisabledInput :text="question.option_d"
                                    :editable="question.editable"
                                    @input-change="(newValue) => question.option_d = newValue" />
                                </div>
                            </li>
                        </div>
                    </ul>

                    <!-- correct option -->
                    <p>
                        Correct Option:
                        <span class="text-success">
                            <DisabledInput :text="question.correct_option.toUpperCase()"
                            :editable="question.editable"
                            @input-change="(newValue) => question.correct_option = newValue" />
                        </span>
                    </p>

                    <!-- score -->
                    <p>
                        Score:
                        <span class="text-secondary">
                            <DisabledInput :text="question.score"
                            :editable="question.editable"
                            @input-change="(newValue) => question.score = newValue" />
                        </span>
                    </p>
                </div>
            </div>
        </Card>
        <div class="modal fade" id="modal" tabindex="-1" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable">
                <div class="modal-content">
                    <div class="modal-header">
                        <h1 class="modal-title fs-5" id="exampleModalLabel">Add Question</h1>
                        <button ref="modalCloseBtnElem" type="button" class="btn-close"
                        data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <form ref="formElem" id="add-question" @submit.prevent="addData">
                            <!-- question -->
                            <div class="mb-3">
                                <label class="form-label" for="question">Question*</label>
                                <input name="question" type="text" class="form-control"
                                :placeholder="state.questions[0]?.question" id="question" required>
                            </div>
                            <!-- options -->
                            <div class="mb-3">
                                <label class="form-label" for="option_a">Option A*</label>
                                <input name="option_a" type="text" class="form-control"
                                :placeholder="state.questions[0]?.option_a"
                                id="option_a" required>
                            </div>
                            <div class="mb-3">
                                <label class="form-label" for="option_b">Option B*</label>
                                <input name="option_b" type="text" class="form-control"
                                :placeholder="state.questions[0]?.option_b"
                                id="option_b" required>
                            </div>
                            <div class="mb-3">
                                <label class="form-label" for="option_c">Option C</label>
                                <input name="option_c" type="text" class="form-control"
                                :placeholder="state.questions[0]?.option_c"
                                id="option_c">
                            </div>
                            <div class="mb-3">
                                <label class="form-label" for="option_d">Option D</label>
                                <input name="option_d" type="text" class="form-control"
                                :placeholder="state.questions[0]?.option_d"
                                id="option_d">
                            </div>
                            <!-- correct option -->
                            <div class="mb-3">
                                <span class="me-4">Correct Option*</span>
                                <div class="form-check form-check-inline">
                                    <input class="form-check-input" type="radio" required
                                    name="correct_option" id="correct_option_a"
                                    value="a">
                                    <label class="form-check-label" for="correct_option_a">A</label>
                                </div>
                                <div class="form-check form-check-inline">
                                    <input class="form-check-input" type="radio" required
                                    name="correct_option" id="correct_option_b"
                                    value="b">
                                    <label class="form-check-label" for="correct_option_b">B</label>
                                </div>
                                <div class="form-check form-check-inline">
                                    <input class="form-check-input" type="radio" required
                                    name="correct_option" id="correct_option_c"
                                    value="c">
                                    <label class="form-check-label" for="correct_option_c">C</label>
                                </div>
                                <div class="form-check form-check-inline">
                                    <input class="form-check-input" type="radio" required
                                    name="correct_option" id="correct_option_d"
                                    value="d">
                                    <label class="form-check-label" for="correct_option_d">D</label>
                                </div>
                            </div>
                            <!-- score -->
                            <div class="mb-3">
                                <label class="form-label" for="score">Score*</label>
                                <input name="score" type="number" class="form-control"
                                :placeholder="state.questions[0]?.score"
                                id="score" required>
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                        <button type="submit" form="add-question" class="btn btn-success">
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
ul {
    list-style: none;
    border: 1px solid gray;
    border-radius: 6px;
    padding: 0;
    margin-top: 14px;
}

ul > div {
    display: flex;
    align-items: center;
}
ul > div:first-child {
    border-bottom: 1px solid gray;
}
li {
    padding: 6px 12px;
    width: 50%;
    display: flex;
}
li > div:first-child {
    margin-right: 8px;
}
ul > div > li:first-child {
    border-right: 1px solid gray;
}
</style>