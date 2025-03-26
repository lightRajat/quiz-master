<script setup>
import Navbar from '@/components/Navbar.vue';
import { RouterView } from 'vue-router';
import { getCurrentUser } from '@/utils/auth';

const leftLinks = [
    { text: 'Home', link: `/user/${getCurrentUser()}` },
    { text: 'Quizzes', link: '#' },
    { text: 'Attempts', link: '#' },
];
const editProfileLink = "#";
const maxWidth = '940px';
</script>

<template>
    <Navbar :leftLinks="leftLinks" :editProfileLink="editProfileLink"
    :maxWidth="maxWidth" />
    <RouterView />
</template>