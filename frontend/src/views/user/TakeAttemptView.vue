<script setup>
import { api, getCurrentUser } from '@/utils/auth';
import { onMounted, reactive, computed } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();

const state = reactive({
    quiz: {},
    questions: [],
    selected_options: {},
    countDown: 3,
    timeLeft: null,
    quizStarted: false,
    quizEnded: false,
    timerId: null,
    startDisplayingQuestions: false,
    attempt: {},
});

const minLeft = computed(() => {
    return parseInt(state.timeLeft / 60).toString().padStart(2, '0');
});
const secLeft = computed(() => {
    return parseInt(state.timeLeft % 60).toString().padStart(2, '0');
});

const clearOption = (question_id) => {
    state.selected_options[question_id] = '';
};

const endQuiz = async () => {
    clearInterval(state.timerId);
    state.quizEnded = true;
    
    // prepare data to send to Attempt
    let score = 0;
    let totalScore = 0;
    state.questions.forEach((question) => {
        totalScore += question.score;
        if (state.selected_options[question.id] == question.correct_option) {
            score += question.score;
        }
    });

    const attemptData = new FormData();
    attemptData.set('user_id', getCurrentUser());
    attemptData.set('quiz_id', state.quiz.id);
    attemptData.set('total_time', state.quiz.time);
    attemptData.set('time_taken', state.quiz.time - parseInt(state.timeLeft / 60));
    attemptData.set('total_score', totalScore);
    attemptData.set('score', score);

    // send attempt data to server
    try {
        const response = await api.post('/attempts', attemptData);
        state.attempt = response.data.data;
        window.showToast("Quiz Completed", 'primary');
    } catch (error) {
        console.log(error.response?.data || error);
    }

    // prepare AttemptQuestion data
    const attemptQuestionsData = {
        attempt_id: state.attempt.id,
        questions: [],
    }
    state.questions.forEach((question) => {
        const correctAnswer = question[`option_${question.correct_option}`] || '';
        const selectedAnswer = question[`option_${state.selected_options[question.id]}`] || '';

        attemptQuestionsData.questions.push({
            'question_id': question.id,
            'selected_answer': selectedAnswer,
            'correct_answer': correctAnswer,
        });
    });
    console.log(attemptQuestionsData)
    
    // send AttemptQuestion data to server
    try {
        const response = await api.post('/attempt-questions', attemptQuestionsData);
        console.log(response.data);
    } catch (error) {
        console.log(error.response?.data || error);
    }
};

onMounted(async () => {
    try {
        // fetch quiz id
        const pathSplit = route.path.split('/');
        state.quiz.id = pathSplit[pathSplit.length - 2];
        
        // fetch quiz details - scopes
    
        let response = await api.get(`/quiz/${state.quiz.id}`);
        state.quiz =  response.data.data;
        
        if (state.quiz.scope === 'chapter') {
            response = await api.get(`/chapter/${state.quiz.chapter_id}`);
            state.quiz.chapter_name = response.data.data.name;
            state.quiz.subject_id = response.data.data.subject_id;
        }
        response = await api.get(`/subject/${state.quiz.subject_id}`);
        state.quiz.subject_name = response.data.data.name;
        
        // fetch question ids of quiz
        response = await api.get(`/quiz-questions?quiz_id=${state.quiz.id}`);
        state.questions = response.data.data;
        
        // fetch question details
        for (let i = 0; i < state.questions.length; i++) {
            const questionId = state.questions[i].question_id;
            response = await api.get(`/question/${questionId}`);
            state.questions[i] = response.data.data;
            
            // add selected_options data
            state.selected_options[state.questions[i].id] = 'b';
        }

    } catch (error) {
        console.log(error.response?.data || error);
    }

    // set quiz timeLeft
    state.timeLeft = state.quiz.time * 60;

    // start countdown timer
    state.startDisplayingQuestions = true;
    state.timerId = setInterval(() => {
        state.countDown -= 1;

        if (state.countDown <= 0) {
            clearInterval(state.timerId);
            state.quizStarted = true;
            state.timerId = setInterval(() => {
                state.timeLeft -= 1;

                if (state.timeLeft <= 0) {
                    endQuiz();
                }
            }, 1000);
        }
    }, 1000);
});
</script>

