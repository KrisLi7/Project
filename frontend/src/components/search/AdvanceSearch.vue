<template>
    <div id="adv-search">
        <br>
        <h2 class="search-title">Advance Search</h2>
        <br>
        <div id = "ads-input">
                <el-form ref="ref_advance_search" :model="advance_form" label-width="120px">
                <el-form-item label="Title">
                    <el-input  v-model="advance_form.title" prop="title" />
                </el-form-item>
                <el-form-item label="Actor">
                    <el-input v-model="advance_form.actor" prop="actor" />
                </el-form-item>
                <el-form-item label="Director">
                    <el-input v-model="advance_form.director" prop="director" />
                </el-form-item>
                <el-form-item label="Country">
                    <el-select v-model="advance_form.country" prop="country" placeholder="Please Select Country">
                        <el-option label="All" value="All" />
                        <el-option label="China" value="China" />
                        <el-option label="Australia" value="Australia" />
                        <el-option label="United States" value="United States" />
                        <el-option label="Japan" value="Japan" />
                        <el-option label="South Korea" value="South Korea" />
                        <el-option label="France" value="France" />
                        <el-option label="United Kingdom" value="United Kingdom" />
                        <el-option label="Germany" value="Germany" />
                        <el-option label="Thailand" value="Thailand" />
                        <el-option label="Italy" value="Italy" />
                        <el-option label="Spain" value="Spain" />
                    </el-select>
                </el-form-item>
                <el-form-item label="Year">
                    <el-col :span="11">
                        <el-date-picker v-model="advance_form.year" type="year" placeholder="Pick a yaer"
                            style="width: 100%" prop="year" />
                    </el-col>
                </el-form-item>
                <el-form-item label="Include Adult" prop="r18">
                    <el-switch v-model="advance_form.r18" />
                </el-form-item>
                <el-form-item label="Genre">
                    <el-radio-group v-model="advance_form.genre" prop="genre">
                        <el-radio label="All" />
                        <el-radio label="Action" />
                        <el-radio label="Adventure" />
                        <el-radio label="Comedy" />
                        <el-radio label="Sci-Fi" />
                        <el-radio label="Documentary" />
                        <el-radio label="Short" />
                        <el-radio label="Horror" />
                        <el-radio label="Thriller" />
                        <el-radio label="Drama" />
                        <el-radio label="Crime" />
                        <el-radio label="Animation" />
                        <el-radio label="Family" />
                        <el-radio label="Music" />
                        <el-radio label="Fantasy" />
                        <el-radio label="Romance" />
                        <el-radio label="Mystery" />
                    </el-radio-group>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="submit_form(ref_advance_search)">Submit</el-button>
                    <el-button @click="reset_form(ref_advance_search)">Reset</el-button>
                </el-form-item>
            </el-form>
        </div>

    </div>

    <SearchResult :tcejbo="return_movie_items" ></SearchResult>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { MovieCardObject } from '../../types';
import { ElMessage, FormInstance, FormRules } from 'element-plus'
import { AxiosError } from 'axios';
import { api_movie_advance_search } from '../../api/service_search';
import SearchResult from './SearchResult.vue';

const ref_advance_search = ref<FormInstance>();

const advance_form = ref({
    title: "",
    actor: "",
    director: "",
    year: "",
    country: "",
    r18: false,
    genre: "",
})

const request_success = ref<boolean>(false)

const error_message = ref()

const return_movie_items = ref<Array<MovieCardObject>>([])

const is_show_result = ref<boolean>(true)

const submit_form = async (element: FormInstance | undefined): Promise<void> => {

    return_movie_items.value = []

    if (!element) { return }
    try {
        let res = await api_movie_advance_search(advance_form.value)
        return_movie_items.value = res.data["items"]
        request_success.value = true
        is_show_result.value = false
    } catch (e) {
        let error = e as AxiosError
        request_success.value = false
        error_message.value = error.response?.data
        ElMessage({
            showClose: true,
            message: "Oops, " + error_message.value,
            type: "error",
        })
    }
}

const reset_form = (element: FormInstance | undefined) => {
    advance_form.value.title = ""
    advance_form.value.actor = ""
    advance_form.value.director = ""
    advance_form.value.year = ""
    advance_form.value.country = ""
    advance_form.value.r18 = false
    advance_form.value.genre = ""
}
</script>

<style>

.search-title {
    text-align: center;
    background-color: #040714;
    color: #F9F9F9 !important;
    /* margin: 10px auto; */
}

.el-form-item__label {
    color: #F9F9F9 !important;
}

.el-radio {
    color: #F9F9F9 !important;
}

#ads-input {
    padding-left: 200px;
    padding-right: 200px;
}

</style>