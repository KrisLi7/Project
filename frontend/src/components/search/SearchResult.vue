<template>
    <div id="search-result">
        <div class="infinite-list" v-infinite-scroll="on_scroll_load" infinite-scroll-distance='1'>
            <div class="infinite-list-item" v-for="item in stack">
                <MovieCard :tcejbo="item"></MovieCard>
            </div>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { ref, watch } from "vue"
import { MovieCardObject } from "../../types";
import MovieCard from "../MovieCard.vue";

const props = defineProps({
    tcejbo: {
        type: Array<MovieCardObject>,
        default: [],
        require: true
    }
})

watch(() => props.tcejbo, (val, old) => {
    pos.value = 20
    stack.value = val.slice(0, pos.value)
});

const pos = ref<number>(10)

const stack = ref<Array<MovieCardObject>>([])

const on_scroll_load = () => {
    pos.value += 10
    stack.value = props.tcejbo.slice(0, pos.value)
}
</script>

<style lang="less">
#search-result {
    display: flex;
    flex-wrap: wrap;
}

.infinite-list {
    display: flex;
    flex-wrap: wrap;
    // height: 300px;
    // overflow: auto
}

.infinite-list-item {
    flex: 0 1 200px;
    margin: 5px auto;
}
</style>
