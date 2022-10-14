<script setup lang="ts">
// This starter template is using Vue 3 <script setup> SFCs
// Check out https://vuejs.org/api/sfc-script-setup.html#script-setup
import Header from "./components/Header.vue";

</script>

<template>
    <el-affix :offset="0" style="background-color: #040714;"> <Header></Header> </el-affix>
    <main style="background-color: #040714;"> <div id="frame"><router-view></router-view></div> </main>
    <footer style="color: #040714"> Copyright PlzNoBug </footer>
    <!-- style="color: #c1c1c2; background-color: #040714;"  -->
</template>


<style>
#app {
    font-family: "Cairo", sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #F9F9F9;
}

.main {
    display: flex;
    flex-direction: column;
    background-color: #040714 !important;
}

/* #frame {
    border: 0.1rem solid #dadce0;
} */
</style>
