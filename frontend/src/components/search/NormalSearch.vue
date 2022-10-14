<template>
    <el-form class="search-rectangle" ref="ref_normal_search_form" :model="normal_search_object" :rules="input_rules"
        @submit.native.prevent>
        <el-form-item id="normal_search_form" prop="keyword" class="search-input-rectangle">
        <div @keydown.stop>
            <el-input
                id="header_search" v-model="normal_search_object.keyword"
                placeholder="Search Keyword"
                :prefix-icon="Search"
                @keyup.enter.native="submit_form(ref_normal_search_form)"
            >
            </el-input>
        </div>
        </el-form-item>
        <el-form-item class="form-button">
            <el-button type="primary" class="form-button" :icon="Search" @click="submit_form(ref_normal_search_form)"></el-button>
        </el-form-item>
    </el-form>
</template>

<script lang="ts">
import { AxiosError } from "axios"
import { ref, defineComponent, reactive } from "vue"
import type { FormInstance, FormRules } from 'element-plus'
import { api_movie_home_search } from "../../api/service_search"
import { Search, Loading } from '@element-plus/icons-vue'
import { SearchMovieReturnObject } from "../../types"
import { useStore } from 'vuex'
import router from "../../router"

export default defineComponent({
    name: "NormalSearch",
    props: {
        tcejbo: Object
    },
    setup: function (props: any, { emit }) {
        const stone = useStore()

        const ref_normal_search_form = ref<FormInstance>()

        const normal_search_object = ref({
            keyword: ""
        })

        const normal_search_success = ref<boolean>(false)

        const success_message = ref<SearchMovieReturnObject[]>()

        const error_message = ref()

        const input_rules = reactive<FormRules>({
            keyword: [
                {
                    required: true,
                    message: "Keyword should not empty",
                    trigger: 'blur'
                }
            ]
        })

        const submit_form = async (element: FormInstance | undefined): Promise<void> => {
            // alert("click")
            if (!element) { return }
            try {
                await element.validate()
                let res = await api_movie_home_search(normal_search_object.value)
                success_message.value = res.data["items"]
                normal_search_success.value = true
                stone.commit("attach_result", success_message.value)
                router.push("/search")
            } catch (e) {
                let error = e as AxiosError
                error_message.value = error.response?.data
                normal_search_success.value = false
            }
        }

        return {
            Search,
            ref_normal_search_form,
            normal_search_object,
            input_rules,
            normal_search_success,
            submit_form,
            success_message,
            error_message,
        };
    }
})
</script>

<style>
.search-rectangle {
    display: flex;
    flex-direction: row;
}

.search-input-rectangle {
    width: 200px;
}

.form-button {
    background-color: #0063E5;
    /* border: #0063E5; */
}
</style>
