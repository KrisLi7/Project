<template>
    <div id="this">
        <el-upload class="avatar-uploader" action="#" :http-request="upload_to_database"
            :show-file-list="false" :on-success="handleAvatarSuccess" :before-upload="beforeAvatarUpload">
            <img class="avatar" v-if="state.getters.get_user_profile.u_avatar" :src="state.getters.get_user_profile.u_avatar"/>
            <el-icon v-else class="avatar-uploader-icon">
                <Plus></Plus>
            </el-icon>
        </el-upload>
    </div>
</template>

<script lang="ts">
import { ref, defineComponent, reactive } from 'vue'
import { ElMessage, UploadFile, UploadRawFile, UploadRequestOptions } from 'element-plus'
import type { UploadProps } from 'element-plus'
import { AxiosError } from 'axios';
import { UploadAvatarObject } from '../types';
import { api_change_user_avatar, api_get_user } from '../api/service';
import { useStore } from 'vuex';

export default defineComponent({
    name: "UserAvatar",
    props: {
        tcejbo: Object as () => string
    },
    setup: function (props) {
        const state = useStore();

        const ref_this = ref();

        const ref_object = {
            upload_file: ref<UploadFile>(),
            upload_raw_file: ref<UploadRawFile>(),
            image_url: ref<string>(""),
            is_avatar_null: ref<Boolean>(false),
        }

        const image_base64 = ref<string | ArrayBuffer | null>("");

        const get_base64 = (file_obj: Blob): Promise<string> => {
            return new Promise(function (resolve, reject) {
                let reader: FileReader = new FileReader();
                let result: string = ""
                reader.readAsDataURL(file_obj);
                reader.onload = function () {
                    if (reader.result) {
                        result = reader.result.toString();
                    } else {
                        throw Error("FileReader result is Empty")
                    }
                };
                reader.onerror = function (error) {
                    reject(error);
                };
                reader.onloadend = function () {
                    resolve(result)
                }
                return result;
            })
        }

        const error_message = ref<unknown>();

        const request_object = reactive<UploadAvatarObject>({
            u_token: "",
            u_data: ""
        })

        const upload_to_database = async (params: UploadRequestOptions): Promise<void> => {
            return get_base64(ref_object.upload_raw_file.value!).then(
                async result => {
                    image_base64.value = result;
                    request_object.u_data = image_base64.value
                    request_object.u_token = state.getters.get_user.u_token
                    try {
                        let api_res = await api_change_user_avatar(request_object)
                        let res = await api_get_user(state.getters.get_user)
                        state.commit("attach_user_profile", res.data)
                        ElMessage({
                            showClose: true,
                            message: api_res.data.message,
                            type: "success",
                        })
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
            )
        }

        const handleAvatarSuccess: UploadProps['onSuccess'] = (response, uploadFile: UploadFile) => {
            ref_object.image_url.value = URL.createObjectURL(uploadFile.raw!)
            ref_object.is_avatar_null.value = ref_object.image_url.value === "" ? false : true;
            ref_object.upload_file.value = uploadFile
        }

        const beforeAvatarUpload: UploadProps['beforeUpload'] = (raw_file: UploadRawFile) => {
            if (raw_file.type !== 'image/jpeg') {
                ElMessage.error('Avatar picture must be JPG format!')
                return false
            } else if (raw_file.size / 1024 / 1024 > 2) {
                ElMessage.error('Avatar picture size can not exceed 2MB!')
                return false
            }
            ref_object.upload_raw_file.value = raw_file
            return true
        }

        return {
            ref_this,
            ref_object,
            handleAvatarSuccess,
            beforeAvatarUpload,
            upload_to_database,
            image_base64,
            state
        };
    },
})
</script>

<style>

.this {
    text-align: left;
}

.avatar-uploader {
    margin-right:50px;
}

.avatar-uploader .avatar {
    width: 100%;
    height: 100%;
    display: block;
    object-fit: scale-down;
}

.avatar-uploader .el-upload {
    border: 1px dashed var(--el-border-color);
    border-radius: 6px;
    cursor: pointer;
    position: relative;
    overflow: hidden;
    transition: var(--el-transition-duration-fast);
}

.avatar-uploader .el-upload:hover {
    border-color: var(--el-color-primary);
}

.el-icon.avatar-uploader-icon {
    font-size: 28px;
    color: #8c939d;
    width: 178px;
    height: 178px;
    text-align: center;
}
</style>