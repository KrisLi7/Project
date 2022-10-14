<template>
    <div id="user_detail" :sm="900" :lg="900">
        <br>
        <br>
        <h2 id="profile-title color-main">User's Profile Page</h2>
        <br>
        <el-row>
            <el-col :span="6">
                <div class="grid-content ep-bg-purple-light" />
            </el-col>
            <el-col :span="6">
                <div class="grid-content ep-bg-purple" />
                <div id="detail-header">
                    Basic Information
                </div>
            </el-col>
        </el-row>
        <el-row><br></el-row>
        <el-row>
            <el-col :span="6">
                <div class="grid-content ep-bg-purple-light" />
            </el-col>
            <el-col :span="6">
                <div class="grid-content ep-bg-purple" />
                <UserAvatar :tcejbo="user_obj?.u_avatar"></UserAvatar>
            </el-col>
            <el-col :span="6">
                <div class="grid-content ep-bg-purple" />
                <el-descriptions>
                    <el-descriptions-item id="col_shape" >
                        <div id="critic_color" v-if="state.getters.get_user_profile.u_is_critic_reviewer" >
                            <box-icon color='#D58C12' name='analyse' flip='vertical' animation='spin' ></box-icon>
                            &nbspCritic Reviewer
                        </div>
                        <div id="critic_color" v-else>
                            <box-icon color='#0063e5' name='analyse' flip='vertical' animation='spin' ></box-icon>
                            &nbspNon Critic Reviewer
                        </div>
                    </el-descriptions-item>
                </el-descriptions>
                <br>
                <br>
                <el-descriptions>
                    <el-descriptions-item id="label_title" label="User ID">
                        <div class="user-label">
                            {{ state.getters.get_user_profile.u_id }}
                        </div>
                    </el-descriptions-item>

                    <el-descriptions-item id="label_title" label="Email Notification">
                        <el-switch id="switch_on_color" v-model="state.getters.get_user_profile.u_notification" @change="onStatus" />
                    </el-descriptions-item>
                </el-descriptions>
                <br>
                <br>
                <el-descriptions>
                    <el-descriptions-item id="label_title">
                        <div class="user-label">
                            {{ "Level : " + state.getters.get_user_profile.u_level }}
                        </div>
                    </el-descriptions-item>
                    <el-descriptions-item id="label_title">
                        <el-progress :text-inside="true" :stroke-width="25" :percentage="percentage">
                            {{ state.getters.get_user_profile.u_exp + " / 2500" }}
                        </el-progress>
                    </el-descriptions-item>
                </el-descriptions>
            </el-col>
            <el-col :span="6">
                <div class="grid-content ep-bg-purple" />
            </el-col>
        </el-row>
        <br>
        <br>
        <el-row>
            <el-col :span="6">
                <div class="grid-content ep-bg-purple" />
            </el-col>
            <el-col :span="6">
                <div class="grid-content ep-bg-purple-light" />
                <el-descriptions>
                    <el-descriptions-item label="Username">
                        <UserDetail tcejbo="user name"></UserDetail> <br>
                        <div class="user-label">
                            {{ state.getters.get_user_profile.u_username }}
                        </div>
                    </el-descriptions-item>
                </el-descriptions>
            </el-col>
            <el-col :span="6">
                <div class="grid-content ep-bg-purple" />
                <el-descriptions>
                    <el-descriptions-item label="Last Name">
                        <UserDetail tcejbo="last name"></UserDetail>
                        <div class="user-label">
                            {{ state.getters.get_user_profile.u_lastname }}
                        </div>
                    </el-descriptions-item>
                </el-descriptions>
            </el-col>
            <el-col :span="6">
                <div class="grid-content ep-bg-purple-light" />
            </el-col>
        </el-row>

        <el-row>
            <el-col :span="6">
                <div class="grid-content ep-bg-purple" />
            </el-col>
            <el-col :span="6">
                <div class="grid-content ep-bg-purple-light" />
                <el-descriptions>
                    <el-descriptions-item label="First Name">
                        <UserDetail tcejbo="first name"></UserDetail>
                        <div class="user-label">
                            {{ state.getters.get_user_profile.u_firstname }}
                        </div>
                    </el-descriptions-item>
                </el-descriptions>
            </el-col>
            <el-col :span="6">
                <div class="grid-content ep-bg-purple" />
                <el-descriptions>
                    <el-descriptions-item label="User Email">
                        <UserDetail tcejbo="email"></UserDetail>
                        <div class="user-label">
                            {{ state.getters.get_user_profile.u_email }}
                        </div>
                    </el-descriptions-item>
                </el-descriptions>
            </el-col>
            <el-col :span="6">
                <div class="grid-content ep-bg-purple-light" />
            </el-col>
        </el-row>
        <el-row>
            <el-col :span="6">
                <div class="grid-content ep-bg-purple" />
            </el-col>
            <el-col :span="12">
                <div class="grid-content ep-bg-purple-light" />
                <div id="detail-header">
                    Wish List
                    <div id="wish-list">
                        <swiper :slides-per-view="3" :space-between="30" :autoplay="autoplay">
                            <swiper-slide v-for="item in state.getters.get_user_profile.u_wishlist">
                                <MovieCard :tcejbo="item"></MovieCard>
                            </swiper-slide>
                        </swiper>
                    </div>
                </div>
            </el-col>
            <el-col :span="6">
                <div class="grid-content ep-bg-purple-light" />
            </el-col>
        </el-row>
        <el-row><br></el-row>
        <el-row>
            <el-col :span="6">
                <div class="grid-content ep-bg-purple" />
            </el-col>
            <el-col :span="12">
                <div class="grid-content ep-bg-purple-light" />
                <el-collapse :accordion=true v-model="activeNames" @change="handleChange">
                    <el-collapse-item title="Ban List" name="1">
                        <el-table :data="state.getters.get_user_profile.u_banned_list">
                            <el-table-column label="User's Name" width="180">
                                <template #default="scope">
                                    <span>
                                        <a class="link-href" :href='update_url(scope.row.u_id).value'>
                                            {{ scope.row.u_username }}
                                        </a>
                                    </span>
                                </template>
                            </el-table-column>

                            <el-table-column align="right">
                                <template #default="scope">
                                    <el-button id="delect-button" size="small" type="primary"
                                        @click="handleDelete(scope.$index, scope.row)">Delete</el-button>
                                </template>
                            </el-table-column>
                        </el-table>
                    </el-collapse-item>
                </el-collapse>
            </el-col>
            <el-col :span="6">
                <div class="grid-content ep-bg-purple-light" />
            </el-col>
        </el-row>
        <el-row><br></el-row>
    </div>
