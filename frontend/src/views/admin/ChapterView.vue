<script setup>
import Card from '@/components/Card.vue';
import { onMounted, ref } from 'vue';
import { api } from '@/utils/auth';
import { useRoute } from 'vue-router';

const route = useRoute();

const questions = ref([]);
const chapterId = ref('0');
const chapterName = ref('');

onMounted(async () => {
    const pathSplit = route.path.split('/');
    chapterId.value = pathSplit[pathSplit.length - 1];
    try {
        // fetch questions
        let response = await api.get(`/questions?chapter_id=${chapterId.value}`);
        questions.value = response.data.data;

        // fetch chapter name
        response = await api.get(`/chapter/${chapterId.value}`);
        chapterName.value = response.data.data.name;
        document.title = chapterName.value;
    } catch (error) {
        console.log(error);
    }
});
</script>

<template>
    <div class="m-3">
        <Card :heading="questions.length ? 'Questions' : 'No Questions Available'" :subheading="chapterName">
            <div v-for="(question, index) in questions" :key="index" class="card m-5">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-center">
                        <p class="h5">
                            <span class="me-3">{{ index + 1 }}.</span>
                            {{ question.question }}
                        </p>
                        <div class="btn-group" role="group">
                            <button class="btn btn-outline-secondary d-flex">
                                <i class="bi bi-pencil me-2"></i>
                                Edit
                            </button>
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
                                <div>{{ question.option_a }}</div>
                            </li>
                            <li>
                                <div>B. </div>
                                <div>{{ question.option_b }}</div>
                            </li>
                        </div>
                        <div v-if="question.option_c">
                            <li>
                                <div>C. </div>
                                <div>{{ question.option_c }}</div>
                            </li>
                            <li>
                                <div>D. </div>
                                <div>{{ question.option_d }}</div>
                            </li>
                        </div>
                    </ul>
                    <p>
                        Correct Option:
                        <span class="text-success">{{ question.correct_option.toUpperCase() }}</span>
                    </p>
                    <p>
                        Score:
                        <span class="text-secondary">{{ question.score }}</span>
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