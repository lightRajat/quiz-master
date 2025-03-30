<script setup>
import Card from '@/components/Card.vue';
import { api } from '@/utils/auth';
import { onMounted, reactive } from 'vue';

const state = reactive({
    attempts: [],
    users: {},
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

            // fetch user details
            response = await api.get(`/user/${attempt.user_id}`);
            attempt.username = response.data.data.username;
        }
    } catch (error) {
        console.error(error.response?.data || error);
    }
};

const downloadData = () => {
    // prepare the csv
    const csvContents = ['username,quiz_scope,subject_name,chapter_name,date_attempted,total_time,time_taken,total_score,score_obtained'];
    for (const attempt of state.attempts) {
        const row = `${attempt.username},${attempt.scope},${attempt.subject_name},${attempt.chapter_name || ''},${attempt.date_attempted},${attempt.total_time},${attempt.time_taken},${attempt.total_score},${attempt.score}`;
        csvContents.push(row);
    }
    const csvString = csvContents.join('\n');
    
    // creating blob and url
    const csvBlob = new Blob([csvString], {type: 'text/csv'});
    const csvUrl = URL.createObjectURL(csvBlob);

    // making download through anchor tag
    const anchorElem = document.createElement('a');
    anchorElem.href = csvUrl;
    anchorElem.download = 'userAttemptsData.csv';
    anchorElem.style.display = 'none';
    document.body.appendChild(anchorElem);
    anchorElem.click();

    // cleanup
    document.body.removeChild(anchorElem);
    URL.revokeObjectURL(csvUrl);
};

onMounted(async () => {
    try {
        // fetch attempts data
        const response = await api.get('/attempts');
        state.attempts = response.data.data.reverse();

        updateScopeNames();
    } catch (error) {
        console.error(error.response?.data || error);
    }
});
</script>

<template>
    <div class="m-5">
        <Card heading="Quiz Attempts by Users">

            <!-- download button -->
            <button @click="downloadData" class="btn btn-primary download-btn"
            :disabled="!state.attempts.length">
                <i class="bi bi-download me-1"></i>
                Download Data as CSV
            </button>

            <!-- table -->
            <table class="table table-striped table-hover align-middle">
                <thead>
                    <tr>
                        <th scope="col">#</th>
                        <th scope="col">User</th>
                        <th scope="col">Scope</th>
                        <th scope="col">Date Attempted</th>
                        <th scope="col">Score</th>
                        <th scope="col">Time</th>
                    </tr>
                </thead>
                <tbody class="table-group-divider">
                    <tr v-for="(attempt, index) in state.attempts" :key="index">
                        <th scope="row">{{ index + 1 }}</th>

                        <!-- username -->
                        <td>{{ attempt.username }}</td>

                        <!-- scope -->
                        <td>
                            <h6 v-if="attempt.scope === 'chapter'" class="text-secondary">
                                {{ attempt.subject_name }}
                            </h6>
                            <h5>
                                {{ attempt.scope === 'chapter' ? attempt.chapter_name : attempt.subject_name }}
                            </h5>
                        </td>

                        <!-- date -->
                        <td>{{ attempt.date_attempted }}</td>

                        <!-- score -->
                        <td>
                            <span class="score">{{ attempt.score }}</span>
                            /<span class="total-score">{{ attempt.total_score }}</span> pts
                        </td>

                        <!-- time -->
                        <td>
                            <span class="score">{{ attempt.time_taken }}</span>
                            /<span class="total-score">{{ attempt.total_time }}</span> mins
                        </td>
                    </tr>

                    <!-- unavailable data info -->
                    <tr v-if="!state.attempts.length">
                        <td colspan="6" class="text-center">No Data Available</td>
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
.download-btn {
    position: absolute;
    top: 28px;
    left: 50px;
}
</style>