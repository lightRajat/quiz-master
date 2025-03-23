import { createRouter, createWebHistory } from 'vue-router';

import Landing from '@/components/public/Landing.vue';
import LoginView from '@/views/public/LoginView.vue';
import SignupView from '@/views/public/SignupView.vue';
import NotFoundView from '@/views/public/NotFoundView.vue';
import UnauthorizedView from '@/views/public/UnauthorizedView.vue';

import AdminDashboard from '@/components/admin/AdminDashboard.vue';
import UserDashboard from '@/views/user/Dashboard.vue';
import AdminHomeView from '@/views/admin/HomeView.vue';
import AdminSubjectView from '@/views/admin/SubjectView.vue';
import AdminQuizView from '@/views/admin/QuizView.vue';

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/', name: 'landing', component: Landing,
            children: [
                {path: '/', name: 'login', component: LoginView, meta: {title: "Login"}},
                {path: '/signup', name: 'signup', component: SignupView, meta: {title: "Signup"}}
            ]
        },
        {
            path: '/admin', name: 'admin-dashboard', component: AdminDashboard,
            children: [
                {path: '/admin', name: 'admin-home', component: AdminHomeView, meta: {title: "Dashboard"}},
                {path: '/admin/subjects', name: 'admin-subject', component: AdminSubjectView, meta: {title: "Subjects"}},
                {path: '/admin/quizzes', name: 'admin-quiz', component: AdminQuizView, meta: {title: "Quizzes"}},
            ]
        },
        {
            path: '/user/:username', name: 'user-dashboard', component: UserDashboard
        },
        {path: '/:catchAll(.*)', name: 'not-found', component: NotFoundView, meta: {title: "404 Not Found"}},
        {path: '/unauthorized', name: 'unauthorized', component: UnauthorizedView, meta: {title: "Not Authorized"}}
    ]
});

router.afterEach((to) => {
    document.title = to.meta.title || "Quiz Master";
});

export default router;