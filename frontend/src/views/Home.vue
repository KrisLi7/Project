
<template>
<div id="home">
    <Carousel title="TOP MOVIES" :tcejbo="movie_items"></Carousel>

    <Carousel title="Recommend MOVIES" :tcejbo="recommend_items"></Carousel>

    <Carousel title="New Movies" :tcejbo="new_items"></Carousel>

    <Carousel title="Action Movies" :tcejbo="action_items"></Carousel>

    <Carousel title="Adventure Movies" :tcejbo="adventure_items"></Carousel>

    <Carousel title="Comedy Movies" :tcejbo="comedy_items"></Carousel>

    <Carousel title="Sci-fi Movies" :tcejbo="scifi_items"></Carousel>

    <Carousel title="Crime Movies" :tcejbo="crime_items"></Carousel>
</div>
</template>

<script lang="ts">
// @ is an alias to /src
import { useStore } from 'vuex'
import { ref, defineComponent, reactive } from "vue"
import { MovieCardObject } from "../types"
import { api_home_page_movie } from '../api/service_search'
import { AxiosError } from 'axios'
import { ElMessage } from 'element-plus'
import Carousel from '../components/Carousel.vue'

export default defineComponent({
    name: "Home",
    props: {
        tcejbo: Object
    },
    components: {
        Carousel
    },
    setup: function (props: any) {

        const state = useStore()

        const error_message = ref()

        const movie_items = ref<MovieCardObject[]>()

        const new_items = ref<MovieCardObject[]>()

        const action_items = ref<MovieCardObject[]>()

        const adventure_items = ref<MovieCardObject[]>()

        const comedy_items = ref<MovieCardObject[]>()

        const scifi_items = ref<MovieCardObject[]>()

        const crime_items = ref<MovieCardObject[]>()

        const recommend_items = ref<MovieCardObject[]>()

        const get_home_page_movie = async (): Promise<void> => {
            try {
                let u_id = state.getters.get_user.u_id
                let res = await api_home_page_movie({"u_id": u_id})
                movie_items.value = res.data["items"]
                new_items.value = res.data["New"]
                action_items.value = res.data["Action"]
                adventure_items.value = res.data["Adventure"]
                comedy_items.value = res.data["Comedy"]
                scifi_items.value = res.data["Sci-fi"]
                crime_items.value = res.data["Crime"]
                recommend_items.value = res.data["Recommend"]
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
            state,
            movie_items,
            new_items,
            action_items,
            adventure_items,
            comedy_items,
            scifi_items,
            crime_items,
            recommend_items,
            get_home_page_movie,
        }
    },
    created() {
        this.$watch(
            () => this.$route.params,
            () => {
                this.get_home_page_movie()
            },
            { immediate: true }
        )
    }
})
</script>

<style lang="less">
#home {
    background-color: var(--background-color);
}

#section {
    background-color: var(--background-color);
    padding: 60px;
    margin: auto;
    width: 95%;
}

#section-header {
    padding-top: var(60px);
    margin-bottom: 30px;
    padding-left: 20px;
    text-transform: uppercase;
    font-size: 1.5rem;
    font-weight: 700;
    border-left: 4px solid var(--main-color);
    display: flex;
    align-items: center;
    color: var(--text-color);
}

</style>
