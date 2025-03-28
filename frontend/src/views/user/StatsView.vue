<script setup>
import { Pie } from "vue-chartjs";
import { Chart as ChartJS, Title, Tooltip, ArcElement } from "chart.js";
import ChartDataLabels from "chartjs-plugin-datalabels";
import { ref, onMounted, reactive } from "vue";
import { api, getCurrentUser } from "@/utils/auth";

// chartjs config
ChartJS.register(Title, Tooltip, ArcElement, ChartDataLabels);
ChartJS.defaults.font.family = "'Poppins', sans-serif";
ChartJS.defaults.font.size = 16;
ChartJS.defaults.font.weight = "bold";
ChartJS.defaults.color = "#333";
ChartJS.defaults.plugins.title.font.size = 22;
ChartJS.defaults.plugins.title.font.weight = "bold";
ChartJS.defaults.plugins.title.color = "#111";
ChartJS.defaults.plugins.datalabels = {
  color: "#eee",
  font: {
    size: 16,
    weight: "bold",
  },
};

const state = reactive({
    attempts: [],
    answersCount: {
        correct: 0,
        incorrect: 0,
        unattempted: 0,
        total: 0,
    }
});

const trueAnswerDist = ref({
    visible: false,
    data: {
        labels: ["Correct", "Incorrect", "Unattempted"],
        datasets: [{
                data: [10, 20, 30],
                backgroundColor: ["#198754", "#dc3545", "#aaaaaa"],
                borderWidth: 0,
            }],
    },
    options: {
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: false,
            },
            title: {
                display: true,
                text: "",
            },
            datalabels: {
                formatter: (value, context) => {
                    return `${context.chart.data.labels[context.dataIndex]}\n${getPercentage(value, state.answersCount.total)}% (${value})`;
                },
            },
        },
    },
});
const trueAnswerDistChart = ref(null);

const getPercentage = (value, total) => {
    return Math.round(value / total * 100);
};

const downloadChart = () => {
    if (!trueAnswerDistChart.value?.chart) return;

    const canvas = trueAnswerDistChart.value.chart.canvas;

    // make white bg
    const newCanvas = document.createElement("canvas");
    newCanvas.width = canvas.width;
    newCanvas.height = canvas.height;

    const ctx = newCanvas.getContext("2d");
    ctx.fillStyle = "white";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.drawImage(canvas, 0, 0);

    const anchorElem = document.createElement("a");
    anchorElem.href = newCanvas.toDataURL("image/jpeg");
    anchorElem.download = 'answerCorrectnessChart.jpg';
    anchorElem.click();
}

onMounted(async () => {
    try {
        // fetch attempts
        let response = await api.get(`/attempts?user_id=${getCurrentUser()}`);
        state.attempts = response.data.data;

        // fetch answers of each attempt
        for (const attempt of state.attempts) {
            response = await api.get(`/attempt-questions?attempt_id=${attempt.id}`);
            for (const question of response.data.data) {
                state.answersCount.total++;
                if (!question.selected_answer) {
                    state.answersCount.unattempted++;
                } else {
                    if (question.selected_answer === question.correct_answer) {
                        state.answersCount.correct++;
                    } else {
                        state.answersCount.incorrect++;
                    }
                }
            }
        }

        // update the answer count in pie chart
        trueAnswerDist.value.data.datasets[0].data = [
            state.answersCount.correct,
            state.answersCount.incorrect,
            state.answersCount.unattempted,
        ];
        trueAnswerDist.value.options.plugins.title.text = `Answer Correctness among ${state.answersCount.total} questions`;
        trueAnswerDist.value.visible = true;

    } catch (error) {
        console.log(error.response?.data || error);
    }
});
</script>

<template>
    <div class="chart-container" v-if="state.attempts.length">
        <div class="pie-chart">
            <Pie :data="trueAnswerDist.data" ref="trueAnswerDistChart"
            :options="trueAnswerDist.options" v-if="trueAnswerDist.visible" />
        </div>

        <button class="btn btn-primary mt-5" @click="downloadChart">
            <i class="bi bi-download me-1"></i>
            Download Chart as JPG
        </button>
    </div>
    <h2 v-else class="m-5">Go attempt some quizzes to view stats here</h2>
</template>

<style scoped>
.chart-container {
    width: 50%;
    padding: 16px;
    text-align: center;
    margin: 32px;
    outline: 1px solid #ddd;
    border-radius: 5px;
}
</style>