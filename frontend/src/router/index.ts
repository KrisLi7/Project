import { createRouter, createWebHistory } from "vue-router";

import Home from "@/views/Home.vue";
import About from "@/views/About.vue";

import Login from "@/views/Login.vue";
import Register from "@/views/Register.vue";
import RequestResetPassword from "@/views/RequestResetPassword.vue";
import ResetPassword from "@/views/ResetPassword.vue";
import Success from "@/views/Success.vue";
import Error from "@/views/Error.vue";
import VerifyEmail from "@/views/VerifyEmail.vue";

import Space from "@/views/Space.vue";
import Search from "@/views/Search.vue";
import MoviePage from "@/views/MoviePage.vue";
// import Actor from "@/views/Actor.vue";

import ActorDetail from "@/views/ActorDetail.vue";
import MovieDetail from "@/views/MovieDetail.vue";
import Profile from "@/views/Profile.vue";
import VisitorProfile from "@/views/VisitorProfile.vue";

const routes = [
    {
        // 00. 主页面 => 根页面
        path: "/",
        name: "Root",
        component: () => import('@/views/Home.vue'),
    },
    {
        // 01. 主页面
        path: "/home",
        name: "Home",
        component: Home,
    },

    {
        // 02. 网站详情
        path: "/about",
        name: "About",
        component: About,
    },

    {
        // 03. 登录界面
        path: "/login",
        name: "Login",
        component: Login,
    },

    {
        path: "/success",
        name: "Success",
        component: Success,
    },

    {
        path: "/error",
        name: "Error",
        component: Error,
    },

    {
        // 04. 注册界面
        path: "/register",
        name: "Register",
        component: Register,
    },

    {
        // 05. 重置密码
        path: "/password/request",
        name: "RequestResetPassword",
        component: RequestResetPassword,
    },

    {
        // 05. 重置密码
        path: "/password/reset",
        name: "ResetPassword",
        component: ResetPassword,
    },

    {
        // 06.
        path: "/verify/email/:u_id",
        name: "VerifyEmail",
        component: VerifyEmail,
    },

    {
        // 06.
        path: "/verify/email",
        name: "PlainVerifyEmail",
        component: VerifyEmail,
    },

    // {
    //     // 04. 个人中心
    //     path: "/space",
    //     name: "Space",
    //     component: Space,
    // },

    {
        // 04. 个人详情
        path: "/profile",
        name: "Profile",
        component: Profile,
    },
    {
        // 04. 他人详情
        path: "/profile/:u_id",
        name: "VisitorProfile",
        component: VisitorProfile,
    },

    {
        // 05. 高级搜索
        path: "/search",
        name: "Search",
        component: Search,
    },

    {
        // 06. 电影详情
        path: "/movie",
        name: "MoviePage",
        component: MoviePage,
    },

    {
        // 07. 电影详情 01
        path: "/movie/:m_id",
        name: "MovieDetail",
        component: MovieDetail,
    },

    {
        path: "/actor/:p_id",
        name: "ActorDetail",
        component: ActorDetail,
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
