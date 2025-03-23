<script setup>
import { RouterLink, useRouter } from 'vue-router';
import { reactive } from 'vue';
import { loginUser } from '@/utils/auth';

const state = reactive({
    email: 'admin',
    password: 'admin'
});
const router = useRouter();

const handleSubmit = async () => {
    const response = await loginUser(state.email, state.password);
    if (response.status === 'failed') {
        window.showToast("Login Failed", 'warning', response.info);
        state.email = '',
        state.password = ''
    } else {
        window.showToast("Successfully Logged In", 'success', `Welcome ${response.user}`);
        if (response.user === 'admin') {
            router.push('/admin');
        } else {
            router.push(`/user/${response.user}`);
        }
    }
};
</script>

<template>
    <h2 class="card-title text-center card-body display-6 mb-0">Login</h2>
    <div class="card-body">
        <form @submit.prevent="handleSubmit">
            <div class="mb-3">
                <label class="form-label" for="email">Email</label>
                <input v-model="state.email" name="email" type="text" class="form-control" placeholder="or enter your username" id="email"
                    required>
            </div>
            <div class="mb-3">
                <label class="form-label" for="password">Password</label>
                <input v-model="state.password" name="password" type="password" class="form-control"
                    placeholder="Hope you didn't share it with anyone" id="password" required>
            </div>
            <div class="mb-3 text-center">
                <button type="submit" class="btn btn-primary mb-3">Submit</button>
            </div>
        </form>
        <p class="text-center lead">
            or <RouterLink to="/signup"
                class="link-opacity-75 link-opacity-100-hover link-offset-2-hover link-underline link-underline-opacity-0 link-underline-opacity-100-hover">
                Create an account</RouterLink>
        </p>
    </div>
</template>

<style scoped>
div.card-body {
    width: 400px;
    margin: 0 auto 0 auto;
}
</style>