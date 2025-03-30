<script setup>
import { Pie, Bar } from "vue-chartjs";
import { Chart as ChartJS, Title, Tooltip, ArcElement, BarElement, CategoryScale, LinearScale, Legend } from "chart.js";
import ChartDataLabels from "chartjs-plugin-datalabels";
import { reactive, onMounted, ref } from 'vue';
import { api } from "@/utils/auth";

// chartjs config
ChartJS.register(Title, Tooltip, ArcElement, ChartDataLabels, BarElement, CategoryScale, LinearScale, Legend);
ChartJS.defaults.font.family = "'Poppins', sans-serif";
ChartJS.defaults.font.size = 16;
ChartJS.defaults.font.weight = "bold";
ChartJS.defaults.color = "#333";
ChartJS.defaults.plugins.title.font.size = 22;
ChartJS.defaults.plugins.title.font.weight = "bold";
ChartJS.defaults.plugins.title.color = "#111";
ChartJS.defaults.plugins.datalabels = {
  color: "#333",
  font: {
    size: 16,
    weight: "bold",
  },
};

const state = reactive({
    attempts: [],
    scopeCount: {
        subject: 0,
        chapter: 0,
    },
    dayAttemptedCount: [0, 0, 0, 0, 0, 0, 0],
});

const scopeDist = ref({
    visible: false,
    data: {
        labels: ["Subject", "Chapter"],
        datasets: [{
                data: [10, 20],
                backgroundColor: ["#ff6384", "#36a2eb"],
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
                text: ["Quiz Attempts by Scope", ''],
            },
            datalabels: {
                formatter: (value, context) => {
                    if (value != 0) {
                        return `${context.chart.data.labels[context.dataIndex]}\n${getPercentage(value, state.attempts.length)}% (${value})`;
                    }
                    return null;
                },
            },
        },
    },
});
const scopeDistChart = ref(null);

const dayAttemptedDist = ref({
    visible: false,
    data: {
        labels: ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
        datasets: [{
            label: "100",
            data: [10, 20, 30, 40, 50, 60, 70],
            backgroundColor: ["#3385FF", "#3385FF", "#3385FF", "#3385FF", "#3385FF", "#3385FF", "#3385FF"],
        }],
    },
    options: {
        responsive: true,
        maintainAspectRatio: true,
        plugins: {
            legend: {
                display: true,
                position: 'top',
                labels: {
                    boxWidth: 0,
                }
            },
            title: {
                display: true,
                text: 'Quiz Attempts Across Week Days',
                align: "center",
                padding: { bottom: 10 },
            },
            datalabels: {
                formatter: (value, context) => {
                    return (value != 0 ? value : null);
                },
            },
        },
        scales: {
            x: { grid: { display: false } },
            y: { grid: { display: false } },
        },
    },
});
const dayAttemptedDistChart = ref(null);

const getPercentage = (value, total) => {
    return Math.round(value / total * 100);
};

const downloadChart = (type) => {
    let chartElem;
    if (type == 'pie') {
        chartElem = scopeDistChart.value;
    } else {
        chartElem = dayAttemptedDistChart.value;
    }
    if (!chartElem?.chart) return;

    const canvas = chartElem.chart.canvas;

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
    anchorElem.download = type == 'pie' ? 'quizzesAcrossScopeChart.jpg' : 'quizzesAcrossDaysChart.jpg';
    anchorElem.click();
}

onMounted(async () => {
    try {
        // fetch all attempts
        let response = await api.get('/attempts');
        state.attempts = response.data.data;

        for (const attempt of state.attempts) {
            response = await api.get(`/quiz/${attempt.quiz_id}`);
            attempt.scope = response.data.data.scope;

            // count scopes
            if (attempt.scope === 'subject') {
                state.scopeCount.subject++;
            } else {
                state.scopeCount.chapter++;
            }
            state.scopeCount.total++;

            // count day attempted for week days
            const dayNum = new Date(attempt.date_attempted).getDay();
            state.dayAttemptedCount[dayNum]++;
        }
        
        // update scope counts in pie chart
        scopeDist.value.data.datasets[0].data = [state.scopeCount.subject, state.scopeCount.chapter];
        scopeDist.value.options.plugins.title.text[1] = `(Total: ${state.scopeCount.subject + state.scopeCount.chapter})`
        scopeDist.value.visible = true;

        // update dayAttempted counts in bar graph
        dayAttemptedDist.value.data.datasets[0].data = state.dayAttemptedCount;
        dayAttemptedDist.value.data.datasets[0].label = `Total: ${state.attempts.length}`;
        dayAttemptedDist.value.visible = true;
    } catch (error) {
        console.log(error.response?.data || error);
    }
});
</script>

<template>
    <main class="p-5">
        <div v-if="state.attempts.length" class="d-flex align-items-end">

            <!-- pie chart -->
            <div class="chart-container">

                <div>
                    <Pie :data="scopeDist.data" :options="scopeDist.options"
                    v-if="scopeDist.visible" ref="scopeDistChart" />
                </div>

                <button class="btn btn-primary mt-4" @click="downloadChart('pie')">
                    <i class="bi bi-download me-1"></i>
                    Download Chart as JPG
                </button>

            </div>

            <!-- bar chart -->
            <div class="chart-container">

                <div>
                    <Bar :data="dayAttemptedDist.data" :options="dayAttemptedDist.options"
                    v-if="dayAttemptedDist.visible" ref="dayAttemptedDistChart" />
                </div>

                <button class="btn btn-primary mt-4" @click="downloadChart('bar')">
                    <i class="bi bi-download me-1"></i>
                    Download Chart as JPG
                </button>

            </div>

        </div>

        <h2 v-else>Stats will appear here after users start attempting quizzes</h2>
    </main>
</template>

<style scoped>
.chart-container {
    width: 50%;
    padding: 16px;
    text-align: center;
}
</style>