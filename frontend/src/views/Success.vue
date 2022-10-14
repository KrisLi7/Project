<template>
    <br>
    <br>
    <el-steps :active="active" finish-status="success"  align-center>
        <el-step title="Confirm your identity" />
        <el-step title="Create your password" />
        <el-step title="You are Successful" />
    </el-steps>
    <br>
    <br>
    <el-row>
        <el-col :sm="900" :lg="900">
            <el-result
                icon="success"
                title="Success Tip"
                sub-title="Please follow the instructions"
            >
                <template #extra>
                    <el-button type="primary" @click="login">Login</el-button>
                </template>
            </el-result>
        </el-col>
    </el-row>
</template>


<script lang="ts" setup>
import { ref } from "vue"
import router from "../router";

const active = ref(2)
const login = async ()  => {
    router.push('/login/')
}
</script>

<style>
.el-result__subtitle p {
    color: #f9f9f9 !important;
}

.el-step__icon-inner {
    color: #040714!important;
}

.el-step__icon.is-text {
    border-color: #f9f9f9!important;
}

.el-button--primary {
    background-color: #0063E5 !important;
    border: #0063E5 !important;
    color: #f9f9f9 !important
}

</style>

