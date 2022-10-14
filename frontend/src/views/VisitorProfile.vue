<template>
    <div class="user_detail" :sm="900" :lg="900">
        <br>
        <br>
        <h2 class="profile-title color-main">User's Profile Page</h2>
        <br>
        <el-row>
            <el-col :span="6"><div class="grid-content ep-bg-purple-light" /></el-col>
            <el-col :span="6"><div class="grid-content ep-bg-purple" />
                <div id="detail-header">
                    Basic Information
                </div>
            </el-col>
        </el-row>
        <el-row><br></el-row>
        <el-row>
            <el-col :span="6"><div class="grid-content ep-bg-purple-light" /></el-col>
            <el-col :span="6"><div class="grid-content ep-bg-purple" />
                <!-- <img :src="state.getters.get_user_profile.u_avatar" class="avatar" /> -->
                <el-image v-if="user_obj?.u_avatar" :src="user_obj?.u_avatar" :fit="'contain'" />
            </el-col>
            <el-col :span="6"><div class="grid-content ep-bg-purple" />
                <el-descriptions>
                    <el-descriptions-item>
                        <div id="critic_color" v-if="user_obj?.u_is_critic_reviewer">
                            <box-icon name='analyse' flip='vertical' animation='spin' color='#D58C12' ></box-icon>
                            &nbspCritic Reviewer
                        </div>
                        <div id="critic_color" v-else >
                            <box-icon name='analyse' flip='vertical' animation='spin' color='#0063e5' ></box-icon>
                            &nbspNon Critic Reviewer
                        </div>
                    </el-descriptions-item>
                </el-descriptions>
                <br>
                <br>
                <el-descriptions>
                    <el-descriptions-item label="User ID">
                        <div class="user-label">
                            {{ user_obj?.u_id }}
                        </div>
                </el-descriptions-item>

                </el-descriptions>
                <br>
                <br>
                <!-- <el-progress :text-inside="true" :stroke-width="30" :percentage="70" /> -->
                <el-descriptions>
                    <el-descriptions-item>
                        <div class="user-label">
                            {{ "Level: " + user_obj?.u_level }}
                        </div>
                    </el-descriptions-item>
                    <el-descriptions-item>
                        <el-progress :text-inside="true" :stroke-width="25" percentage="user_obj?.u_exp / 2500 * 100" color="#0063E5">
                            {{ user_obj?.u_exp + " / 2500" }}
                        </el-progress>
                    </el-descriptions-item>
                </el-descriptions>
            </el-col>
            <el-col :span="6"><div class="grid-content ep-bg-purple" />
                <el-descriptions>
                    <el-descriptions-item label="Banned User">
                    <span @click="onStatus">
                    <el-button round>
                        <div v-if="user_obj?.u_is_banned">
                            <box-icon type='solid' name='ghost' color="#ff0000"></box-icon>
                        </div>
                        <div v-else>
                            <box-icon type='solid' name='ghost' color="#040714"></box-icon>
                        </div>
                    </el-button>

                    </span>

                    </el-descriptions-item>
                </el-descriptions>
            </el-col>
        </el-row>
        <br>
        <br>
        <el-row>
            <el-col :span="6"><div class="grid-content ep-bg-purple" /></el-col>
            <el-col :span="6"><div class="grid-content ep-bg-purple-light" />
                <el-descriptions>
                    <el-descriptions-item label="Username">
                        <div class="user-label">
                            {{ user_obj?.u_username }}
                        </div>
                    </el-descriptions-item>
                </el-descriptions>
            </el-col>
            <el-col :span="6"><div class="grid-content ep-bg-purple" />
                <el-descriptions>
                    <el-descriptions-item label="Last Name">
                        <div class="user-label" >
                            {{ user_obj?.u_lastname }}
                        </div>
                    </el-descriptions-item>
                </el-descriptions>
            </el-col>
            <el-col :span="6"><div class="grid-content ep-bg-purple-light" /></el-col>
        </el-row>

        <el-row>
            <el-col :span="6"><div class="grid-content ep-bg-purple" /></el-col>
            <el-col :span="6"><div class="grid-content ep-bg-purple-light" />
                <el-descriptions>
                    <el-descriptions-item label="First Name">
                        <div class="user-label">
                            {{ user_obj?.u_firstname }}
                        </div>
                    </el-descriptions-item>
                </el-descriptions>
            </el-col>
            <el-col :span="6"><div class="grid-content ep-bg-purple" />
                <el-descriptions>
                    <el-descriptions-item label="User Email">
                        <div class="user-label">
                            {{ user_obj?.u_email }}
                        </div>
                    </el-descriptions-item>
                </el-descriptions>
            </el-col>
            <el-col :span="6"><div class="grid-content ep-bg-purple-light" /></el-col>
        </el-row>
        <el-row>
            <el-col :span="6"><div class="grid-content ep-bg-purple" /></el-col>
            <el-col :span="12"><div class="grid-content ep-bg-purple-light" />
                <div id="detail-header">
                    Wish List
                    <swiper :slides-per-view="3" :space-between="30" :autoplay="autoplay">
                        <swiper-slide v-for="item in user_obj?.u_wishlist">
                            <MovieCard :tcejbo="item"></MovieCard>
                        </swiper-slide>
                    </swiper>
                </div>
            </el-col>
            <el-col :span="6"><div class="grid-content ep-bg-purple-light" /></el-col>
        </el-row>
        <el-row><br></el-row>
    </div>
