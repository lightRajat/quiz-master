<script setup>
import { RouterLink, useRoute, useRouter } from 'vue-router';
import { logoutUser } from '@/utils/auth';

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
    },
    profilePicUrl: {
        type: String,
        default: ""
    },
    userName: String,
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
            <!-- left links -->
            <div class="mx-5 navbar-nav">
                <RouterLink v-for="(link, index) in leftLinks" :key="index"
                class="nav-link" :to="link.link" :class="isLinkActive(link.link) ? 'active' : ''">
                    <i v-if="index === 0 && userName === 'Admin'" class="bi bi-house"></i>
                    <i v-if="index === 0 && userName !== 'Admin'" class="bi bi-card-checklist"></i>
                    {{ link.text }}
                </RouterLink>
            </div>

            <!-- right links -->
            <div class="nav-item dropdown">
                <!-- front -->
                <button class="nav-link dropdown-toggle" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                    <img v-if="profilePicUrl" :src="profilePicUrl" alt="Profile Picture">
                    <i v-else class="bi bi-person"></i>
                    {{ userName }}
                </button>

                <!-- dropdown -->
                <ul class="dropdown-menu">
                    <li>
                        <button class="dropdown-item" data-bs-toggle="modal"
                        :data-bs-target="`#${editProfileLink}`">
                            Edit Profile
                        </button>
                    </li>
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

<style scoped>
img {
    width: 40px;
    border-radius: 100px;
    margin-right: 2px;
}
</style>