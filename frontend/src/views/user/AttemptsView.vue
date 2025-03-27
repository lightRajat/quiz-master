<script setup>
import Card from '@/components/Card.vue';
import { api, getCurrentUser } from '@/utils/auth';
import { onMounted, reactive } from 'vue';
import { RouterLink } from 'vue-router';

const state = reactive({
    attempts: [],
});

const updateScopeNames = async () => {
    try {
        for (const attempt of state.attempts) {
            // fetch quiz details
            let response = await api.get(`/quiz/${attempt.quiz_id}`);
            attempt.scope = response.data.data.scope;
            attempt.chapter_id = response.data.data.chapter_id;
            attempt.subject_id = response.data.data.subject_id;

            // fetch subject / chapter names
            if (attempt.scope === 'chapter') {
                response = await api.get(`/chapter/${attempt.chapter_id}`)
                attempt.chapter_name = response.data.data.name;
                attempt.subject_id = response.data.data.subject_id;
            }
            response = await api.get(`/subject/${attempt.subject_id}`)
            attempt.subject_name = response.data.data.name;
        }
    } catch (error) {
        console.error(error.response?.data || error);
    }
};

onMounted(async () => {
    try {
        // fetch attempts data
        const response = await api.get(`/attempts?user_id=${getCurrentUser()}`);
        state.attempts = response.data.data.reverse();

        updateScopeNames();
    } catch (error) {
        console.error(error.response?.data || error);
    }
});
</script>

<template>
    <div class="m-5">
        <Card heading="Your Quiz Attempts">
            <table class="table table-striped table-hover align-middle">
                <!-- table head -->
                <thead>
                    <tr>
                        <th scope="col">#</th>
                        <th scope="col">Scope</th>
                        <th scope="col">
                            <span class="score">Score</span>
                            /<span class="total-score">Total</span>
                        </th>
                        <th scope="col">Date Attempted</th>
                        <th scope="col">Action</th>
                    </tr>
                </thead>

                <!-- table body  -->
                <tbody class="table-group-divider">
                    <tr v-for="(attempt, index) in state.attempts" :key="index">
                        <th scope="row">{{ index + 1 }}</th>

                        <!-- scopes -->
                        <td>
                            <h6 v-if="attempt.scope === 'chapter'" class="text-secondary">
                                {{ attempt.subject_name }}
                            </h6>
                            <h5>
                                {{ attempt.scope === 'chapter' ? attempt.chapter_name : attempt.subject_name }}
                            </h5>
                        </td>

                        <!-- scores -->
                        <td>
                            <span class="score">{{ attempt.score }}</span>
                            /<span class="total-score">{{ attempt.total_score }}</span>
                        </td>
                        <td>{{ attempt.date_attempted }}</td>
                        <td class="d-flex">
                            <RouterLink :to="`/user/${getCurrentUser()}/attempt/${attempt.id}`"
                            class="btn btn-primary d-flex me-3"
                            style="width: fit-content;">
                                <i class="bi bi-eye me-1"></i>
                                View Attempt
                            </RouterLink>
                        </td>
                    </tr>
                    <tr v-if="!state.attempts.length">
                        <td colspan="5" class="text-center lead">No Data Available</td>
                    </tr>
                </tbody>
            </table>
        </Card>
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
.total-score {
    font-size: 12px;
}
.score {
    font-size: 22px;
}
</style>