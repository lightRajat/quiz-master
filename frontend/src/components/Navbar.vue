<script setup>
import { RouterLink, useRoute, useRouter } from 'vue-router';
import { logoutUser, getCurrentUser } from '@/utils/auth';

const router = useRouter();

defineProps({
    leftLinks: {
        type: Array,
        default: []
    },
    editProfileLink: {
        type: String,
        default: "#"
    },
    maxWidth: {
        type: String,
        default: "940px"
    }
});

const logOut = () => {
    logoutUser();
    router.push('/');
};

const isLinkActive = (link) => {
    const route = useRoute();
    return route.path === link;
};
</script>

<template>
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
        <div class="container d-flex justify-content-around lead" :style="`width: ${maxWidth};`">
            <div class="mx-5 navbar-nav">
                <RouterLink v-for="(link, index) in leftLinks" :key="index"
                class="nav-link" :to="link.link" :class="isLinkActive(link.link) ? 'active' : ''">
                    <i v-if="index === 0" class="bi bi-house"></i>
                    {{ link.text }}
                </RouterLink>
            </div>
            <div class="nav-item dropdown">
                <button class="nav-link dropdown-toggle" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                    <i class="bi bi-person"></i>
                    {{ getCurrentUser() }}
                </button>
                <ul class="dropdown-menu">
                    <li><RouterLink class="dropdown-item" :to="editProfileLink">Edit Profile</RouterLink></li>
                    <li>
                        <button @click="logOut" class="dropdown-item text-danger">
                            <i class="bi bi-box-arrow-right me-1"></i>
                            Logout
                        </button>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
</template>