<script setup>
import Navbar from '@/components/Navbar.vue';
import { api } from '@/utils/auth';
import { onMounted, reactive } from 'vue';
import { RouterView } from 'vue-router';

const state = reactive({
    adminPassword: '',
});

const leftLinks = [
    { text: 'Home', link: '/admin' },
    { text: 'Subjects', link: '/admin/subjects' },
    { text: 'Quizzes', link: '/admin/quizzes' },
    { text: 'Attempts', link: '/admin/attempts' },
    { text: 'Users', link: '#' },
];
const maxWidth = '940px';

// welcome msg
window.showToast("Successfully Logged In", 'success', "Welcome Admin");

const updateAdminPassword = async () => {
    try {
        const response = await api.post('/admin-creds', {password: state.adminPassword});
        console.log(response.data);
        window.showToast("Password Successfully Updates", 'success', "You can now login with your New Password")
        document.getElementById('edit-menu-close').click();
    } catch (error) {
        console.error(error.response?.data || error);
    }
};

onMounted(async () => {
    try {
        const response = await api.get('/admin-creds');
        state.adminPassword = response.data.data.password;
    } catch (error) {
        console.error(error.response?.data || error);
    }
});
</script>

<template>
    <Navbar :leftLinks="leftLinks" editProfileLink="edit-profile-menu"
    :maxWidth="maxWidth" userName="Admin" />
    <RouterView />

    <!-- edit profile menu -->
    <div class="modal fade" id="edit-profile-menu" tabindex="-1" aria-hidden="true"
    aria-labelledby="edit-profile-menu-title">
        <div class="modal-dialog modal-dialog-centered">
            <!-- modal head -->
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" id="edit-profile-menu-title">Update Password</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"
                    aria-label="Close" id="edit-menu-close"></button>
                </div>

                <!-- modal body -->
                <div class="modal-body">
                    <form id="edit-profile-menu-form" @submit.prevent="updateAdminPassword">
                        <!-- username -->
                        <div class="mb-3">
                            <label class="form-label">Username</label>
                            <input type="text" class="form-control" value="admin" disabled>
                        </div>

                        <!-- password -->
                        <div class="mb-3">
                            <label class="form-label" for="password">Password</label>
                            <input type="password" name="password" id="password" required
                            class="form-control" v-model="state.adminPassword">
                        </div>
                    </form>
                </div>

                <!-- modal footer -->
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                        Cancel
                    </button>
                    <button form="edit-profile-menu-form" type="submit" class="btn btn-success">
                        <i class="bi bi-pencil me-1"></i>
                        Update
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>