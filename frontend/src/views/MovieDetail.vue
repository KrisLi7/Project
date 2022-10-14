<template>
    <div id="movie-detail">

        <div class="container">
            <div class="cover">
                <img :src="page_data.m_poster" width="200" />
            </div>
            <div class="hero">
                <div class="details">
                    <div class="title1">
                        {{ page_data.m_title }}
                    </div>
                </div>
            </div>

            <div id="column1">
                <div class="detail-box-content">
                    <p class='inset'>
                    <div id="title-in">
                        <span> IMDB RATE : </span>
                    </div>
                    <i class="bx bxs-star bx-spin"></i>
                    {{ page_data.m_imdb_rate }}
                    </p>

                    <p>
                    <div id="title-in">
                        <span> RATE From WEB : </span>
                    </div>
                    <i class="bx bxs-star bx-spin"></i>
                    {{ page_data.m_web_rate }}
                    </p>

                    <p>
                    <div id="title-in">
                        <span> RATE From CRITICS : </span>
                    </div>
                    <i class="bx bxs-star bx-spin"></i>
                    {{ page_data.m_critic_web_rate }}
                    </p>

                    <p>
                    <div id="title-in">
                        <span> GENRES : </span>
                    </div>
                    <i class="bx bxs-star bx-spin"></i>
                    {{ page_data.m_genre }}
                    </p>

                    <p>
                    <div id="title-in">
                        <span> RELEASE DATE : </span>
                    </div>
                    <i class="bx bxs-star bx-spin"></i>
                    {{ page_data.m_year }}
                    </p>

                    <p>
                    <div id="title-in">
                        <span> DIRECTOR : </span>
                    </div>

                    <p>
                    <div v-for="i in page_data.m_director">
                        <Link :tcejbo="i" />
                    </div>
                    </p>
                    </p>

                    <p>
                    <div id="title-in">
                        <p> FAVORITE : </p>
                    </div>
                    <el-button v-if="is_in_wishlist_obj.u_is_in_wishlist" type="primary" :icon="Star" circle
                        @click="add_or_remove_wishlist" />
                    <el-button v-else :icon="Star" circle @click="add_or_remove_wishlist" />
                    </p>

                </div>
            </div>

            <div id="movie-column-2">
                <el-tabs id="el-tabs" v-model="activeName" @tab-click="handleClick">
                    <el-tab-pane label="OVERVIEW" name="first">
                        <h2 class="movie-infor-header"> DESCRIPTION </h2>
                        <div class="movie-detail-content-info"> {{ page_data.m_info }} </div>
                        <h2 class="movie-infor-header"> STARS </h2>
                        <div class="movie-detail-content">
                            <swiper :slides-per-view="3" :space-between="30" :autoplay="autoplay">
                                <swiper-slide v-for="i in page_data.m_star">
                                    <StarLink :tcejbo="i" />
                                </swiper-slide>
                            </swiper>
                        </div>
                    </el-tab-pane>
                    <el-tab-pane label="CAST & CREWS" name="third">
                        <h2 class="movie-infor-header"> CAST & CREW </h2>
                        <div v-for="i in page_data.m_cast">
                            <Link :tcejbo="i" />
                        </div>
                    </el-tab-pane>
                    <el-tab-pane label="SIMILAR MOVIE" name="fourth">
                        <h2 class="movie-infor-header"> SIMILAR MOVIE </h2>
                        <div class="movie-detail-content">
                            <swiper :slides-per-view="3" :space-between="30" :autoplay="autoplay">
                                <swiper-slide v-for="item in page_data.m_similar">
                                    <MovieCard :tcejbo="item"></MovieCard>
                                </swiper-slide>
                            </swiper>
                        </div>
                    </el-tab-pane>
                    <el-tab-pane label="COMMENT" name="fifth">
                        <h2 class="movie-infor-header"> COMMENT </h2>
                        <div class="movie-detail-content">
                            <Review :m_id="page_data.m_id" :u_curr_obj="curr_user_obj"></Review>
                        </div>
                    </el-tab-pane>
                </el-tabs>
            </div>
        </div>
    </div>
</template>


<script lang="ts" setup>
import { AxiosError } from "axios"
import { ElMessage } from "element-plus"
import { ref, onMounted } from "vue"
import { useRoute } from "vue-router"
import {
    api_add_to_wishlist,
    api_get_target_movie,
    api_remove_from_wishlist,
    api_check_is_in_wish_list,
} from "../api/service_search"
import { CurrentUserObject, MovieObject } from "../types"
import Link from "../components/Link.vue"
import StarLink from "../components/StarLink.vue"
import 'boxicons'
import MovieCard from "../components/MovieCard.vue"
import { Swiper, SwiperSlide } from 'swiper/vue'
import SwiperCore, { Autoplay } from "swiper"
import 'swiper/css'
import Review from '../components/review/Review.vue'
import { useStore } from "vuex"
import type { TabsPaneContext } from 'element-plus'
import { Star } from '@element-plus/icons-vue'

SwiperCore.use([Autoplay])


const activeName = ref('first')
const handleClick = (tab: TabsPaneContext, event: Event) => {
    // console.log(tab, event)
}
const activeNames = ref(['1'])
const handleChange = (val: string[]) => {
    // console.log(val)
}
const state = useStore()
const route = useRoute()
const current_token = ref<string>(state.getters.get_user.u_token)

