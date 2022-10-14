<template>
  <div id="message-list">
    <div class="" v-for="msg in tcejbo">
      <MessageCard :tcejbo="msg"></MessageCard>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { MessageObject } from '@/types';
import { ref, onMounted, PropType } from 'vue'
import { useStore } from 'vuex';
import MessageCard from './MessageCard.vue';

const state = useStore()

const props = defineProps({
  tcejbo: {
    type: Object as PropType<MessageObject[]>,
    default: {
      ms_id: "",
      m_id: "",
      message: "",
    },
    require: true
  }
})

onMounted(async () => {

})


</script>

<style lang="less">

#message-list {
  color: var(--text-color);
}

</style>