import { AdvanceSearchObject, LoginObject, RegisterObject } from "../types";

import request from "./index";

export function echo(params: any) {
  return request({
    url: "/user/",
    method: "get",
    params,
  });
}

export function api_test_get(params: any) {
  return request({
    url: "/moviehomesearch",
    method: "get",
    params,
  });
}

export function api_test_post(params: any) {
  return request({
    url: "/moviedetails",
    method: "post",
    params,
  });
}

/** auth api
 *
 **/

export function api_register(data: RegisterObject) {
  return request({
    url: "/register/",
    method: "post",
    data,
  });
}

export function api_login(data: LoginObject) {
  return request({
    url: "/login/",
    method: "post",
    data,
  });
}

export function api_logout(data: any) {
  return request({
    url: "/logout/",
    method: "post",
    data,
  });
}

export function api_password_reset_request(data: any) {
  return request({
    url: "/passwordreset/request",
    method: "post",
    data,
  });
}

export function api_password_reset(data: any) {
  return request({
    url: "/passwordreset/reset",
    method: "post",
    data,
  });
}

export function api_get_user_register(data: any) {
  return request({
    url: "/verify/email",
    method: "post",
    data,
  });
}

export function api_get_user_detail(params: any) {
  return request({
    url: "/user/detail/",
    method: "get",
    params, // u_token
  });
}

export function api_get_user(params: any) {
  return request({
    url: "/user/profile/",
    method: "get",
    params, // u_token
  });
}

export function api_get_visit_user(params: any) {
  return request({
    url: "/user/profile/visit",
    method: "get",
    params, // u_token
  });
}

export function api_change_username(data: any) {
  return request({
    url: "/user/profile/change/username",
    method: "post",
    data, // u_token
  });
}

export function api_change_user_firstname(data: any) {
  return request({
    url: "/user/profile/change/firstname",
    method: "post",
    data, // u_token
  });
}

export function api_change_user_lastname(data: any) {
  return request({
    url: "/user/profile/change/lastname",
    method: "post",
    data, // u_token
  });
}

export function api_change_user_email(data: any) {
  return request({
    url: "/user/profile/change/email",
    method: "post",
    data, // u_token
  });
}

export function api_change_user_avatar(data: any) {
  return request({
    url: "/user/profile/change/avatar",
    method: "post",
    data, // u_token
  });
}

export function api_change_user_notif_status(data: any) {
  return request({
    url: "/user/profile/change/notification",
    method: "post",
    data, // u_token
  });
}

export function api_change_user_ban_status(data: any) {
  return request({
    url: "/user/profile/bannedlist/add",
    method: "post",
    data, // u_token
  });
}

export function api_change_user_remove_ban_status(data: any) {
  return request({
    url: "/user/profile/bannedlist/remove",
    method: "post",
    data, // u_token
  });
}

export function api_get_target_actor(params: any) {
  return request({
    url: "/actor",
    method: "get",
    params,
  });
}

export function api_expand_bio(params: any) {
    return request({
        url: "/actor/expand/bio",
        method: "get",
        params,
    })
}

/** movie api
 *
 **/

export function api_message_delete(data: any) {
  return request({
    url: "/user/message/delete",
    method: "post",
    data,
  });
}

export function api_message_collect(data: any) {
  return request({
    url: "/user/message/collect",
    method: "post",
    data,
  });
}