<template>
    <main class="container mt-4">
        <!-- heading -->
        <div class="mb-5">
            <h2 v-if="state.quiz.scope === 'chapter'" class="lead mb-0 ms-1">
                {{ state.quiz.subject_name }}
            </h2>
            <h1 class="display-5">
                {{ state.quiz.scope === 'chapter' ? state.quiz.chapter_name : state.quiz.subject_name }}
            </h1>
        </div>

        <!-- questions -->
        <div v-for="(question, index) in state.questions" :key="index" class="card mb-5 question"
        :class="state.startDisplayingQuestions ? 'question-visible' : ''"
        :style="`transition: ${state.countDown + 1}s;`">
            <div class="card-body p-4">
                <!-- question -->
                <p class="h5 mb-3 d-flex justify-content-between">
                    <div>
                        <span class="me-3">{{ index + 1 }}.</span>
                        <span>{{ question.question }}</span>
                    </div>

                    <!-- marks -->
                     <div class="text-secondary me-2 fs-6">{{ question.score }} marks</div>
                </p>
                
                <!-- options -->
                <div class="option-grp container mb-2">
                    <div class="row">
                        <input class="col" type="radio" :id="`q_${question.id}_option_a`" :name="`q_${question.id}`"
                        value="a" v-model="state.selected_options[question.id]"
                        :disabled="!state.quizStarted || state.quizEnded">
                        <label :for="`q_${question.id}_option_a`" class="radio-label col radio-label-a">
                            <span class="me-2">A.</span>
                            <span>{{ question.option_a }}</span>
                        </label>

                        <input class="col" type="radio" :id="`q_${question.id}_option_b`" :name="`q_${question.id}`"
                        value="b" v-model="state.selected_options[question.id]"
                        :disabled="!state.quizStarted || state.quizEnded">
                        <label :for="`q_${question.id}_option_b`" class="radio-label col radio-label-b">
                            <span class="me-2">B.</span>
                            <span>{{ question.option_b }}</span>
                        </label>
                    </div>
                    <div class="row" v-if="question.option_c">
                        <input class="col" type="radio" :id="`q_${question.id}_option_c`" :name="`q_${question.id}`"
                        value="c" v-model="state.selected_options[question.id]"
                        :disabled="!state.quizStarted || state.quizEnded">
                        <label :for="`q_${question.id}_option_c`" class="radio-label col radio-label-c">
                            <span class="me-2">C.</span>
                            <span>{{ question.option_c }}</span>
                        </label>

                        <input class="col" type="radio" :id="`q_${question.id}_option_d`" :name="`q_${question.id}`"
                        value="d" v-model="state.selected_options[question.id]"
                        :disabled="!state.quizStarted || state.quizEnded">
                        <label :for="`q_${question.id}_option_d`" class="radio-label col radio-label-d">
                            <span class="me-2">D.</span>
                            <span>{{ question.option_d }}</span>
                        </label>
                    </div>
                </div>

                <!-- clear option btn -->
                <button class="text-secondary link-underline-secondary clear-btn"
                @click="clearOption(question.id)" :disabled="state.quizEnded"
                :class="{'clear-btn-ended': state.quizEnded}">
                    Clear Option
                </button>
            </div>
        </div>
    </main>

    <!-- menu -->
    <div class="menu bg-success-subtle" :class="{'menu-later': state.quizStarted}">
        <p class="timer" :class="state.quizStarted ? 'timer-hidden' : ''">will start in {{ state.countDown }} seconds</p>
        <p class="fs-4 mb-2">{{ minLeft }}:{{ secLeft }}</p>
        <button class="btn btn-success" :disabled="!state.quizStarted || state.quizEnded"
        @click="endQuiz">
            Sumbit
        </button>
    </div>
</template>

<style scoped>
.question {
    opacity: 0;
}
.question-visible {
    opacity: 1;
}

.timer {
    max-height: 100px;
    overflow: hidden;
    transition: 0.5s;
}
.timer.timer-hidden {
    max-height: 0;
    margin: 0;
}
.menu {
    position: fixed;
    top: 26px;
    right: 32px;
    padding: 10px;
    border-radius: 8px;
    text-align: center;
    width: 200px;
    transition: 0.5s;
}
.menu-later {
    opacity: 0.4;
}
.menu:hover {
    opacity: 1;
}

input[type="radio"] {
    display: none;
}

.radio-label {
    padding: 10px 20px;
    background-color: white;
    cursor: pointer;
    font-size: 16px;
    transition: 0.35s;
}
.radio-label:hover {
    background-color: #f0f0f0;
}

input[type="radio"]:checked + .radio-label {
    background-color: #198754;
    color: white;
}

.option-grp {
    outline: 1px solid gray;
    border-radius: 6px;
}
.option-grp > .row:first-child {
    border-bottom: 1px solid gray !important;
}
.radio-label-a, .radio-label-c {
    border-right: 1px solid gray !important;
}

.radio-label-a {
    border-top-left-radius: 6px;
}
.radio-label-b {
    border-top-right-radius: 6px;
}
.radio-label-c {
    border-bottom-left-radius: 6px;
}
.radio-label-d {
    border-bottom-right-radius: 6px;
}
.clear-btn {
    background: none;
    outline: none;
    border: none;
}
.clear-btn:hover {
    text-decoration: underline;
    display: inline-block;
    cursor: pointer;
}
.clear-btn-ended.clear-btn:hover {
    text-decoration: none;
    cursor: default;
}
</style>