<template>
    <el-button id="edit-button" @click="changeData">
        edit
    </el-button>
</template>


<script lang="ts">
import { AxiosError } from 'axios';
import { ElMessage, ElMessageBox } from 'element-plus';
import { ref, defineComponent, reactive } from 'vue'
import {
    api_get_user,
    api_change_username,
    api_change_user_email,
    api_change_user_lastname,
    api_change_user_firstname,
} from '../api/service';
import { useStore } from 'vuex'

export default defineComponent({
    name: "UserDetail",
    props: {
        tcejbo: {
            type: String
        }
    },
    setup: function (props: any) {
        const error_message = ref();
        const state = useStore();
        const change_data_obj = reactive({
            u_token: "",
            u_data: ""
        })

        const get_current_user = async () => {
            try {
                let res = await api_get_user(state.getters.get_user)
                state.commit("attach_user_profile", res.data)
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

        const changeData = async () => {
            let res
            await ElMessageBox.prompt("Please enter your " + props.tcejbo.type, 'Tip', {
                confirmButtonText: 'OK',
                cancelButtonText: 'Cancel'
            }).then((result) => {
                change_data_obj.u_token = state.getters.get_user.u_token
                change_data_obj.u_data = ""
                if (result.value != null) {
                    change_data_obj.u_data = result.value
                }
            })
            try {
                if (props.tcejbo == "user name") {
                    res = await api_change_username(change_data_obj)
                } else if (props.tcejbo == "first name") {
                    res = await api_change_user_firstname(change_data_obj)
                } else if (props.tcejbo == "last name") {
                    res = await api_change_user_lastname(change_data_obj)
                } else {
                    res = await api_change_user_email(change_data_obj)
                }
                get_current_user()
                ElMessage({
                    showClose: true,
                    message: res.data.message,
                    type: "success",
                })
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
            changeData
        };
    },
})
</script>


<style>
#edit-button {
    color: white;
    background-color: #30333e;
}

.el-switch.is-checked .el-switch__core {
    background-color: #0063E5 !important
}
</style>

