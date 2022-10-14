<template>
    <div class="message-notify-div">
        <el-icon @click="switch_drawer" id="message-icon" :size="30">
            <Message />
        </el-icon>
    </div>
    <el-drawer v-model="drawer" title="Message Box" :direction="direction" :before-close="handleClose">
        <MessageList :tcejbo="message_list['message_list']"></MessageList>
    </el-drawer>
</template>

<script lang="ts" setup>
import { onMounted, ref } from 'vue'
import { Message } from '@element-plus/icons-vue'
import MessageList from './MessageList.vue';
import { api_message_collect } from '@/api/service';
import { ElMessage } from 'element-plus';
import { AxiosError } from 'axios';

const props = defineProps({
    u_token: {
        type: String,
        require: true
    }
})

const drawer = ref(false)

const direction = ref('ltr')

const switch_drawer = () => {
    drawer.value = !drawer.value
}

const handleClose = (done: () => void) => {
    drawer.value = false
}

const message_list = ref()

const error_message = ref()

const get_user_message = async () => {
    try {
        let result = await api_message_collect({ "u_token": props.u_token })
        console.log(result.data)
        message_list.value = result.data
    } catch (e) {
        let error = e as AxiosError
        console.log(error)
        error_message.value = error.response?.data
        ElMessage({
            showClose: true,
            message: "Oops, " + error_message.value,
            type: "error",
        })
    }
}

onMounted(() => {
    console.log("abs")
    get_user_message()
})
</script>

<style lang="less">
.message-notify-div {
    align-items: center;
    margin: 10px 5px;
    padding-left: 20px;
}

.message-item {
    margin-top: 10px;
    margin-right: 35px;
}

#message-icon:hover {
    color: red;
}

.el-drawer {
    background-color: #040714 !important
}

</style>