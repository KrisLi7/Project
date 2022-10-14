/**
 *
**/

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

import stones from "./stone"

import ElementPlus from 'element-plus'
import { Plus, Message } from '@element-plus/icons-vue'
import 'element-plus/dist/index.css'


const app = createApp(App)

app.component("Plus", Plus)
app.component("Message", Message)

app.use(router).use(ElementPlus).use(stones).mount('#app')
