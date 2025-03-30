<script setup>
import Navbar from '@/components/Navbar.vue';
import { RouterView, useRoute } from 'vue-router';
import { getCurrentUser } from '@/utils/auth';
import { onMounted, reactive, computed } from 'vue';
import { api } from '@/utils/auth';

const route = useRoute();

const state = reactive({
    leftLinks: [
        { text: 'Quizzes', link: `/user/${getCurrentUser()}` },
        { text: 'Past Quizzes', link: `/user/${getCurrentUser()}/attempts` },
        { text: 'Stats', link: `/user/${getCurrentUser()}/stats` },
    ],
    maxWidth: '940px',
    user: {},
    profilePicUrl: '',
});

const isPageTakeQuiz = computed(() => {
    const pathSplit = route.path.split('/');
    return pathSplit[pathSplit.length - 1] === 'take';
});

const updateProfile = async () => {
    const formData = new FormData(document.getElementById('edit-profile-form'));
    try {
        await api.put(`/user/${state.user.id}`, formData);
        window.showToast("Profile Successfully Updated", 'success', "Profile picture would update on next login");
    } catch (error) {
        console.error(error.response?.data || error);
        window.showToast("Can't Update Profile", 'danger', error.response?.data.info);
    }

    // clear form and close panel
    document.getElementById('edit-profile-password').value = '';
    document.getElementById('edit-profile-image').value = '';
    document.getElementById('edit-profile-close').click();
};

const fetchProfilePic = async () => {
    if (!state.user.profile_pic) return;
    
    const response = await api.get(state.user.profile_pic, {
        responseType: 'blob',
    });
    state.profilePicUrl = URL.createObjectURL(response.data);
};

onMounted(async () => {
    try {
        // fetch user details
        let response = await api.get(`/user/${getCurrentUser()}`);
        state.user = response.data.data;

        // welcome msg
        window.showToast("Successfully Logged In", 'success', `Welcome ${state.user.name.split(' ')[0]}`);

        await fetchProfilePic();
    } catch (error) {
        console.log(error.response?.data || error);
    }
});
</script>

<template>
    <Navbar v-show="!isPageTakeQuiz" :leftLinks="state.leftLinks" editProfileLink="edit-profile-menu"
    :maxWidth="state.maxWidth" :user-name="state.user.username" :profile-pic-url="state.profilePicUrl" />
    <RouterView />

    <!-- edit profile menu -->
    <div class="modal fade" id="edit-profile-menu" tabindex="-1" aria-hidden="true"
    aria-labelledby="edit-profile-title">
        <div class="modal-dialog modal-lg">
            <!-- modal head -->
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" id="edit-profile-title">Edit Profile</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"
                    aria-label="Close" id="edit-profile-close"></button>
                </div>

                <!-- modal body -->
                <div class="modal-body">
                    <form id="edit-profile-form" @submit.prevent="updateProfile">

                        <!-- name and username -->
                        <div class="row">
                            <div class="mb-3 col">
                                <label class="form-label" for="edit-profile-name">Name*</label>
                                <input name="name" type="text" class="form-control"
                                placeholder="Enter your full name" id="edit-profile-name"
                                v-model="state.user.name" required>
                            </div>

                            <div class="mb-3 col">
                                <label class="form-label" for="edit-profile-username">Username*</label>
                                <input name="username" type="text"
                                class="form-control" placeholder="Choose a unique username"
                                id="edit-profile-username" v-model="state.user.username" required>
                            </div>
                        </div>

                        <!-- qualification and dob -->
                        <div class="row">
                            <div class="mb-3 col">
                                <label class="form-label" for="edit-profile-qualification">Qualification</label>
                                <input name="qualification" type="text"
                                class="form-control" placeholder="Enter your qualification"
                                id="edit-profile-qualification" v-model="state.user.qualification">
                            </div>

                            <div class="mb-3 col">
                                <label class="form-label" for="edit-profile-dob">Date of Birth</label>
                                <input name="dob" type="date" class="form-control"
                                id="edit-profile-dob" v-model="state.user.dob">
                            </div>
                        </div>

                        <!-- password and profile picture -->
                        <div class="row">
                            <div class="mb-3 col">
                                <label class="form-label" for="edit-profile-password">New Password</label>
                                <input name="password" type="password"
                                class="form-control" placeholder="Create a strong password"
                                id="edit-profile-password">
                            </div>

                            <div class="mb-3 col">
                                <label class="form-label" for="edit-profile-image">New Profile Picture</label>
                                <input name="image" type="file"
                                class="form-control" id="edit-profile-image" accept="image/*">
                            </div>
                        </div>

                        <!-- email -->
                        <div>
                            <div class="mb-3 col-6 mx-auto">
                                <label class="form-label" for="edit-profile-email">Email*</label>
                                <input name="email" type="email" class="form-control"
                                id="edit-profile-email" placeholder="Enter your email"
                                v-model="state.user.email" required>
                            </div>
                        </div>
                    </form>
                </div>

                <!-- modal footer -->
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                        Cancel
                    </button>

                    <button form="edit-profile-form" type="submit" class="btn btn-success">
                        <i class="bi bi-pencil me-1"></i>
                        Update
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>