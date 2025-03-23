<script setup>
    import { RouterLink, useRouter } from  'vue-router';
    import { ref } from 'vue';
    import axios from 'axios';

    const formElem = ref(null);
    const router = useRouter();

    const handleSubmit = async () => {
        const formData = new FormData(formElem.value);

        try {
            const response = await axios.post('/api/signup', formData);
            window.showToast(response.data.info, 'primary', "Now Log in with Your Credentials");
            router.push('/');
        } catch (error) {
            window.showToast(error.response.data.info, 'warning', "Use Another Email");
            formElem.value.reset();
        }
    };
</script>

<template>
    <h2 class="card-title text-center card-body display-6 mb-0">Sign Up</h2>
    <div class="card-body">
        <form ref="formElem" @submit.prevent="handleSubmit">
            <div class="row">
                <div class="mb-3 col">
                    <label class="form-label" for="name">Name</label>
                    <input name="name" type="text" class="form-control" placeholder="Enter your full name" id="name" required>
                </div>
                <div class="mb-3 col">
                    <label class="form-label" for="email">Email</label>
                    <input name="email" type="email" class="form-control" placeholder="Enter your email" id="email" required>
                </div>
            </div>
            <div class="row">
                <div class="mb-3 col">
                    <label class="form-label" for="password">Password</label>
                    <input name="password" type="password" class="form-control" placeholder="Create a strong password" id="password" required>
                </div>
                <div class="mb-3 col">
                    <label class="form-label" for="image">Profile Picture</label>
                    <input name="image" type="file" class="form-control" id="image" accept="image/*">
                </div>
            </div>
            <div class="row">
                <div class="mb-3 col">
                    <label class="form-label" for="qualification">Qualification</label>
                    <input name="qualification" type="text" class="form-control" placeholder="Enter your qualification" id="qualification">
                </div>
                <div class="mb-3 col">
                    <label class="form-label" for="dob">Date of Birth</label>
                    <input name="dob" type="date" class="form-control" id="dob">
                </div>
            </div>
            <div class="my-3 text-center">
                <button type="submit" class="btn btn-primary mb-3">Sign Up</button>
            </div>
        </form>
        <p class="text-center lead">
            Already have an account?
            <RouterLink to="/" class="link-opacity-75 link-opacity-100-hover link-offset-2-hover link-underline link-underline-opacity-0 link-underline-opacity-100-hover">
                Login here
            </RouterLink>
        </p>
    </div>
</template>

<style scoped>
    div.card-body {
        width: 750px;
        margin: 0 auto 0 auto;
    }
</style>