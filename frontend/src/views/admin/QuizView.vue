<script setup>
import Card from '@/components/Card.vue';
import { api } from '@/utils/auth';
import { onMounted, reactive, nextTick } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();

const state = reactive({
    subject: {},
    quiz: {
        id: '',
    },
    chapters: [],
    questions: {},
});

const saveChanges = async () => {
    const questionIds = Object.keys(state.questions).filter((key) => state.questions[key] === true);
    const dataToSend = {
        quiz_id: state.quiz.id,
        question_ids: questionIds,
    }
    try {
        const response = await api.post('/quiz-questions', dataToSend);
        window.showToast("Questions Updated Successfully", 'success', response.data.info);
    } catch (error) {
        console.log(error.response?.data || error);
        window.showToast("Can't Update Questions", 'danger', error.response.data);
    }
};

const toggleQuestion = (event) => {
    state.questions[event.target.value] = event.target.checked;
};

const addRowClickability = () => {
    const rows = document.querySelectorAll('.clickable-row');
    for (const row of rows) {
        row.addEventListener('click', (event) => {
            if (event.target.classList.contains('form-check-input')) {
                return;
            }

            const checkbox = row.querySelector('.form-check-input');
            checkbox.click();
        });
    }
};

onMounted(async () => {
    // retrieve quiz id
    const pathSplit = route.path.split('/');
    state.quiz.id = pathSplit[pathSplit.length - 1];

    let response
    // fetch quiz
    try {
        response = await api.get(`/quiz/${state.quiz.id}`);
        state.quiz = response.data.data;
    } catch (error) {
        console.log(error.response?.data || error);
    }

    // fetch subject and chapters
    try {
        if (state.quiz.scope === 'subject') {
            // if scope subject
            response = await api.get(`/subject/${state.quiz.subject_id}`);
            state.subject = response.data.data;
            
            response = await api.get(`/chapters?subject_id=${state.subject.id}`);
            state.chapters = response.data.data;
        } else {
            // if scope chapter
            response = await api.get(`/chapter/${state.quiz.chapter_id}`);
            state.chapters.push(response.data.data);

            response = await api.get(`/subject/${state.chapters[0].subject_id}`);
            state.subject = response.data.data;
        }
    } catch (error) {
        console.log(error.response?.data || error);
    }

    // fetch questions
    for (const chapter of state.chapters) {
        response = await api.get(`/questions?chapter_id=${chapter.id}`);
        chapter.questions = response.data.data;
    }

    // prepare questions data structure
    for (const chapter of state.chapters) {
        for (const question of chapter.questions) {
            state.questions[question.id] = false;
        }
    }

    // fetch quiz questions
    response = await api.get(`/quiz-questions?quiz_id=${state.quiz.id}`);
    response.data.data.forEach((question) => {
        state.questions[question.question_id] = true;
    });

    await nextTick();
    addRowClickability();
});
</script>

<template>
    <main class="container">
        <h1 v-if="state.quiz.scope === 'subject'"
        class="display-3 text-center me-5">{{ state.subject.name }}</h1>
        <Card v-for="(chapter, chapterIndex) in state.chapters" :key="chapterIndex"
        :heading="chapter.name" :subheading="state.quiz.scope === 'chapter' ? state.subject.name : ''">
            
            <table class="table table-hover align-middle">
                <!-- table head -->
                <thead>
                    <tr>
                        <th scope="col">#</th>
                        <th scope="col">Question</th>
                        <th scope="col">Select</th>
                    </tr>
                </thead>

                <!-- table body -->
                <tbody class="table-group-divider">
                    <tr v-for="(question, questionIndex) in chapter.questions"
                    :key="questionIndex" class="clickable-row">
                        <th scope="row">{{ questionIndex + 1 }}</th>
                        <td>{{ question.question }}</td>
                        <td>
                            <input class="form-check-input" type="checkbox"
                            :value="question.id" :checked="state.questions[question.id]"
                            @change="toggleQuestion">
                        </td>
                    </tr>

                    <!-- no chapters placeholder -->
                    <tr>
                        <td v-if="!chapter.questions?.length" colspan="4" class="text-center lead">
                            No Chapters Available
                        </td>
                    </tr>
                </tbody>
            </table>
        </Card>
        <h2 v-if="!state.chapters.length" class="text-center lead">No Chapters Available</h2>
    </main>
    <button @click="saveChanges" class="btn btn-success" id="save-btn"
    v-if="Object.keys(state.questions).length">
        Save Changes
    </button>
</template>

<style scoped>
.clickable-row {
    cursor: pointer;
}

#save-btn {
    position: fixed;
    bottom: 32px;
    right: 64px;
    z-index: 5;
}
</style>