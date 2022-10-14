<template>
    <div class="login">
        <h2 class="login-title color-main">Login Page</h2>

        <el-form class="form-rectangle" ref="ref_login_form" :model="login_object" :rules="input_rules">

            <el-form-item id="email" prop="u_email" class="login-input-rectangle">
                <el-input type="email" v-model="login_object.u_email" placeholder="Please input email" required />
            </el-form-item>

            <el-form-item id="password" prop="u_password" class="login-input-rectangle">
                <el-input type="password" v-model="login_object.u_password" placeholder="Please input password"
                    show-password @keyup.enter.native="submit_form(ref_login_form)"/>
            </el-form-item>

            <el-form-item class="sign-in-div">
                <el-link id="reset-password-link" type="primary" href="/password/request">
                    Forgot Password
                </el-link>
                <el-button id="sign-in-submit" type="primary" @click="submit_form(ref_login_form)">
                    Login
                </el-button>
            </el-form-item>
        </el-form>

        <div id="login-callout">
            <p> New to MovieFinder?
                <el-link id="sign-up-link" type="primary" href="/register">
                    Create an account
                </el-link>
            </p>
        </div>
    </div>
</template>

<script lang="ts">

import { AxiosError } from 'axios';
import { api_login, api_get_user } from "../api/service";
import { ref, defineComponent, reactive } from 'vue'
import { LoginObject } from "../types";
import type { FormInstance, FormRules } from 'element-plus'
import { ElMessage } from 'element-plus'
import { useStore } from 'vuex'
import router from '../router';
export default defineComponent({
    name: "Login",
    props: {},
    setup: function () {
        const stone = useStore()
        const ref_login_form = ref<FormInstance>()
        const error_message = ref()
        const login_object = ref<LoginObject>({
            u_email: "",
            u_password: ""
        })
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
        const submit_form = async (element: FormInstance | undefined): Promise<void> => {
            if (!element) { return }
            try {
                //await element.validate()
                let res = await api_login(login_object.value)
                stone.commit("attach_user", res.data)
                res = await api_get_user(stone.getters.get_user)
                stone.commit("attach_user_profile", res.data)
                ElMessage({
                    showClose: true,
                    message: "Congrats, Login Success",
                    type: "success",
                })
                router.push("/home")
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
            ref_login_form,
            error_message,
            login_object,
            input_rules,
            submit_form,
        };
    }
})
</script>

<style lang="less" scoped>

@--color-link-hover: #0063E5;

.login {
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

.login-title {
    text-align: center;
    color: #ffffff;
}

#reset-password-link {
    color: #ecf5ff;
    &.el-link:hover {
        color: @--color-link-hover;
    }
}

#sign-up-link {
    color: #ecf5ff;
    &.el-link:hover {
        color: @--color-link-hover;
    }
}


// style="color: #2700d7; text-decoration: underline"

.form-rectangle {
    display: flex;
    flex-direction: column;
    margin: 10px auto;
    text-align: center;
}

.login-input-rectangle {
    /* box-sizing: border-box; */
    /* position: absolute; */
    width: 540px;
    height: 40px;
    margin: 10px auto;
}

#sign-in-div {
    display: flex;
    flex-direction: row;
}

#sign-in-submit {
    display: flex;
    margin-left: auto;
}

#login-callout {
    padding: 16px 16px;
    color: #c1c1c2;
    text-align: center;
    border: 1px solid #30333e;
    border-radius: 6px;
    display: block;
    margin-block-start: 1em;
    margin-block-end: 1em;
    margin-inline-start: 0px;
    margin-inline-end: 0px;
    background-color: #30333e;
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

::v-deep(.el-link) {
    --el-link-hover-text-color: none;
}

::v-deep(.el-link.el-link--primary) {
    --el-link-text-color: none;
    --el-link-hover-text-color: none;
    --el-link-disabled-text-color: none;
}

::v-deep(.el-link:hover) {
    color: none;
}
</style>