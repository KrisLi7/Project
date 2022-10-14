<template>
    <div class="verify">
        <h2></h2>
        <el-form class="form-rectangle"  v-if="active == 1" >
            <el-sub-form-item class="verify-page" >
                <h1 class="verify-title color-main">Welcome!</h1>
                <br>
                <h2 class="verify-info color-main">You're almost there! We sent an email to </h2>
                <h2> {{stone.getters.get_email.u_email}} </h2>
                <br> <br>
                <h2> Just click on the link in that email to complete your signup.
                    If you don't see it, you may need to check your spam folder.
                </h2>
            </el-sub-form-item>
        </el-form>

        <el-sub-form class="form-rectangle"   v-if="active == 2" >
            <el-sub-form-item class="verify-page" >
                <h1 class="verify-title color-main" >Congrats!</h1>
                <br><br>
                <h2 class="verify-info color-main" >Your email is being verified.</h2>
                <br>
                <h2> You can now login with your account!
                </h2>
            </el-sub-form-item>
        </el-sub-form>

        <el-sub-form class="form-rectangle" v-if="active == 3" >
            <el-sub-form-item class="verify-page" >
                <h1 class="verify-title color-main">Oops!</h1>
                <br>
                <br>
                <h2 class="verify-info color-main">Your email verification is failed.</h2>
                <br>
                <h2> Verification link are only valid for 30 minutes, you may need to register again
                </h2>
            </el-sub-form-item>
        </el-sub-form>
    </div>
</template>

<script lang="ts">
import { AxiosError } from 'axios';
import { ElMessage } from 'element-plus'
import { ref, defineComponent, reactive } from "vue"
import { useStore } from 'vuex'
import { useRoute } from "vue-router"
import { api_get_user_register } from "../api/service"

export default defineComponent({
    name: "VerifyEmail",
    props: {
        tcejbo: {
            type: Object
        }
    },
    components: {},
    setup: function () {
        const stone = useStore();

        const active = ref(1);

        const error_message = ref()

        const route = useRoute();

        const id_object = ref({
            u_id: route.params.u_id
        })

        const post_data = async () => {
            try {
                if (route.params.u_id == null) {
                    active.value = 1
                } else {
                    await api_get_user_register(id_object.value)
                    active.value = 2
                }
            } catch (e) {
                active.value = 3
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
            stone,
            active,
            post_data
        };
    },
    created() {
        this.$watch(
            () => this.$route.params,
            () => {
                this.post_data()
            },
            { immediate: true }
        )
    }
})
</script>

<style lang="less" scoped>
.verify {
    /* Rectangle */
    display: flex;
    flex-direction: column;
    width: 100%;
    height: 100%;
    display: flex;
    box-sizing: border-box;
    margin: 20px auto;
    background-color: #040714 !important;
    color: #f9f9f9;
    /* border: 1px solid rgba(0, 0, 0, 0.5); */
    box-shadow: var(--el-box-shadow);
}
.form-rectangle {
    display: flex;
    flex-direction: column;
    margin: 20px auto;
}

.verify-title {
    text-align: center;
    font-size: 3em;
    color: #f9f9f9;
}

.verify-info {
    text-align: center;
    font-size: 1.5em;
    color: #f9f9f9;
}
</style>