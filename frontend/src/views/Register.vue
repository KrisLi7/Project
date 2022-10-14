<template>
    <div class="register">
        <h2 class="register-title color-main">Register Page</h2>
        <el-form class="form-rectangle" ref="ref_register_form" :model="register_object" :rules="input_rules">

            <el-form-item id="username" prop="u_username" class="register-input-rectangle">
                <el-input type="username" v-model="register_object.u_username" placeholder="Username" required />
            </el-form-item>

            <el-form-item id="email" prop="u_email" class="register-input-rectangle">
                <el-input type="email" v-model="register_object.u_email" placeholder="Email Address" required />
            </el-form-item>

            <el-form-item id="password" prop="u_password" class="register-input-rectangle">
                <el-input type="password" v-model="register_object.u_password" placeholder="Create Password"
                    show-password @keyup.enter.native="submit_form(ref_register_form)"/>
            </el-form-item>

            <el-form-item class="form-button-div">
                <el-button type="primary" class="form-button" @click="submit_form(ref_register_form)"> Register
                </el-button>
                <el-button type="primary" class="form-button" @click="reset_form(ref_register_form)"> Clear </el-button>
            </el-form-item>

        </el-form>
    </div>
</template>

<script lang="ts">
import { api_register } from "../api/service";
import { ref, defineComponent, reactive } from "vue"
import { ErrorObject, RegisterObject, CurrentEmailObject } from "../types";
import type { FormInstance, FormRules } from 'element-plus'
import { useStore } from 'vuex'
import { AxiosError } from 'axios';
import { ElMessage } from 'element-plus'
import router from "../router";


export default defineComponent({
    name: "Register",
    props: {},
    setup: function () {
        const stone = useStore()
        const ref_register_form = ref<FormInstance>()
        const error_message = ref()

        const register_object = ref<RegisterObject>({
            u_username: "",
            u_email: "",
            u_password: ""
        })

        const input_rules = reactive<FormRules>({
            u_username: [
                {
                    required: true,
                    message: "Please input username",
                    trigger: 'blur'
                },
                {
                    min: 5,
                    max: 30,
                    message: "5 ~ 30",
                    trigger: 'blur'
                }
            ],
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
            ],
            u_password: [
                {
                    required: true,
                    message: "Please input password",
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

        const reset_form = (element: FormInstance | undefined) => {
            element?.resetFields()
        }

        const submit_form = async (element: FormInstance | undefined): Promise<void> => {
            if (!element) { return }
            try {
                let res = await api_register(register_object.value)
                stone.commit("attach_email", res.data)
                ElMessage({
                    showClose: true,
                    message: "Congrats, Welcome Movie Finder",
                    type: "success",
                })
                router.push("/verify/email")
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
            ref_register_form,
            register_object,
            input_rules,
            reset_form,
            submit_form,
        }
    },
    watch: {},
    computed: {},
})

</script>

<style lang="less" scoped>
.register {
    /* Rectangle */
    display: flex;
    flex-direction: column;
    width: 100%;
    height: 100%;
    display: flex;
    place-items: center;
    box-sizing: border-box;
    // margin: 10px auto;
    // background: #1a1d29;
    /* border: 1px solid rgba(0, 0, 0, 0.5); */
    box-shadow: var(--el-box-shadow);
}

.register-title {
    text-align: center;
    color: #FFFFFF;
}

.form-rectangle {
    display: flex;
    flex-direction: column;
    margin: 10px auto;
    text-align: center;
}

.register-input-rectangle {
    /* box-sizing: border-box; */
    /* position: absolute; */
    width: 540px;
    height: 40px;
    margin: 10px auto;
    background: #000000;
    /* border: 1px solid rgba(0, 0, 0, 0.5); */
}

.form-button-div {
    margin-left: auto;
}

.form-button {
    background-color: #2700d7;
    border: #2700d7;
}

#sign-up-submit {
    display: flex;
    margin-left: auto;
}

::v-deep(.el-input__wrapper) {
    background: #30333e !important;
    box-shadow: none;
    padding: 0px;
}

::v-deep(.el-input__inner) {
    line-height: 0px;
    padding: 11px;
    margin: 0px;
    background: transparent;
    border-radius: 4px;
}
</style>