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

    <div class="password-reset">
        <h2></h2>
        <h2 class="reset-title color-main">Password Reset Page</h2>

        <el-form class="form-rectangle" ref="ref_reset_form" :model="reset_object" :rules="input_rules">
            <el-form-item id="reset_code" prop="u_reset_code" class="reset-input-rectangle">
                <el-input v-model="reset_object.u_reset_code" placeholder="Please input reset verification code" required />
            </el-form-item>

            <el-form-item id="password" prop="u_password" class="reset-input-rectangle">
                <el-input type="password" autocomplete="off" v-model="reset_object.u_password"
                    placeholder="Please input new password" show-password />
            </el-form-item>

            <p></p>

            <el-form-item class="form-button">
                <el-button type="primary" @click="submit_form(ref_reset_form)"> Password Reset </el-button>
            </el-form-item>

        </el-form>
    </div>
</template>

<script lang="ts">
import Debug from "../components/Debug.vue"
import { api_password_reset } from "../api/service";
import { ref, defineComponent, reactive } from "vue"
import { ResetObject } from "../types";
import type { FormInstance, FormRules } from 'element-plus'
import { ElMessage } from 'element-plus'
import { AxiosError } from 'axios';
import router from "../router";

export default defineComponent({
    name: "ResetPassword",
    props: {},
    components: {},
    setup: function () {
        const error_message = ref()
        const reset_object = ref<ResetObject>({
            u_password: "",
            u_reset_code: ""
        })
        const ref_reset_form = ref<FormInstance>()
        const input_rules = reactive<FormRules>({
            u_reset_code: [
                {
                    required: true,
                    message: "Please input reset verification code",
                    trigger: 'blur'
                }
            ],
            u_password: [
                {
                    required: true,
                    message: "Please input new password",
                    trigger: 'blur'
                },
                { // const weak_regex : RegExp = /^[\w]{6,16}$/g;
                    min: 6,
                    max: 16,
                    message: "6 ~ 16",
                    trigger: 'blur'
                }
            ]
        })

   
        const submit_form = async (element: FormInstance | undefined): Promise<void> => {
            if (!element) { return }
            try {
                await api_password_reset(reset_object.value)
                ElMessage({
                    showClose: true,
                    message: "Congrats, your password is reset",
                    type: "success",
                })
                router.push('/success')
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

        const active = ref(1)

        const next = () => {
        if (active.value++ > 2) active.value = 0
        }

        return {
            ref_reset_form,
            reset_object,
            input_rules,
            submit_form,
            active
        }
    }
})
</script>


<style lang="less" scoped>
.password-reset {
    /* Rectangle */
    display: flex;
    flex-direction: column;
    width: 100%;
    height: 100%;
    display: flex;
    place-items: center;
    box-sizing: border-box;
    margin: 10px auto;
    background: #000000;
    /* border: 1px solid rgba(0, 0, 0, 0.5); */
    box-shadow: var(--el-box-shadow);
}

.reset-title {
    text-align: center;
    color: #FFFFFF;
}

.form-rectangle {
    display: flex;
    flex-direction: column;
    margin: 10px auto;
    text-align: center;
}

.reset-input-rectangle {
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