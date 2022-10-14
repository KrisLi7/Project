
import { AdvanceSearchObject, LoginObject, RegisterObject } from "../types";

import request from "./index";

// 高级搜索
export function api_movie_advance_search(params: any) {
    return request({
        url: '/movie/advancedsearch',
        method: 'get',
        params,
    })
}

/** search api
 *
**/

// 主页电影
export function api_home_page_movie(params: any) {
    return request({
        url: '/homepagemovie',
        method: 'get',
        params
    })
}

// 平凡搜索
export function api_movie_home_search(params: any) {
    return request({
        url: '/movie/homesearch',
        method: 'get',
        params,
    })
}

export function api_get_target_movie(params: any) {
    return request({
        url: '/moviedetails',
        method: 'get',
        params, // m_id
    })
}

export function api_check_is_in_wish_list(params: any) {
    return request({
        url: '/movie/wishlist/check',
        method: 'get',
        params, // m_id
    })
}

export function api_add_to_wishlist(data: any) {
    return request({
        url: "/movie/wishlist/add",
        method: "post",
        data, // u_token
    })
}

export function api_remove_from_wishlist(data: any) {
    return request({
        url: "/movie/wishlist/remove",
        method: "post",
        data, // u_token
    })
}