const is_in_wishlist_obj = ref({ u_is_in_wishlist: false })

const page_object = ref({
    m_id: route.params.m_id
})

const wishlist_object = ref({
    u_token: "",
    m_id: route.params.m_id
})

const page_data = ref<MovieObject>({
    m_id: route.params.m_id.toString(),
    m_title: "",
    m_info: "",
    m_poster: "",
    m_year: "",
    m_cast: [],
    m_director: [],
    m_imdb_rate: 0,
    m_web_rate: 0,
    m_country: "",
    m_language: "",
    m_genre: "",
    m_similar: [],
    m_star: [],
    m_critic_web_rate: 0
})

const curr_user_obj = ref<CurrentUserObject>({
    u_id: state.getters.get_user.u_token,
    u_username: state.getters.get_user.u_username,
    u_token: state.getters.get_user.u_token,
    u_is_login: 1
})

const fetch_data = async () => {
    try {
        let res = await api_get_target_movie(page_object.value)
        page_data.value = res.data
    } catch (e) {
        let error = e as AxiosError
        ElMessage({
            showClose: true,
            message: "Oops, " + error.response?.data,
            type: "error",
        })
    }
}

const check_is_in_wishlist = async () => {
    try {
        wishlist_object.value.u_token = state.getters.get_user.u_token
        let res = await api_check_is_in_wish_list(wishlist_object.value)
        is_in_wishlist_obj.value.u_is_in_wishlist = res.data
    } catch (e) {
        let error = e as AxiosError
        ElMessage({
            showClose: true,
            message: "Oops, " + error.response?.data,
            type: "error",
        })
    }
}

const add_or_remove_wishlist = async () => {
    try {
        let res
        wishlist_object.value.u_token = state.getters.get_user.u_token
        if (is_in_wishlist_obj.value.u_is_in_wishlist) {
            res = await api_remove_from_wishlist(wishlist_object.value)
        } else {
            res = await api_add_to_wishlist(wishlist_object.value)
        }
        check_is_in_wishlist()
        ElMessage({
            showClose: true,
            message: res.data.message,
            type: "success",
        })
    } catch (e) {
        let error = e as AxiosError
        ElMessage({
            showClose: true,
            message: "Oops, " + error.response?.data,
            type: "error",
        })
    }
}
const autoplay = {
    delay: 5000
}


onMounted(() => {
    fetch_data()
    check_is_in_wishlist()
})

</script>

<style lang="less">
#el-tabs {
    --el-text-color-primary: white;
}

#movie-detail {
    display: flex;
    flex-direction: column;
    background: var(--background-color) !important;
    font: "Cairo", sans-serif;
    line-height: 25px;
    // border: 1px solid #d0d7de;
}

.hero {
    height: 342px;
    margin: 0;
    position: relative;
    overflow: hidden;
    z-index: 1;
    border-top-left-radius: 5px;
    border-top-right-radius: 5px;
}

.hero:before {
    content: '';
    width: 100%;
    height: 100%;
    position: absolute;
    overflow: hidden;
    top: 0;
    left: 0;
    background: url("../assets/bg.jpg");
    z-index: -1;
    transform: skewY(-2.2deg);
    transform-origin: 0 0;
    opacity: 0.8;
}

.cover {
    position: absolute;
    top: 160px;
    left: 40px;
    z-index: 2;
    width: auto;
}

.details {

    padding: 100px 0 0 250px;

    .title1 {
        color: white;
        font-size: 55px;
        margin-bottom: 20px;
        position: relative;
        line-height: 60px;
        text-transform: uppercase;
        font-weight: 700;
    }
}

#column1 {
    padding-left: 35px;
    padding-top: 120px;
    width: 240px;
    float: left;
    text-align: LEFT;
    color: var(--text-color);
}

#movie-column-2 {
    display: flex;
    flex-direction: column;
    padding-left: 70px;
    padding-right: 5px;
    padding-top: 20px;
    margin: 10px 10px;
    width: 730px;
    height: auto;
    float: left;
    // color: var(--text-color);
}

.movie-detail-content-info {
    text-align: justify;
    color: var(--text-color);
    font-size: 18px;
    line-height: 30px;
}

.movie-infor-header {
    text-align: left;
    color: var(--main-color);
}

.movie-detail-content {
    text-align: left;
}

#detail-header {
    text-align: Left;
    font-size: 1.2rem;
    font-weight: 700;
    // text-transform: uppercase;
    color: var(--main-color);
    width: 100%;
    height: flex;
    float: left;
}

.detail-box-content {
    margin-left: 1px;
    text-align: Left;
    margin-top: 10px;
    font-size: 0.5rem;
    color: var(--text-color);
}

.profile-content {
    margin-left: 5px;
    text-align: justify;
    margin-top: 10px;
    color: var(--text-color);
}

.comment-content {
    text-align: justify;
    margin: 30px 0px 30px;
    font-size: 0.8rem;
    color: black;
}

#title-in {
    font-weight: bold;
    color: var(--text-color);
}

p.inset {
    border-style: inset;
    font-size: 1.0rem;
}

p.outset {
    border-style: outset;
}

p {
    font-size: 1.0rem;
}

#see-less {
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;

    -webkit-line-clamp: 17;
    -webkit0box-orient: vertical
}

#button-ws {
    border-radius: 50%;
    padding: 8px;
}
</style>