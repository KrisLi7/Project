<template>
    <div class="search">
        <h2 class="search-title">Search Result</h2>
        <SearchResult :tcejbo="stone.getters.get_result['items']"></SearchResult>
    </div>
</template>

<script lang="ts" setup>
import { useStore } from 'vuex'
import SearchResult from "../components/search/SearchResult.vue"

const stone = useStore();
</script>

<style lang="less">
.search {
    background-color: var(--background-color);
}

.search-title {
    text-align: center;
    background-color: #040714;
    color: #F9F9F9 !important;
}
</style>



