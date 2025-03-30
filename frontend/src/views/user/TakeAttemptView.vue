<script setup>
import { api, getCurrentUser } from '@/utils/auth';
import { onMounted, reactive, computed } from 'vue';
import { useRoute, useRouter, RouterLink } from 'vue-router';

const route = useRoute();
const router = useRouter();

const state = reactive({
    quiz: {},
    questions: [],
    selected_options: {},
    timeLeft: null,
    quizStarted: false,
    quizEnded: false,
    timerId: null,
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

const startQuiz = () => {
    state.quizStarted = true;
    state.timerId = setInterval(() => {
        state.timeLeft -= 1;

        if (state.timeLeft <= 0) {
            endQuiz();
        }
    }, 1000);
};

const endQuiz = async () => {
    clearInterval(state.timerId);
    state.quizEnded = true;
    
    // prepare data to send to Attempt
    state.quiz.time_taken = state.quiz.time - parseInt(state.timeLeft / 60);

    state.quiz.score = 0;
    state.questions.forEach((question) => {
        if (state.selected_options[question.id] == question.correct_option) {
            state.quiz.score += question.score;
        }
    });

    // show closing modal
    document.getElementById('modal').click();

    // prepare form
    const attemptData = new FormData();
    attemptData.set('user_id', getCurrentUser());
    attemptData.set('quiz_id', state.quiz.id);
    attemptData.set('total_time', state.quiz.time);
    attemptData.set('time_taken', state.quiz.time_taken);
    attemptData.set('total_score', state.quiz.total_score);
    attemptData.set('score', state.quiz.score);

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
    
    // send AttemptQuestion data to server
    try {
        const response = await api.post('/attempt-questions', attemptQuestionsData);
    } catch (error) {
        console.log(error.response?.data || error);
    }
};

const goBack = () => {
    router.push(`/user/${getCurrentUser()}`);
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
        state.quiz.total_score = 0;
        
        // fetch question ids of quiz
        response = await api.get(`/quiz-questions?quiz_id=${state.quiz.id}`);
        state.questions = response.data.data;
        
        // fetch question details
        for (let i = 0; i < state.questions.length; i++) {
            const questionId = state.questions[i].question_id;
            response = await api.get(`/question/${questionId}`);
            state.questions[i] = response.data.data;
            
            // add selected_options data
            state.selected_options[state.questions[i].id] = '';

            // add score to total score
            state.quiz.total_score += response.data.data.score;
        }

    } catch (error) {
        console.log(error.response?.data || error);
    }

    // show welcome modal
    document.getElementById('modal').click();

    // set quiz timeLeft
    state.timeLeft = state.quiz.time * 60;
});
</script>

