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

    <div class="passwordreset-request">
        <br>
        <br>
        <h2 class="request-title color-main">Confirm who you are</h2>

        <el-form class="form-rectangle" ref="ref_request_form" :model="request_object" :rules="input_rules">
            <el-form-item id="email" prop="u_email" class="request-input-rectangle">
                <el-input v-model="request_object.u_email" placeholder="Email Address" required />
            </el-form-item>

            <p></p>

            <el-form-item class="form-button">
                <el-button type="primary" @click="submit_form(ref_request_form)"> SEND ME THE PASSCODE </el-button>
            </el-form-item>

        </el-form>
    </div>
</template>

<script lang="ts">
import { api_password_reset_request } from "../api/service";
import { ref, defineComponent, reactive } from "vue"
import { RequestResetObject } from "../types";
import type { FormInstance, FormRules } from 'element-plus'
import { ElMessage } from 'element-plus'
import { AxiosError } from 'axios';
import router from "../router";

export default defineComponent({
    name: "RequestResetPassword",
    props: {},
    components: {},
    setup: function () {
        const error_message = ref()
        const request_object = ref<RequestResetObject>({
            u_email: ""
        })

        const ref_request_form = ref<FormInstance>()

        const input_rules = reactive<FormRules>({
            u_email: [
                {
                    required: true,
                    message: "Please input email address",
                    trigger: 'blur'
                },
                {
                    type: "email",
                    message: "Not a valid email address",
                    trigger: 'blur'
                }
            ]
        })

        const submit_form = async (element: FormInstance | undefined): Promise<void> => {
            if (!element) { return }
            try {
                await api_password_reset_request(request_object.value)
                ElMessage({
                    showClose: true,
                    message: "Reset verification code is send to your email",
                    type: "success",
                })
                router.push('/password/reset')
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
        const active = ref(0)
        return {
            ref_request_form,
            request_object,
            input_rules,
            submit_form,
            active
        }
    }
})
</script>


<style lang="less" scoped>
.passwordreset-request {
    /* Rectangle */
    display: flex;
    flex-direction: column;
    width: 100%;
    height: 100%;
    display: flex;
    place-items: center;
    box-sizing: border-box;
    // margin: 10px auto;
    // background: #000000;
    /* border: 1px solid rgba(0, 0, 0, 0.5); */
    box-shadow: var(--el-box-shadow);
}

.request-title {
    text-align: center;
    color: #FFFFFF;
}

.form-rectangle {
    display: flex;
    flex-direction: column;
    margin: 10px auto;
    text-align: center;
}

.request-input-rectangle {
    /* box-sizing: border-box; */
    /* position: absolute; */
    width: 540px;
    height: 40px;
    margin: 10px auto;
    background: #000000;
    /* border: 1px solid rgba(0, 0, 0, 0.5); */
}

#input-email {
    background: #FFFFFF;
}

.form-button {
    display: flex;
    margin-left: auto;
}

.el-button {
    background-color: #0063E5 !important;
    border: #0063E5 !important;
}

#sign-up-submit {
    display: flex;
    margin-left: auto;
}

::v-deep(.el-input__wrapper) {
    background: #30333e !important;
    box-shadow: none;
}

::v-deep(.el-input__inner) {
    line-height: 38px;
    padding-left: 10px;
    padding-right: 0;
    background: transparent;
}
</style>