import request from "./index";


export function api_post_review(data: any) {
    return request({
        url: "/review/post",
        method: "post",
        data,
    })
}

export function api_get_review(params: any) {
    return request({
        url: "/review/get",
        method: "get",
        params, // [m_id: string]
    })
}

export function api_review_react(data: any) {
    return request({
        url: "/review/react",
        method: "post",
        data, // [m_id: string]
    })
}
