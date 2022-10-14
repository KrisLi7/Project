<template>
    <div id="review">
        <div id="md-editor-box">
            <md-editor id="md-editor" v-model="text" @onChange="on_change" :toolbars="[
                'bold', 'underline', 'italic', '-',
                'title', 'strikeThrough', 'sub', 'sup',
                'quote', 'unorderedList', 'orderedList',
                '-', 'codeRow', 'code', 'preview'
            ]" :preview="false" language="en-US" />
            <div>
                <el-form class="edit-form-button-div" ref="ref_edit_form" :model="post_review_object">
                    <div class="review-rate-div">
                        <el-rate v-model="value" allow-half show-score score-template="{value} Points" />
                    </div>
                    <div class="review-button-div">
                        <el-button type="primary" class="edit-form-button" @click="submit_form"> Submit
                        </el-button>
                        <el-button type="primary" class="edit-form-button" @click="reset_form"> Clear </el-button>
                    </div>
                </el-form>
            </div>
        </div>
    </div>
    <div id="review-result">
        <div class="review-infinite-list" v-infinite-scroll="on_scroll_load" infinite-scroll-distance="1">
            <div class="review-infinite-list-item" v-for="item in reviews">
                <div class="review-container">
                    <div class="review-info">
                        <ReviewCard :tcejbo="item"></ReviewCard>
                        <div class="review-info right">
                            <div class="review-info right rate">
                                <el-rate v-model="item.r_rate" disabled />
                                <i class="review-info right rate i">
                                    {{ item.r_rate }}
                                </i>
                            </div>
                            <div class="review-info right rate">
                                <p>
                                    <el-button v-if="item.r_is_like" round type="success"
                                        @click="react_like(item.r_id)">
                                        <box-icon name='happy-heart-eyes' animation='tada' color='#190eed'></box-icon>
                                        Like
                                        {{ item.r_like }}
                                    </el-button>
                                    <el-button v-else round @click="react_like(item.r_id)">
                                        <box-icon name='wink-smile' animation='tada' color='#190eed'></box-icon>
                                        Like
                                        {{ item.r_like }}
                                    </el-button>
                                </p>

                                <p>
                                    <el-button v-if="item.r_is_dislike" round type="danger"
                                        @click="react_dislike(item.r_id)">
                                        <box-icon name='sad' animation='tada' color="#000000"></box-icon>
                                        Dislike
                                        {{ item.r_dislike }}
                                    </el-button>
                                    <el-button v-else round @click="react_dislike(item.r_id)">
                                        <box-icon name='tired' animation='tada' color="#ff0000"></box-icon>
                                        Dislike
                                        {{ item.r_dislike }}
                                    </el-button>
                                </p>

                            </div>
                        </div>
                    </div>
                    <div class="review-box">
                        <md-editor id="md-editor" v-model="item.r_review" :preview-only="true" />
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>


<script lang="ts" setup>
import { ref, reactive, onMounted, watch, PropType } from 'vue'
import MdEditor from 'md-editor-v3';
import 'md-editor-v3/lib/style.css';
import { ElMessage } from 'element-plus';
import { AxiosError } from 'axios';
import { api_get_review, api_post_review, api_review_react } from '../../api/service_review';
import { useStore } from 'vuex'
import ReviewCard from './ReviewCard.vue';
import { CurrentUserObject, MovieReviewObject, PostReviewObject } from '../../types';

const props = defineProps({
    m_id: {
        type: String,
        required: true
    },
    u_curr_obj: {
        type: Object as PropType<CurrentUserObject>,
        required: true
    },
})

const value = ref<number>(0)
const text = ref<string>('# Please leave a friendly review')
const on_change = (val: any) => { };
const reviews = ref<Array<MovieReviewObject>>([])
const pos_x = ref<number>(0)
const pos_y = ref<number>(3)
const stack = ref<Array<MovieReviewObject>>([])
const state = useStore()
const DFA = ref<number>(0) // 0 -> 1 -> 2 -> 3 -> 2 -> 4 -> 2
const error_message = ref()

const update_reviews = async () => {
    try {
        let result = await api_get_review({
            "u_token": state.getters.get_user.u_token,
            "m_id": props.m_id
        })
        reviews.value = result.data
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

onMounted(async () => {
    update_reviews()
});

watch(() => reviews, (val, old) => {
    if (DFA.value === 0) {
        DFA.value = 1
    }
    if (DFA.value === 1) {
        on_scroll_load()
    }
    if (DFA.value === 4) {
        let item = reviews.value.at(0)
        stack.value.unshift(item!)
        DFA.value = 2
    }
})

const on_scroll_load = () => {
    switch (DFA.value) {
        case 1:
            DFA.value = 2
        case 2:
            for (const x of reviews.value.slice(pos_x.value, pos_y.value)) {
                stack.value.push(x)
            }
            DFA.value = 3
        case 3:
            pos_x.value = pos_y.value
            pos_y.value += 1
            DFA.value = 2
        default:
            break;
    }
};

const post_review_object = ref<PostReviewObject>({
    m_id: props.m_id,
    u_token: props.u_curr_obj.u_token,
    u_text: "",
    u_rate: 0
})

const react_obj = reactive({
    u_token: "",
    r_id: "",
    ra_id: "",
})

const submit_form = async (): Promise<void> => {
    try {
        post_review_object.value.u_text = text.value
        post_review_object.value.u_rate = value.value
        await api_post_review(post_review_object.value)
        ElMessage({
            showClose: true,
            message: "Post review successfully",
            type: "success",
        })
        update_reviews()
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

const react_like = async (r_id: string) => {
    try {
        react_obj.u_token = state.getters.get_user.u_token
        react_obj.r_id = r_id
        react_obj.ra_id = "1"
        await api_review_react(react_obj)
        update_reviews()
    } catch (e) {
        let error = e as AxiosError
        ElMessage({
            showClose: true,
            message: "Oops, " + error.response?.data,
            type: "error",
        })
    }
}

const react_dislike = async (r_id: string) => {
    try {
        react_obj.u_token = state.getters.get_user.u_token
        react_obj.r_id = r_id
        react_obj.ra_id = "2"
        await api_review_react(react_obj)
        update_reviews()
    } catch (e) {
        let error = e as AxiosError
        ElMessage({
            showClose: true,
            message: "Oops, " + error.response?.data,
            type: "error",
        })
    }
}

const reset_form = () => {
    text.value = ""
}
</script>

<style lang="less" scoped>
::v-deep(.el-rate__text) {
    color: var(--rate-color);
    align-items: center;
}

::v-deep(.el-rate__item) {
    display: flex;
    align-items: center;
}

#review {
    display: flex;
    flex-direction: column;
    text-align: left;
    margin-bottom: 50px;
}

#md-editor-box {
    height: 250px;
}

#md-editor {
    height: 100%;
    width: 100%;
    border-radius: 5px;
    background-color: #1a1d29;
    --md-color: #ffffff;
    --md-bk-color-outstand: #1a1d29;
}

.edit-form-button-div {
    display: flex;
    position: relative;
    flex-direction: row;
    margin: 10px 5px;
}

.review-rate-div {
    width: 68%;
}

.review-button-div {
    width: 32%;
    text-align: right;
}

#review-result {
    display: flex;
    flex-wrap: wrap;
    overflow: auto;
    margin-top: 20px;
}

.review-infinite-list {
    display: flex;
    flex-direction: column;
    padding-right: 10px;
    padding-left: 10px;
    width: 100%;
    height: 800px;
}
.review-infinite-list-item {
    flex: 0 1 200px;
    margin-top: 10px;
}
</style>




