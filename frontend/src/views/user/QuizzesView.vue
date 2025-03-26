<script setup>
import Card from '@/components/Card.vue';
import { reactive, onMounted, watch } from 'vue';
import { api, getCurrentUser } from '@/utils/auth';
import { RouterLink } from 'vue-router';

const state = reactive({
    quizzes: [],
    subjects: [],
    chapters: [],
    chaptersInFilter: [],
    quizDisplay: null,
    isQuizDisplayEmpty: false,
});

const filter = reactive({
    subject_id: '',
    chapter_id: '',
    quizType: 'subject',
});

// filter quizzes
watch(filter, () => {
    if (!state.quizDisplay) {
        return;
    }

    const quizDisplay = {};
    state.quizzes.forEach((quiz) => {
        let visible = false;

        // quiz type subject
        if (filter.quizType === 'subject') {
            filter.chapter_id = ''; // resetting chapter filter

            // subject selected
            if (filter.subject_id) {
                visible = quiz.scope === 'subject' && quiz.subject_id == filter.subject_id;
            } else {
                visible = quiz.scope === 'subject'
            }
        } else {
            // subject selected
            if (filter.subject_id) {
                // chapter selected
                if (filter.chapter_id) {
                    visible = quiz.scope === 'chapter' && quiz.chapter_id == filter.chapter_id;
                } else {
                    visible = quiz.scope === 'chapter' && quiz.subject_id == filter.subject_id;
                }
            } else {
                filter.chapter_id = ''; // resetting chapter filter
                visible = quiz.scope === 'chapter'
            }
        }

        quizDisplay[quiz.id] = visible;
    });

    state.quizDisplay = quizDisplay;

    // check if no items to display
    state.isQuizDisplayEmpty = !Object.values(state.quizDisplay).some(Boolean);
}, {deep: true});

const resetFilter = () => {
    filter.subject_id = '';
    filter.chapter_id = '';
    filter.quizType = 'subject';
};

const updateScopeNames = () => {
    state.quizzes.forEach((quiz) => {
        let chapter;
        if (quiz.scope === 'chapter') {
            chapter = state.chapters.find((chapter) => chapter.id == quiz.chapter_id);
            quiz.chapter_name = chapter.name;
            quiz.subject_id = chapter.subject_id;
        }

        const subject = state.subjects.find((subject) => subject.id == quiz.subject_id);
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
        updateScopeNames();

        // set quiz display
        const quizDisplay = {};
        state.quizzes.forEach((quiz) => quizDisplay[quiz.id] = quiz.scope === 'subject');
        state.quizDisplay = quizDisplay;
    } catch (error) {
        console.log(error.response?.data || error);
    }
});
</script>

<template>
    <main class="container mt-5">
        <!-- filter -->
        <div>
            <h3 class="text-center">Filter</h3>
            <div class="d-flex my-4 mx-auto justify-content-evenly align-items-center">
                <!-- quiz type -->
                <div class="d-flex align-items-center">
                    <label class="lead me-2">Quiz Type:</label>
                    <div class="btn-group" role="group">
                        <input type="radio" class="btn-check" id="btncheck1" v-model="filter.quizType"
                        checked value="subject">
                        <label class="btn btn-outline-primary" for="btncheck1">Subject</label>

                        <input type="radio" class="btn-check" id="btncheck2" v-model="filter.quizType"
                        value="chapter">
                        <label class="btn btn-outline-primary" for="btncheck2">Chapter</label>
                    </div>
                </div>

                <!-- subject -->
                <div class="d-flex align-items-center">
                    <label for="subject" class="lead me-3">Subject:</label>
                    <select class="form-select" id="subject" name="subject"
                    v-model="filter.subject_id">
                        <option value="" selected>All Subjects</option>
                        <option v-for="(row, index) in state.subjects" :key="index"
                        :value="row.id">
                            {{ row.name }}
                        </option>
                    </select>
                </div>

                <!-- chapter -->
                <div class="d-flex align-items-center">
                    <label for="chapter" class="lead me-3">Chapter:</label>
                    <select class="form-select" id="chapter" name="chapter"
                    :disabled="filter.quizType === 'subject' || !filter.subject_id" v-model="filter.chapter_id">
                        <option value="" selected>All Chapters</option>
                        <option v-for="(row, index) in state.chapters.filter((item) => item.subject_id === filter.subject_id)"
                        :key="index" :value="row.id">
                            {{ row.name }}
                        </option>
                    </select>
                </div>
                <button type="reset" class="btn btn-outline-secondary" @click="resetFilter">
                    Clear Filter
                </button>
            </div>
        </div>

        <Card heading="Quizzes">
            <table class="table table-hover align-middle">
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
                    <tr v-for="(row, index) in state.quizzes" :key="index"
                    v-show="state.quizDisplay[row.id]">
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
                            {{ row.time }} mins
                        </td>

                        <!-- description -->
                        <td>
                            {{ row.description }}
                        </td>

                        <!-- actions -->
                        <td class="d-flex">
                            <RouterLink :to="`/user/${getCurrentUser()}/quiz/${row.id}/take`"
                            class="btn btn-primary d-flex me-3 my-1 action-link"
                            style="width: fit-content;">
                                <i class="bi bi-pencil-square me-2"></i>
                                Attempt Quiz
                            </RouterLink>
                        </td>
                    </tr>
                    <tr v-show="state.isQuizDisplayEmpty">
                        <td colspan="5" class="text-center lead">No Quizzes Available for this Filter</td>
                    </tr>
                </tbody>
            </table>
        </Card>
    </main>
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

.action-link {
    opacity: 0.85;
    transition: all 0.2s ease-out;
}
.action-link:hover {
    opacity: 1;
    transition: none;
}
</style>