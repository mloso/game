import {createRouter, createWebHistory} from "vue-router";
import Home from "./pages/Game.vue";
import Register from "./pages/Register.vue";
import Login from "./pages/Login.vue";

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: "/login",
            name: "login",
            component: Login,
            meta: {requiresAuth: false}
        },
        {
            path: "/register",
            name: "register",
            component: Register,
            meta: {requiresAuth: false}
        },
        {
            path: "/game",
            name: "game",
            component: Home,
            meta: {requiresAuth: true}
        },
        {
            path: "/:pathMatch(.*)*",
            redirect: "/login"
        }
    ]
});

router.beforeEach((to, from, next) => {
    const isAuthenticated = localStorage.getItem("token");

    if (to.meta.requiresAuth && !isAuthenticated) {
        next({name: "login"});
    } else if ((to.name === "login" || to.name === "register") && isAuthenticated) {
        next({name: "game"});
    } else {
        next();
    }
});

export default router;
