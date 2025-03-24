<script setup>
import { onMounted, reactive } from 'vue';
import { api } from '@/utils/auth';
import { RouterLink } from 'vue-router';

import Card from '@/components/Card.vue';

const state = reactive({
    subjects: [],
    quizzes: []
});
const limit = 5;

onMounted(async () => {
    try {
        // fetch subjects
        let response = await api.get('/subjects');
        state.subjects = response.data.data;

        // fetch quizzes
        response = await api.get('/quizzes');
        const quizzes = response.data.data;

        for (const quiz of quizzes) {
            if (quiz.scope === 'subject') {
                response = await api.get(`/subject/${quiz.subject_id}`);
            } else {
                response = await api.get(`/chapter/${quiz.chapter_id}`);
            }
            quiz.scope_name = response.data.data.name;
        }
        state.quizzes = quizzes;
    } catch (error) {
        console.error(error);
    }
});
</script>

<template>
    <div class="row m-2">
        <div class="col">
            <Card heading="Subjects">
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
                        <tr v-for="(row, rowIndex) in state.subjects.slice(0, state.subjects.length < limit ? state.subjects.length : limit)" :key="rowIndex">
                            <th scope="row">{{ rowIndex + 1 }}</th>
                            <td>{{ row.name }}</td>
                            <td>{{ row.description || "--- No Description ---" }}</td>
                            <td>
                                <RouterLink to="#" class="btn btn-outline-secondary d-flex" style="width: fit-content;">
                                    <i class="bi bi-info"></i> View
                                </RouterLink>
                            </td>
                        </tr>
                        <tr v-if="state.subjects.length === 0">
                            <td colspan="4" class="text-center lead">No Data Available</td>
                        </tr>
                        <tr>
                            <td colspan="4">
                                <RouterLink to="/admin/subjects" class="btn btn-primary d-flex mx-auto" style="width: fit-content;">
                                    <i class="bi bi-journal me-2"></i> Show All Subjects
                                </RouterLink>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </Card>
        </div>
        <div class="col">
            <Card heading="Quizzes">
                <table class="table table-striped table-hover align-middle">
                    <thead>
                        <tr>
                            <th scope="col">#</th>
                            <th scope="col">Scope</th>
                            <th scope="col">Time</th>
                            <th scope="col">Action</th>
                        </tr>
                    </thead>
                    <tbody class="table-group-divider">
                        <tr v-for="(row, rowIndex) in state.quizzes.slice(0, state.subjects.length < limit ? state.subjects.length : limit)" :key="rowIndex">
                            <th scope="row">{{ rowIndex + 1 }}</th>
                            <td>{{ row.scope_name }}</td>
                            <td>{{ row.time }} m</td>
                            <td>
                                <RouterLink to="#" class="btn btn-outline-secondary d-flex" style="width: fit-content;">
                                    <i class="bi bi-info"></i> View
                                </RouterLink>
                            </td>
                        </tr>
                        <tr v-if="state.quizzes.length === 0">
                            <td colspan="4" class="text-center lead">No Data Available</td>
                        </tr>
                        <tr>
                            <td colspan="4">
                                <RouterLink to="/admin/quizzes" class="btn btn-primary d-flex mx-auto" style="width: fit-content;">
                                    <i class="bi bi-card-checklist me-2"></i> Show All Quizzes
                                </RouterLink>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </Card>
        </div>
    </div>
</template>