</template>

<script lang="ts">
import { AxiosError } from 'axios';
import { ref, defineComponent, reactive } from 'vue'
import { ElMessage } from 'element-plus';
import { api_get_visit_user,
    api_change_user_ban_status,
    api_change_user_remove_ban_status
} from '../api/service';
import { useStore } from 'vuex'
import UserAvatar from '../components/UserAvatar.vue'
import { VisitUserObject } from '../types';
import router from '../router';
import { useRoute } from 'vue-router';
import 'boxicons'
import 'swiper/css';
import { Swiper, SwiperSlide } from 'swiper/vue';
import MovieCard from '../components/MovieCard.vue';
import SwiperCore, { Autoplay } from "swiper"

SwiperCore.use([Autoplay])

export default defineComponent({
    name: "VisitorProfile",
    props: {  },
    components: { UserAvatar, Swiper, SwiperSlide, MovieCard },
    setup: function () {
        const state = useStore()
        const error_message = ref()
        const route = useRoute()
        const dialogTableVisible = ref(false)
        const user_obj = ref<VisitUserObject>()

        const ban_user_obj = reactive({
            u_token: "",
            banned_u_id: route.params.u_id
        })


        const get_visit_user_object = reactive({
            u_token: "",
            u_id_visit: route.params.u_id
        })

        const onStatus = async () => {
            try {
                let res
                if (user_obj.value?.u_is_banned) {
                    ban_user_obj.u_token = state.getters.get_user.u_token
                    res = await api_change_user_remove_ban_status(ban_user_obj)
                } else {
                    ban_user_obj.u_token = state.getters.get_user.u_token
                    res = await api_change_user_ban_status(ban_user_obj)
                }
                get_current_user()
                ElMessage({
                        showClose: true,
                        message: res.data.message,
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

        const get_current_user = async (): Promise<void> => {
            try {
                if (route.params.u_id == state.getters.get_user.u_id) {
                    router.push("/profile")
                }
                get_visit_user_object.u_token = state.getters.get_user.u_token
                let res = await api_get_visit_user(get_visit_user_object)
                user_obj.value = res.data
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

        return {
            get_current_user,
            dialogTableVisible,
            onStatus,
            user_obj,
            autoplay: {
                delay: 5000
            },
        };
    },
    created() {
        this.$watch(
            () => this.$route.params,
            () => {
                this.get_current_user()
            },
            { immediate: true }
        )
    },
})
</script>

<style lang="less">
#profile {
    display: flex;
    flex-direction: column;
}

#detail-header {
    margin-left: 0px;
    text-align: Left;
    font-size: 1.2rem;
    font-weight: 700;
    // text-transform: uppercase;
    color: var(--main-color);
    float: left;
}


.user_detail {
    background-color: #040714;
}

.profile-title {
    text-align: center;
    color: #f9f9f9;
}

.user-label {
    color: #f9f9f9;
}

#critic_color {
    color:#F9F9F9 !important
}

.el-descriptions__body {
    background-color: transparent !important;
    box-shadow: none;
}

.el-descriptions__label:not(.is-bordered-label) {
    color: #f9f9f9 !important;
    margin-right: 16px;
}

.el-descriptions-item {
    color: #f9f9f9 !important;
    padding: 0 400px !important;
}

.el-image {
    margin-right:50px !important;
}

</style>
