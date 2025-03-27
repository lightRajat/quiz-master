<script setup>
import Card from '@/components/Card.vue';
import { api } from '@/utils/auth';
import { onMounted, reactive } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();

const state = reactive({
    attempt: {},
    quiz: {},
    questions: [],
});

onMounted(async () => {
    // retrieve attempt id
    const pathSplit = route.path.split('/');
    state.attempt.id = pathSplit[pathSplit.length - 1];
    
    try {
        // fetch attempt
        let response = await api.get(`/attempt/${state.attempt.id}`);
        state.attempt = response.data.data;
        
        // fetch quiz
        response = await api.get(`/quiz/${state.attempt.quiz_id}`);
        state.quiz = response.data.data;
        
        // fetch scope names
        if (state.quiz.scope === 'chapter') {
            response = await api.get(`/chapter/${state.quiz.chapter_id}`);
            state.quiz.chapter_name = response.data.data.name;
            state.quiz.subject_id = response.data.data.subject_id;
        }
        response = await api.get(`/subject/${state.quiz.subject_id}`);
        state.quiz.subject_name = response.data.data.name;

        // fetch questions
        response = await api.get(`/attempt-questions?attempt_id=${state.attempt.id}`);
        state.questions = response.data.data;
        
        for (const question of state.questions) {
            response = await api.get(`/question/${question.question_id}`);
            question.question = response.data.data.question;
            question.score = response.data.data.score;
        }

    } catch (error) {
        console.log(error.response?.data || error);
    }
});
</script>

<template>
    <div class="m-3">
        <Card :heading="state.quiz.scope === 'chapter' ? state.quiz.chapter_name : state.quiz.subject_name"
        :subheading="state.quiz.scope === 'chapter' ? state.quiz.subject_name : ''">

            <!-- attempt stats -->
            <div class="card stats">

                <!-- time -->
                <div class="stat">
                    <div>Time: </div>
                    <div>
                        <span>{{ state.attempt.time_taken }}</span>
                        /<span class="stat-total">{{ state.attempt.total_time }}</span> mins
                    </div>
                </div>

                <!-- score -->
                <div class="stat">
                    <div>Score: </div>
                    <div>
                        <span>{{ state.attempt.score }}</span>
                        /<span class="stat-total">{{ state.attempt.total_score }}</span> pts
                    </div>
                </div>

                <!-- date attempted -->
                 <div class="stat">
                    <div>Attempted on:</div>
                    <div>{{ state.attempt.date_attempted }}</div>
                 </div>

            </div>

            <div v-for="(question, index) in state.questions" :key="index"
            class="card m-5">
                <div class="card-body">

                    <!-- question and score -->
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <div class="fs-5">
                            <span class="me-2">{{ index + 1 }}.</span>
                            <span>{{ question.question }}</span>
                        </div>

                        <div class="text-secondary">{{ question.score }} marks</div>
                    </div>

                    <!-- correct answer -->
                    <div class="mb-1">
                        <span class="me-2">Correct Answer:</span>
                        <span class="text-success">{{ question.correct_answer }}</span>
                    </div>

                    <!-- selected answer -->
                    <div class="mb-3">
                        <span class="me-2">Selected Answer:</span>
                        <span :class="question.correct_answer == question.selected_answer ? 'text-success' : 'text-danger'">
                            {{ question.selected_answer || 'Left Blank' }}
                        </span>
                    </div>

                </div>
            </div>
        </Card>
    </div>
</template>

<style scoped>
.stats {
    position: absolute;
    top: 12px;
    left: 64px;
    display: inline-block;
    padding: 12px 8px;
    font-size: large;
    width: 300px;
}
.stat {
    display: flex;
    justify-content: space-around;
}
.stat-total {
    font-size: 12px;
}
</style>