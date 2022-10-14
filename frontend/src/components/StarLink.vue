<template>  
    <a id="link-href" :href='update_url().value'> 
        <div class="star-card"><img :src="tcejbo?.[3]"/>
            <div class="star-card-content">
                <p class="star-card-title"> 
                    <p> Role: </p> {{ tcejbo?.[2]}}
                </p>              
            </div>
        </div>
        <div id="star-name">
            {{ tcejbo?.[1] }}
        </div>
    </a>
</template>

<script lang="ts">
import { ref, defineComponent, reactive } from "vue"

export default defineComponent({
    name: "StarLink",
    props: {
        tcejbo: Object as () => Array<string>
    },
    components: { },
    setup: function (props: any) {

        const update_url = () => {
            let info_array = props.tcejbo;
            let dynamic_url = ref<string>("")
            let id_str = info_array?.at(0)
            if (id_str?.substring(0, 2) === "tt") {
                dynamic_url.value = "/movie/" + info_array?.at(0)
            } else if (id_str?.substring(0, 2) === "nm") {
                dynamic_url.value = "/actor/" + info_array?.at(0)
            } else {
                dynamic_url.value = "/echo" // 404
            }
            return dynamic_url
        }

        return {
            update_url
        }
    }
})

</script>

<style>
#link-href {
    color: #ffffff;
}


.star-card {
    display: block;
    position: relative;
    overflow: hidden;
    padding-top: 140%;
    height: 300px;
    width: 200px;
    cursor: pointer;
    border-radius: 20px;
}

.star-card img {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    transition: transform 0.3s linear;
}

/*
cursor scale up
*/

.star-card:hover img {
    transform: scale(1.2);
}

.star-card-content {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    padding: 5px;
    background-color: rgba(0, 0, 0, 0.8);
}

.star-card-content::before {
    content: "";
    position: absolute;
    bottom: 100%;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(to top, rgba(0, 0, 0, 0.8), rgba(0, 0, 0, 0));
}

.star-card-title {
    color: var(--text-color);
    font-size: 1.2rem;
    position: relative;
    font-weight: 600;
    text-align: center;
}

#star-name {
    font-size: 1.2rem;
    padding-top: 10px;
    text-align: center;
}
::v-deep(.el-rate__item) {
    display: flex;
}
</style>