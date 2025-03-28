<script setup>
import { Pie } from "vue-chartjs";
import { Chart as ChartJS, Title, Tooltip, ArcElement } from "chart.js";
import ChartDataLabels from "chartjs-plugin-datalabels";
import { reactive, onMounted, ref } from 'vue';
import { api } from "@/utils/auth";

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
  color: "#fff",
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
        total: 0,
    },
});

const scopeDistPieChart = ref({
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
                text: "Quiz Attempts in Subject vs Chapter Scopes",
            },
            datalabels: {
                formatter: (value, context) => {
                    return `${context.chart.data.labels[context.dataIndex]}\n${getPercentage(value, state.scopeCount.total)}%`;
                },
            },
        },
    },
});

const getPercentage = (value, total) => {
    return Math.round(value / total * 100);
};

onMounted(async () => {
    try {
        // fetch all attempts
        let response = await api.get('/attempts');
        state.attempts = response.data.data;

        // fetch scopes
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
        }
        
        // update scope counts in pie chart
        scopeDistPieChart.value.data.datasets[0].data = [state.scopeCount.subject, state.scopeCount.chapter];
        scopeDistPieChart.value.visible = true;
    } catch (error) {
        console.log(error.response?.data || error);
    }
});
</script>

<template>
    <main class="p-5">
        <Pie :data="scopeDistPieChart.data" :options="scopeDistPieChart.options"
        v-if="scopeDistPieChart.visible" />
    </main>
</template>