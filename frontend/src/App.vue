<script setup>
  import axios from 'axios';
  import { onMounted, reactive } from 'vue';

  const state = reactive({
    name: ''
  });

  onMounted(async () => {
    const response = await axios.get('/api/');
    state.name = response.data.name;
  });
</script>

<template>
  <h1>Hello {{ state.name }}</h1>
</template>