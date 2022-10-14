<template>

   <div id="movie-info">

      <div id="movie-image">
         <el-image style="width: 100px; height: 100px" :src="tcejbo?.m_poster" />
      </div>
      <div id="movie-info-detail">
         <label>{{ tcejbo?.m_title }} {{ tcejbo?.m_year }}</label>
         <el-rate v-model="value" disabled :max="10" show-score text-color="#ff9900" score-template="{value}" />
         <div>
            {{ tcejbo?.m_cast }}
         </div>
      </div>
   </div>
</template>


<script lang="ts" setup>
import { ref } from "vue"
import { MovieObject } from "../types"

const props = defineProps({
   tcejbo: Object as () => MovieObject
})

const value = ref(props.tcejbo?.m_imdb_rate)
const state = props
</script>


<style>
#movie-info {
   display: flex;
   flex-direction: row;
   margin: 10px auto;
   border: 1px solid #d0d7de;
}

#movie-image {
   display: flex;
   flex-direction: column;
   margin: 10px auto;
   border: 1px solid #d0d7de;
}

#movie-info-detail {
   display: flex;
   flex-direction: column;
   margin: 10px auto;
   border: 1px solid #d0d7de;
}
</style>
