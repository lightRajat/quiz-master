import { createRouter, createWebHistory } from 'vue-router';
import { getCurrentUser } from './auth';

import Landing from '@/components/public/Landing.vue';
import LoginView from '@/views/public/LoginView.vue';
import SignupView from '@/views/public/SignupView.vue';
import NotFoundView from '@/views/public/NotFoundView.vue';
import UnauthorizedView from '@/views/public/UnauthorizedView.vue';

import AdminDashboard from '@/components/admin/AdminDashboard.vue';
import AdminHomeView from '@/views/admin/HomeView.vue';
import AdminSubjectsView from '@/views/admin/SubjectsView.vue';
import AdminSubjectView from '@/views/admin/SubjectView.vue';
import AdminQuizzesView from '@/views/admin/QuizzesView.vue';
import AdminChapterView from '@/views/admin/ChapterView.vue';
import AdminQuizView from '@/views/admin/QuizView.vue';
import AdminAttemptsView from '@/views/admin/AttemptsView.vue';
import AdminStatsView from '@/views/admin/StatsView.vue';

import UserDashboard from '@/components/user/UserDashboard.vue';
import UserQuizzesView from '@/views/user/QuizzesView.vue';
import TakeAttemptView from '@/views/user/TakeAttemptView.vue';
import UserAttemptsView from '@/views/user/AttemptsView.vue';
import UserAttemptView from '@/views/user/AttemptView.vue';

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
            path: '/admin', name: 'admin-dashboard', component: AdminDashboard, meta: {requiresAuth: true},
            children: [
                {path: '/admin', name: 'admin-home', component: AdminHomeView, meta: {title: "Dashboard"}},
                {path: '/admin/subjects', name: 'admin-subjects', component: AdminSubjectsView, meta: {title: "Subjects"}},
                {path: '/admin/quizzes', name: 'admin-quizzes', component: AdminQuizzesView, meta: {title: "Quizzes"}},
                {path: '/admin/subject/:subject_id', name: 'admin-subject', component: AdminSubjectView},
                {path: '/admin/subject/:subject_id/:chapter_id', name: 'admin-chapter', component: AdminChapterView},
                {path: '/admin/quizzes/:quiz_id', name: 'admin-quiz', component: AdminQuizView, meta: {title: "Edit Questions"}},
                {path: '/admin/attempts', name: 'admin-attempts', component: AdminAttemptsView, meta: {title: "Quiz Attempts"}},
                {path: '/admin/stats', name: 'admin-stats', component: AdminStatsView, meta: {title: "Statistics"}},
            ]
        },
        {
            path: '/user/:user_id', name: 'user-dashboard', component: UserDashboard, meta: {requiresAuth: true},
            children: [
                {path: '/user/:user_id', name: 'user-quizzes', component: UserQuizzesView, meta: {title: "Quizzes"}},
                {path: '/user/:user_id/quiz/:quiz_id/take', name: 'user-quiz-take', component: TakeAttemptView, meta: {title: "Quiz"}},
                {path: '/user/:user_id/attempts', name: 'user-attempts', component: UserAttemptsView, meta: {title: "Quiz Attempts"}},
                {path: '/user/:user_id/attempt/:attempt_id', name: 'user-attempt', component: UserAttemptView, meta: {title: "Past Attempt"}},
            ]
        },
        {path: '/:catchAll(.*)', name: 'not-found', component: NotFoundView, meta: {title: "404 Not Found"}},
        {path: '/unauthorized', name: 'unauthorized', component: UnauthorizedView, meta: {title: "Not Authorized"}}
    ]
});

router.afterEach((to) => {
    document.title = to.meta.title || "Quiz Master";
});

router.beforeEach((to, from, next) => {
    if (to.meta.requiresAuth) {
        const pageOf = (() => {
            const pathSplit = to.path.split('/')
            if (pathSplit[1] === 'admin') {
                return 'admin';
            }
            return pathSplit[2];
        })();
        const currUser = getCurrentUser();
        if (pageOf !== currUser) {
            next('/unauthorized');
        } else {
            next();
        }
    } else {
        next();
    }
});

export default router;