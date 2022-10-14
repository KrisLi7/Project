<template>
    <div id="header">
        <el-menu default-active="/home" style="background-color: #040714; color: #F9F9F9" class="el-menu-demo"
            mode="horizontal" :ellipsis="false" :router="true" :border-bottom="null" @select="handle_select">
            <Logo id="logo"></Logo>
            <el-menu-item index="/home">Home</el-menu-item>
            <el-menu-item index="/movie">Advance Search</el-menu-item>
            <el-menu-item index="/search">Search</el-menu-item>
            <div class="flex-grow"> </div>
            <div id="normal-search-div">
                <NormalSearch></NormalSearch>
            </div>
            <div class="header-user-div">
                <div v-if="stone.getters.get_user.u_is_login == 0">
                    <el-menu-item style="background-color: #040714;" index="/login">Login</el-menu-item>
                </div>
                <div class="header-user-div" v-else>
                    <MessageNotify :u_token="stone.getters.get_user.u_token"></MessageNotify>
                    <el-sub-menu class="el-submenu" style="background-color: #040714;" index="4">
                        <template style="background-color: #040714;" #title>
                            <el-avatar v-if="stone.getters.get_user_profile.u_avatar"
                                :src="stone.getters.get_user_profile.u_avatar" />
                            <el-avatar v-else> user </el-avatar>
                        </template>
                        <el-menu-item style="background-color: #040714;" index="/profile">Profile</el-menu-item>
                        <el-menu-item style="background-color: #040714;" index="/home" @click="logout">Logout
                        </el-menu-item>
                    </el-sub-menu>
                </div>
            </div>
        </el-menu>
    </div>
</template>


<script lang="ts" setup>
import { AxiosError } from 'axios';
import { ElMessage } from 'element-plus'
import { ref } from "vue"
import { useStore } from 'vuex'
import NormalSearch from "./search/NormalSearch.vue";
import { api_logout } from "../api/service";
import Logo from './Logo.vue';
import MessageNotify from './message/MessageNotify.vue';

const stone = useStore();

const success_message = ref()

const error_message = ref()

const active_search = ref<boolean>(false)

const active_index = ref<string>("")

const handle_select = (key: string, path: string[]) => {
    if ("/search" === path[0]) {
        active_search.value = true
    } else {
        active_search.value = false
    }
}

const logout = async () => {
    try {
        await api_logout(stone.getters.get_user)
        stone.commit("clear_user")
        ElMessage({
            showClose: true,
            message: "Congrats, Logout Success",
            type: "success",
        })
    } catch (e) {
        let error = e as AxiosError
        error_message.value = error.response?.data
        ElMessage({
            showClose: true,
            message: "Oops, " + error_message.value,
            type: "error",
        })
    }
}
</script>


<style>
#header {
    display: flex;
    flex-direction: column;
    /* border: 1px solid #040714; */
    box-shadow: var(--el-box-shadow);
}

.flex-grow {
    flex-grow: 1;
}

#logo {
    display: flex;
    align-items: center;
}

#header_search_div {
    display: flex;
    flex-direction: column;
    margin: 10px auto;
}

#normal-search-div {
    display: flex;
    flex-direction: column;
    text-align: center;
    margin-top: 15px;
    margin-bottom: 0px;
}

.header-user-div {
    display: flex;
    flex-direction: row;
}

.el-menu--popup {
    background: rgb(11, 11, 11) !important;
    padding: 0 0;
    min-width: 120px !important;
    line-height: 40px !important;
    box-shadow: 0 4px 8px 0 rgba(25, 14, 109, 0.13);
    border-radius: 5px;
}
</style>
