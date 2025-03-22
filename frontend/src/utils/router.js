import { createRouter, createWebHistory } from 'vue-router';

import Login from '@/views/public/Login.vue';
import Signup from '@/views/public/Signup.vue';
import Home from '@/views/public/Home.vue';
import AdminDashboard from '@/views/admin/Dashboard.vue';
import UserDashboard from '@/views/user/Dashboard.vue';
import NotFound from '@/views/public/NotFound.vue';
import Unauthorized from '@/views/public/Unauthorized.vue';

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/', name: 'home', component: Home,
            children: [
                {path: '/', name: 'login', component: Login, meta: {title: "Login"}},
                {path: '/signup', name: 'signup', component: Signup, meta: {title: "Signup"}}
            ]
        },
        {
            path: '/admin', name: 'admin-dashboard', component: AdminDashboard
        },
        {
            path: '/user/:username', name: 'user-dashboard', component: UserDashboard
        },
        {path: '/:catchAll(.*)', name: 'not-found', component: NotFound},
        {path: '/unauthorized', name: 'unauthorized', component: Unauthorized}
    ]
});

router.afterEach((to) => {
    document.title = to.meta.title || "Quiz Master";
});

export default router;