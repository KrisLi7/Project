<template>
<div id="message-card">
    <a id="message-link" :href="dynamic_url">
        <div class="message-card-info">
            {{ tcejbo.message }}
        </div>
    </a>
</div>
</template>

<script lang="ts" setup>
import { ref, defineComponent, reactive, PropType } from 'vue'
import { MessageObject } from "../../types/index"

const props = defineProps({
    tcejbo: {
        type: Object as PropType<MessageObject>,
        default: {
            ms_id: "0",
            m_id: "#",
            message: ""
        },
        require: true
    }
})


const dynamic_url = ref("/movie/" + props.tcejbo.m_id)


</script>

<style lang="less">
#message-card {
    margin: 50px;
    color: var(--text-color);
    box-shadow: 3px;
}

#message-link {
    color: var(--text-color);
}

#message-link:hover {
    color: #0063E5;
}
</style>