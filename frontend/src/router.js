import { createRouter, createWebHistory } from 'vue-router';

import Login from './components/public/Login.vue';
import Signup from './components/public/Signup.vue';
import Home from './components/public/Home.vue';

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/', name: 'home', component: Home,
            children: [
                {path: '/', name: 'login', component: Login, meta: {title: "Login"}},
                {path: '/signup', name: 'signup', component: Signup, meta: {title: "Signup"}}
            ]
        }
    ]
});

router.afterEach((to) => {
    document.title = to.meta.title || "Quiz Master";
});

export default router;