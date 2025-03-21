<script setup>
import { RouterLink, useRouter } from 'vue-router';
import { ref } from 'vue';
import axios from 'axios';

const formElem = ref(null);
const router = useRouter();

const handleSubmit = async () => {
    const formData = new FormData(formElem.value);
    try {
        const response = await axios.post('api/login', formData);
        if (response.data.user === 'admin') {
            router.push('/admin'); // TODO
        } else {
            router.push(''); // TODO
        }
        window.showToast(`Welcome ${response.data.user}`, "enjoy");

        sessionStorage.setItem('token', response.data.token)
    } catch (error) {
        window.showToast('Login Failed', error.response.data.info);
        formElem.value.reset();
    }
};
</script>

<template>
    <h2 class="card-title text-center card-body display-6 mb-0">Login</h2>
    <div class="card-body">
        <form ref="formElem" @submit.prevent="handleSubmit">
            <div class="mb-3">
                <label class="form-label" for="email">Email</label>
                <input name="email" type="text" class="form-control" placeholder="or enter your username" id="email"
                    required>
            </div>
            <div class="mb-3">
                <label class="form-label" for="password">Password</label>
                <input name="password" type="password" class="form-control"
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