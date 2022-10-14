<template>
    <div id="section">
        <div id="section-header"> {{ title }} </div>
        <swiper :slides-per-view="5" :space-between="30" :autoplay="autoplay" :loop="true">
            <swiper-slide v-for="item in $props.tcejbo">
                <MovieCard :tcejbo="item"></MovieCard>
            </swiper-slide>
        </swiper>
    </div>
</template>

<script lang="ts">
import { ref, defineComponent, reactive } from "vue"
import { Swiper, SwiperSlide } from 'swiper/vue';
import SwiperCore, { Autoplay } from "swiper"
import 'swiper/css';
import { MovieCardObject } from "../types";
import MovieCard from "./MovieCard.vue";

SwiperCore.use([Autoplay])

export default defineComponent({
    name: "Carousel",
    props: {
        tcejbo: Object as () => MovieCardObject[],
        title: String
    },
    components: {
        Swiper,
        SwiperSlide,
        MovieCard
    },
    setup: function (props: any) {

        return {
            autoplay: {
                delay: 5000
            },
        };
    }
})
</script>


<style>
</style>