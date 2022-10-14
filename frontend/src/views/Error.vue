<template>
    <br>
    <br>

    <el-row>
        <el-col :sm="900" :lg="900">
        <el-result
            icon="error"
            title="OOPS! PAGE NOT FIND"
            sub-title="We are working very very very hard to enrich our movie database"
        >
            <template #extra>
                <el-button type="primary" @click="home">Home Page</el-button>
            </template>
        </el-result>
        </el-col>
    </el-row>
</template>


<script lang="ts" setup>
import { ref, defineComponent, reactive } from "vue"
import router from "../router";

const active = ref(2)

const home = async ()  => {
    router.push('/home/')
}

</script>

<style>
/* #profile {
    display: flex;
    flex-direction: column;
} */
</style>

