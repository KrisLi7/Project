<template>
    <div id="link">
        <a id="link-href" :href='update_url().value'>{{ tcejbo?.[1] }}</a>
    </div>
</template>

<script lang="ts">
import { ref, defineComponent, reactive } from "vue"

export default defineComponent({
    name: "Link",
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

#link {
    width: 153px;
    height:50px;
    border: 1px solid rgb(255, 255, 255);
    float: left;
    text-align: center;
    margin:5px;
    font-family: var(--font-family);
}
</style>