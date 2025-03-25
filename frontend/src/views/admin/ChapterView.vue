<script setup>
import Card from '@/components/Card.vue';
import { onMounted, reactive } from 'vue';
import { api } from '@/utils/auth';
import { useRoute } from 'vue-router';
import DisabledInput from '@/components/DisabledInput.vue';
import EditButton from '@/components/EditButton.vue';

const route = useRoute();

const state = reactive({
    questions: [],
    chapter: {name: '', id: ''},
});

const btnData = {
    text: "Add Question",
    func: () => {
        alert("hi");
    }
}

const editData = async (id) => {
    const question = state.questions.find((item) => item.id == id);
    question.editable = !question.editable;

    // update data on server
    if (!question.editable) {
        try {
            const { editable: value, ...dataToSend } = question;
            dataToSend.score = Number(dataToSend.score);
            dataToSend.correct_option = dataToSend.correct_option.toLowerCase();
            console.log(dataToSend);
            const response = await api.put(`/question/${id}`, dataToSend);
            console.log(response.data);
            window.showToast("Question Successfully Updated", 'success');
        } catch (error) {
            console.log(error.response?.data || error);
        }
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
                        <p class="h5">
                            <span class="me-3">{{ index + 1 }}.</span>
                            <DisabledInput :text="question.question"
                            :editable="question.editable"
                            @input-change="(newValue) => question.quesion = newValue" />
                        </p>
                        <div class="btn-group" role="group">
                            <EditButton :editable="question.editable"
                            :func="() => editData(question.id)" />

                            <button class="btn btn-outline-danger">
                                <i class="bi bi-trash me-2"></i>
                                Delete
                            </button>
                        </div>
                    </div>
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
                        <div v-if="question.option_c">
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
                    <p>
                        Correct Option:
                        <span class="text-success">
                            <DisabledInput :text="question.correct_option.toUpperCase()"
                            :editable="question.editable"
                            @input-change="(newValue) => question.correct_option = newValue" />
                        </span>
                    </p>
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