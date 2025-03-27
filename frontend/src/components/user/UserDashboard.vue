<script setup>
import Navbar from '@/components/Navbar.vue';
import { RouterView } from 'vue-router';
import { getCurrentUser } from '@/utils/auth';
import { onMounted, ref } from 'vue';
import { api } from '@/utils/auth';

const leftLinks = [
    { text: 'Quizzes', link: `/user/${getCurrentUser()}` },
    { text: 'Attempts', link: `/user/${getCurrentUser()}/attempts` },
];
const editProfileLink = "#";
const maxWidth = '940px';
const userName = ref('');
const profilePicUrl = ref('');

let profilePic = '';

onMounted(async () => {
    let response;
    // fetch user details
    try {
        response = await api.get(`/user/${getCurrentUser()}`);
        userName.value = response.data.data.username;
        profilePic = response.data.data.profile_pic;
    } catch (error) {
        console.log(error.response?.data || error);
    }

    // welcome msg
    window.showToast("Successfully Logged In", 'success', `Welcome ${userName.value}`);

    // fetch profile pic
    try {
        response = await api.get(`/${profilePic}`, {
            responseType: 'blob',
        });
        profilePicUrl.value = URL.createObjectURL(response.data)
    } catch (error) {
        console.log(error.response?.data || error);
    }
});
</script>

<template>
    <Navbar :leftLinks="leftLinks" :editProfileLink="editProfileLink"
    :maxWidth="maxWidth" :user-name="userName" :profile-pic-url="profilePicUrl" />
    <RouterView />
</template>