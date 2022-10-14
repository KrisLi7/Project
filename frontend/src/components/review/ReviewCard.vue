<template>
    <div class="review-info left">
        <div class="review-info left avatar">
            <a id="link-href" :href="dynamic_url">
                <el-avatar v-if="props.tcejbo.u_avatar" size="large" :src= "props.tcejbo.u_avatar"/>
                <el-avatar v-else size="large" :src= "default_avatar"/>
            </a>
        </div>
        <div class="review-info left user">
            <div class="review-info left user name">
                <a id="link-href" :href="dynamic_url">{{ props.tcejbo.u_username }} </a>
            </div>

            <div v-if="props.tcejbo.u_is_critic_reviewer == false">
                <box-icon name='analyse' flip='vertical' animation='spin' color='#0063e5' ></box-icon>
                Non Critic Reviewer
            </div>
            <div v-else>
                <box-icon name='analyse' flip='vertical' animation='spin' color='#D58C12' ></box-icon>
                Critic Reviewer
            </div>

            <div class="review-info left user time">Time : {{ props.tcejbo.r_time_created }} </div>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { PropType, ref} from 'vue'
import { MovieReviewObject } from '../../types';

const props = defineProps({
    tcejbo: {
        type: Object as PropType<MovieReviewObject>,
        default: [],
        require: true
    }
})
const dynamic_url =  "/profile/" + props.tcejbo?.u_id
const default_avatar = ref<string>("https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png")
</script>

<style lang="less">
.review-container {
    display: flex;
    flex-direction: column;
    position: relative;
    background-color: #1a1d29;
    border-radius: 5px;
    box-shadow: 0 15px 20px rgba(0, 0, 0, 0.356);
}

.review-info {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;

    &.left {
        &.avatar {
            padding-top: 10px;
            padding-left: 10px;
            margin-right: 10px;
        }

        &.user {
            padding-top: 10px;
            flex-direction: column;
            align-items: baseline;
        }
    }

    &.right {
        &.rate {
            padding-top: 10px;
            padding-right: 50px;
            flex-direction: column;
            align-items: baseline;

            &.i {
                color: var(--rate-color);
            }
        }

    }
}

.review-box {
    display: flex;
    text-align: left;
    padding: 10px;
    margin: 0;
    box-shadow: var(--el-box-shadow);
}

#md-editor {

    height: 100%;
    width: 100%;
    border-radius: 5px;
    background-color: #1a1d29;
    --md-color: #ffffff;
    --md-bk-color-outstand: #1a1d29;
    border: 2px solid #ffffff;
}

#link-href {
    color: #ffffff;
}
</style>