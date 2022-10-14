<template>
    <a :href="dynamic_url">
        <div class="movie-card">
            <div v-if="is_empty_poster"> <img src="../assets/not_found.png" /> </div>
            <div v-else><img :src="tcejbo?.m_poster" /></div>
            <div class="movie-card-content">
                <p class="movie-card-title"> {{ tcejbo?.m_title }} </p>
                <div class="movie-card-info">
                    <el-rate v-model="value" disabled text-color="red" score-template="{value}" />
                    {{ tcejbo?.m_imdb_rate }}
                </div>
                <p class="movie-card-info-2">
                    <el-rate class="movie-card-info-2" v-model="value_2" disabled text-color="red"
                        score-template="{value_2}" />
                    {{ tcejbo?.m_web_rate }}
                </p>
            </div>
        </div>
    </a>
</template>

<script lang="ts">
import axios from "axios"
import { ref, defineComponent, reactive } from "vue"
import { MovieCardObject } from "../types";

export default defineComponent({
    name: "MovieCard",
    props: {
        tcejbo: Object as () => MovieCardObject
    },
    setup: function (props) {
        const dynamic_url = "/movie/" + props.tcejbo?.m_id

        const default_src = "../assets/not_found.png"

        const is_empty_poster = ref<boolean>(false)

        const value = ref<Number | String>(0.25)

        const value_2 = ref<Number | String>(0.25)

        const preprocess = () => {
            if (props.tcejbo?.m_imdb_rate!) {
                value.value = props.tcejbo.m_imdb_rate / 2
            }
            if (props.tcejbo?.m_web_rate!) {
                value_2.value = props.tcejbo.m_web_rate
            }
            if (props.tcejbo?.m_poster!) {
                is_empty_poster.value = false
            } else {
                is_empty_poster.value = true
            }
        }

        return {
            dynamic_url,
            is_empty_poster,
            preprocess,
            default_src,
            value,
            value_2
        }
    },
    created: function () {
        this.$watch(
            () => this.is_empty_poster,
            () => {
                this.preprocess()
            },
            { immediate: true }
        )
    }
})
</script>

<style lang="less" scoped>
.movie-card {
    display: block;
    position: relative;
    overflow: hidden;
    padding-top: 140%;
    height: 300px;
    width: 200px;
    cursor: pointer;
    border-radius: 20px;
}

.movie-card img {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    transition: transform 0.3s linear;
}

/*
cursor scale up
*/

.movie-card:hover img {
    transform: scale(1.2);
}

.movie-card-content {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    padding: 5px;
    background-color: rgba(0, 0, 0, 0.8);
}

.movie-card-content::before {
    content: "";
    position: absolute;
    bottom: 100%;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(to top, rgba(0, 0, 0, 0.8), rgba(0, 0, 0, 0));
}

.movie-card-title {
    color: var(--text-color);
    font-size: 1.2rem;
    position: relative;
    font-weight: 600;
}

.movie-card-info {
    display: flex;
    align-items: center;
    flex-direction: row;
    font-size: 0.8rem;
    font-weight: 600;
    color: var(--text-color);
}

.movie-card-info-2 {
    display: flex;
    align-items: center;
    flex-direction: row;
    font-size: 0.8rem;
    font-weight: 600;
    color: var(--text-color);
    --el-rate-fill-color: #0063E5;
}


::v-deep(.el-rate__item) {
    display: flex;
}
</style>