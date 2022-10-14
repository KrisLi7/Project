<template>
    <div id="actor-detail">
        <div class="container">
            <!-- <img :src="page_data?.p_headshot" /> -->
            <div class="cover">
                <img :src="page_data?.p_headshot" width="200" />
            </div>
            <div class="hero">
                <div class="details">
                    <div class="title1">
                        {{ page_data?.p_name }}
                    </div>
                </div>
            </div>

            <div id="column1">
                <div class="detail-box-content">
                    <p class='inset'>
                    <div id="title-in">
                        <span> Name : </span>
                    </div>
                    <i class="bx bxs-star bx-spin"></i>
                    {{ page_data?.p_name }}
                    </p>

                    <p v-if="page_data?.p_nick_name != undefined && page_data?.p_nick_name.length > 0">
                    <div id="title-in">
                        <span> Nick Name : </span>
                    </div>
                    <i class="bx bxs-star bx-spin"></i>
                    {{ page_data?.p_nick_name }}
                    </p>

                    <p v-if="page_data?.p_birth_name != undefined && page_data?.p_birth_name.length > 0">
                    <div id="title-in">
                        <span> Birth Name : </span>
                    </div>
                    <i class="bx bxs-star bx-spin"></i>
                    {{ page_data?.p_birth_name }}
                    </p>

                    <p v-if="page_data?.p_height != undefined && page_data?.p_height.length > 0">
                    <div id="title-in">
                        <span> Height : </span>
                    </div>
                    <i class="bx bxs-star bx-spin"></i>
                    {{ page_data?.p_height }}
                    </p>

                    <p v-if="page_data?.p_akas != undefined && page_data?.p_akas.length > 0">
                    <div id="title-in">
                        <span> AKAS : </span>
                    </div>
                    <i class="bx bxs-star bx-spin"></i>
                    {{ page_data?.p_akas }}
                    </p>
                </div>
            </div> <!-- end column1 -->

            <div id="column2">
                <div id="detail-header">
                    Personal Profile
                </div>
                <br>
                <div v-if="page_data?.p_bio_expand" class="profile-content">
                    <div v-if="bio_expand_obj.is_bio_expand">
                        {{ biography_obj.biography }}
                        <br>
                        <div class="bio-bottom">
                            <el-button type="primary" @click="bio_expand_obj.is_bio_expand = false">
                                Shrink Bio
                            </el-button>
                        </div>
                    </div>
                    <div v-else>
                        {{ page_data?.p_biography }}
                        <br>
                        <div class="bio-bottom">
                            <el-button class="bio-bottom" type="primary" @click="expand_bio">
                                See Full Bio
                            </el-button>
                        </div>
                    </div>
                </div>
                <div v-else class="profile-content">
                    {{ page_data?.p_biography }}
                </div>
                <br>
                <div id="detail-header">
                    Highest Related Moives
                    <br>
                    <swiper :slides-per-view="3" :space-between="30" :autoplay="autoplay">
                        <swiper-slide v-for="item in page_data?.p_filmography">
                            <MovieCard :tcejbo="item"></MovieCard>
                        </swiper-slide>
                    </swiper>
                </div>
                <br>
            </div>
        </div>
    </div>
</template>


<script lang="ts">
import { AxiosError } from "axios"
import { ElMessage } from "element-plus"
import { ref, defineComponent, reactive } from "vue"
import { useRoute } from "vue-router"
import { api_get_target_actor, api_expand_bio } from "../api/service"
import { ActorObject } from "../types"
import SwiperCore, { Autoplay } from "swiper"
import "boxicons"
import Link from "../components/Link.vue"
import MovieCard from "../components/MovieCard.vue"
import { Swiper, SwiperSlide } from 'swiper/vue'
import Review from '../components/review/Review.vue'

SwiperCore.use([Autoplay])

export default defineComponent({
    name: "ActorDetail",
    props: {
        tcejbo: Object as () => any
    },
    components: {
        Link, MovieCard,
        Swiper,
        SwiperSlide,
        Review
    },
    setup: function (props: any) {
        const bio_expand_obj = reactive ({
            is_bio_expand: false
        })

        const biography_obj = reactive ({
            biography: ""
        })

        const error_message = ref()

        const route = useRoute();

        const page_object = ref({
            p_id: route.params.p_id
        })

        const page_data = ref<ActorObject>()

        const fetch_data = async () => {
            try {
                let res = await api_get_target_actor(page_object.value)
                page_data.value = res.data
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

        const expand_bio = async () => {
            try {
                let res = await api_expand_bio(page_object.value)
                biography_obj.biography = res.data.p_biography
                bio_expand_obj.is_bio_expand = true
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

        const shrink_bio = async () => {
            bio_expand_obj.is_bio_expand = false
        }

        return {
            bio_expand_obj,
            biography_obj,
            page_data,
            page_object,
            fetch_data,
            shrink_bio,
            expand_bio,
            autoplay: {
                delay: 5000
            },
        }
    },
    created() {
        this.$watch(
            () => this.$route.params,
            () => {
                this.fetch_data()
            },
            { immediate: true }
        )
    }
})

</script>

<style lang="less">

#actor-detail {
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

    padding: 190px 0 0 280px;

    .title1 {
        color: white;
        font-size: 50px;
        margin-bottom: 20px;
        position: relative;
    }
}

#column1 {
    padding-left: 35px;
    padding-top: 120px;
    width: 220px;
    float: left;
    text-align: left;
}

#column2 {
    padding-left: 40px;
    padding-right: 10px;
    padding-top: 20px;
    margin: 10px, 10px;
    width: 700px;
    float: left;
}

#detail-header {
    margin-left: 5px;
    text-align: Left;
    font-size: 1.2rem;
    font-weight: 700;
    // text-transform: uppercase;
    color: #000;
    float: left;
}

.detail-box-content {
    margin-left: 1px;
    text-align: Left;
    margin-top: 10px;
    font-size: 0.5rem;
}

.bio-bottom {
    margin-top: 10px;
    text-align: center;
    align-content: center;
}

#title-in {
    font-weight: bold;
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
</style>