<template>
    <!-- modal panel -->

    <!-- button -->
    <button type="button" data-bs-toggle="modal" data-bs-target="#exampleModal"
    id="modal" style="display: none;"></button>
    <!-- Modal -->
    <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true" data-bs-backdrop="static" data-bs-keyboard="false">
    <div class="modal-dialog">
        <div class="modal-content">
            
            <!-- header -->
            <div class="modal-header p-3">

                <!-- welcome title -->
                <div v-if="!state.quizEnded" class="d-flex flex-column">
                    <div v-if="state.quiz.scope === 'chapter'" class="mb-0 modal-subheading text-secondary">
                        {{ state.quiz.subject_name }}
                    </div>
                    <div class="fs-5 modal-heading">
                        {{ state.quiz.scope === 'chapter' ? state.quiz.chapter_name : state.quiz.subject_name }}
                        Quiz
                    </div>
                </div>
                <!-- closing title -->
                <div v-else>
                    <h3>Quiz Ended</h3>
                </div>

                <!-- close button -->
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>

            </div>

            <!-- body  -->
            <div class="modal-body">

                <!-- welcome body -->
                <div v-if="!state.quizEnded">

                    <!-- description -->
                    <h6 class="mb-0">Description:</h6>
                    <p class="mb-1">{{ state.quiz.description }}</p>

                    <!-- time -->
                    <div class="d-flex align-items-center mb-1">
                        <h6 class="mb-0 me-2">Total Time:</h6>
                        <p class="mb-0">{{ state.quiz.time }} mins</p>
                    </div>

                    <!-- score -->
                    <div class="d-flex align-items-center">
                        <h6 class="mb-0 me-2">Total Score:</h6>
                        <p class="mb-0">{{ state.quiz.total_score }} pts</p>
                    </div>

                    <!-- quiz instructions -->
                    <h6 class="mb-0 mt-3">Instructions:</h6>
                    <p>Once you start the quiz, the questions will appear and the
                        timer will start on the upper right corner. The quiz will end
                        when either the time runs out or you click the submit button</p>

                </div>
                <!-- closing body -->
                <div v-else>

                    <!-- score obtained -->
                    <div class="d-flex align-items-center">
                        <h6 class="mb-0 me-2">Score Obtained:</h6>
                        <p class="mb-0">
                            <span class="score">{{ state.quiz.score }}</span>
                            /<span class="total-score">{{ state.quiz.total_score }}</span> pts
                        </p>
                    </div>

                    <!-- time taken -->
                    <div class="d-flex align-items-center mb-2">
                        <h6 class="mb-0 me-2">Time Taken:</h6>
                        <p class="mb-0">
                            <span class="score">{{ state.quiz.time_taken }}</span>
                            /<span class="total-score">{{ state.quiz.time }}</span> mins
                        </p>
                    </div>

                    <!-- instruction -->
                    <p>The quiz has ended. You can now view the correct options
                        to all the questions. Quiz details are also now available
                        on the <em>Past Attempts</em> Page</p>

                </div>

            </div>

            <!-- footer -->
            <div class="modal-footer">

                <!-- welcome footer -->
                <div v-if="!state.quizEnded">

                    <button type="button" class="btn btn-outline-secondary me-3"
                    data-bs-dismiss="modal" @click="goBack">
                        Go Back
                    </button>

                    <button type="button" class="btn btn-primary" @click="startQuiz"
                    data-bs-dismiss="modal">
                        Start Quiz
                    </button>

                </div>
                <!-- closing footer -->
                <div v-else>
                    <button type="button" class="btn btn-primary"
                    data-bs-dismiss="modal">
                        Close
                    </button>
                </div>
                
            </div>

        </div>
    </div>
    </div>

    <!-- page content -->
    <main class="container mt-4">
        <!-- heading -->
        <div class="mb-5 d-flex align-items-end">
            <RouterLink v-if="state.quizEnded" :to="`/user/${getCurrentUser()}`" class="h3 mb-3 me-3"><i class="bi bi-arrow-left-circle me-3"></i></RouterLink>
            <div>
                <h2 v-if="state.quiz.scope === 'chapter'" class="lead mb-0 ms-1">
                    {{ state.quiz.subject_name }}
                </h2>
                <h1 class="display-5">
                    {{ state.quiz.scope === 'chapter' ? state.quiz.chapter_name : state.quiz.subject_name }}
                    Quiz
                </h1>
            </div>
        </div>

        <!-- questions -->
        <div v-for="(question, index) in state.questions" :key="index" class="card mb-5 question"
        :class="state.quizStarted ? 'question-visible' : ''">
            <div class="card-body p-4">
                <!-- question -->
                <div class="h5 mb-3 d-flex justify-content-between">
                    <div>
                        <span class="me-3">{{ index + 1 }}.</span>
                        <span>{{ question.question }}</span>
                    </div>

                    <!-- marks -->
                     <div class="text-secondary me-2 fs-6">{{ question.score }} marks</div>
                </div>
                
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

                <!-- clear option btn and correct option display -->
                <button class="text-secondary link-underline-secondary clear-btn"
                @click="clearOption(question.id)" :disabled="state.quizEnded"
                v-if="!state.quizEnded">
                    Clear Option
                </button>

                <div v-else class="mt-3 fw-medium d-flex align-items-center">
                    <span>Correct Option: </span>
                    <span class="text-success fs-5 ms-2">{{ question.correct_option.toUpperCase() }}</span>
                </div>
            </div>
        </div>
    </main>

    <!-- menu -->
    <div class="menu bg-success-subtle" :class="{'menu-later': state.quizStarted}"
    v-show="!state.quizEnded">
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
    transition: 1s;
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
    background-color: #0d6efd;
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

.modal-subheading {
    font-size: small;
    margin-left: 1px;
}
.modal-heading {
    line-height: normal;
}


.total-score {
    font-size: 12px;
}
.score {
    font-size: 22px;
}
</style>