</template>

<script lang="ts">
import { AxiosError } from 'axios';
import { ref, defineComponent, reactive } from 'vue'
import { ElMessage } from 'element-plus';
import {
    api_get_user,
    api_change_user_avatar,
    api_change_user_notif_status,
    api_change_user_remove_ban_status
} from '../api/service';
import UserDetail from '../components/UserDetail.vue'
import { useStore } from 'vuex'
import UserAvatar from '../components/UserAvatar.vue'
import SwiperCore, { Autoplay } from "swiper"
import { BanObject, UserObject } from '../types'
import 'swiper/css';
import { Swiper, SwiperSlide } from 'swiper/vue';
import MovieCard from '../components/MovieCard.vue';

SwiperCore.use([Autoplay])

export default defineComponent({
    name: "Profile",
    props: {},
    components: { UserDetail, UserAvatar, MovieCard, Swiper, SwiperSlide },
    setup: function () {
        const state = useStore();
        const error_message = ref();
        const change_data_obj = reactive({
            u_token: "",
            u_data: ""
        })

        const remove_banned_user_obj = reactive({
            u_token: "",
            banned_u_id: ""
        })
        const percentage = ref<number>();
        const user_obj = ref<UserObject>();

        const imgUrl = reactive({
            u_data: null
        })

        const onStatus = async () => {
            try {
                change_data_obj.u_token = state.getters.get_user.u_token
                change_data_obj.u_data = state.getters.get_user_profile.u_notification
                let res = await api_change_user_notif_status(change_data_obj)
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
                let res = await api_get_user(state.getters.get_user)
                state.commit("attach_user_profile", res.data)
                percentage.value = state.getters.get_user_profile.u_exp / 2500 * 100
                user_obj.value = res.data;
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
        const dialogTableVisible = ref(false)

        const handleDelete = async (index: number, row: BanObject) => {
            try {
                remove_banned_user_obj.u_token = state.getters.get_user.u_token
                remove_banned_user_obj.banned_u_id = row.u_id
                let res = await api_change_user_remove_ban_status(remove_banned_user_obj)
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

        const activeNames = ref(['0'])
        const handleChange = (val: string[]) => {
            console.log(val)
        }

        const update_url = (u_id: string) => {
            let dynamic_url = ref<string>("")
            dynamic_url.value = "/profile/" + u_id
            return dynamic_url
        }

        return {
            get_current_user,
            state,
            dialogTableVisible,
            change_data_obj,
            imgUrl,
            onStatus,
            user_obj,
            percentage,
            handleDelete,
            activeNames,
            handleChange,
            update_url,
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
    color: var(--main-color);
    float: left;
}

.user_detail {
    background-color: #040714;
}

.profile-title {
    text-align: center;
    color: #ffffff;
}

#col_shape {
    padding: 0 400px;
}

#critic_color {
    color:#F9F9F9 !important
}

#switch_on_color {
    --el-switch-on-color: #0063E5;
}

#label_title {
    padding: 0 400px
}

.link-href {
    font-size: 1rem;
    color: #ffffff;
    text-decoration: none;
    display: inline-block;
}

.link-href:hover {
    color: #0063E5;
}

.el-progress-bar__inner {
    background-color: #0063E5 !important;
}

.user-label {
    width: 80px;
    color: #ffffff;
}

.user_name {
    display: flex !important;
    align-items: center !important;
}

.el-descriptions__body {
    background-color: transparent !important;
    box-shadow: none;
}

.el-descriptions__label:not(.is-bordered-label) {
    color: #ffffff !important;
    margin-right: 16px;
}

.el-table:not(.el-table--border) .el-table__cell {
    background-color: #1A1D29;
}

.el-table--enable-row-hover .el-table__body tr:hover>td.el-table__cell {
    background-color: #1A1D29 !important;
}

.el-table td.el-table__cell,
.el-table th.el-table__cell.is-leaf {
    border-bottom: 0ch !important;
    --el-table-border: none;
}

.el-collapse-item__header {
    font-weight: 700 !important;
    border-bottom: null !important;
}

.el-collapse {
    --el-fill-color-blank: #040714 !important;
    --el-text-color-primary: #0063E5 !important;
    --el-collapse-header-font-size: 1.2rem !important;
    --el-collapse-border-color: none !important;
}

.el-collapse-item {
    font-size:1.2rem !important
}

.el-table {
    width: 100% !important;
    background-color: #1A1D29 !important;
    color: #F9F9F9 !important;
}

.el-table-column {
    color: #F9F9F9 !important;
}

.el-table thead {
    color: #f9f9f9 !important;
}

#edit-button {
    color: #f9f9f9;
    background-color: #30333e;
}

#delect-button {
    color: #f9f9f9;
    background-color: #30333e;
}

.el-table__inner-wrapper::before {
    height: 0px !important
}

.el-progress-bar__innerText {
    color: #ffffff !important
}

.el-progress-bar__outer {
    width: 370px;
    background-color: #31343E !important
}

#wish-list {
    margin-top: 30px;
}
</style>
