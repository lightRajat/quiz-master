<script setup>
import Navbar from '@/components/Navbar.vue';
import { RouterView } from 'vue-router';

const leftLinks = [
    { text: 'Home', link: '/admin' },
    { text: 'Subjects', link: '/admin/subjects' },
    { text: 'Quizzes', link: '/admin/quizzes' },
    { text: 'Attempts', link: '#' },
    { text: 'Users', link: '#' },
];
const editProfileLink = "#";
const maxWidth = '940px';
</script>

<template>
    <Navbar :leftLinks="leftLinks" :editProfileLink="editProfileLink" :maxWidth="maxWidth" />
    <RouterView />
</template>