import { createStore } from 'vuex'
import { CurrentUserObject, CurrentEmailObject, UserObject } from "../types"
import VuexPersistence from 'vuex-persist'

const curr_user: CurrentUserObject = {
    u_id: "",
    u_username: "",
    u_token: "",
    u_is_login: 0
}

const user_profile: UserObject = {
    u_id: "",
    u_email: "",
    u_username: "",
    u_avatar: "",
    u_firstname: "",
    u_lastname: "",
    u_level: 1,
    u_exp: 0,
    u_is_critic_reviewer: false,
    u_notification: false,
    u_wishlist: [],
    u_banned_list:[]
}

const curr_regi_email: CurrentEmailObject = {
    u_email: ""
}


const curr_search = {
    items: []
}

const home_page_movie = {
    items: []
}

const curr_count = 0

const stores = createStore({
    state: function () {
        return {
            curr_user,
            curr_search,
            curr_count,
            home_page_movie,
            curr_regi_email,
            user_profile
        }
    },
    mutations: {
        clear_user(state) {
            state.curr_user = {
                u_id: "",
                u_token: "",
                u_username: "",
                u_is_login: 0
            }
        },
        attach_user(state, payload) {
            state.curr_user = payload
        },

        attach_user_profile(state, payload) {
            state.user_profile = payload
        },

        attach_email(state, payload) {
            state.curr_regi_email = payload
        },

        attach_result(state, payload) {
            state.curr_search.items = payload
        },
        attach_home_page_movie(state, payload) {
            state.home_page_movie.items = payload
        }
    },
    getters: {
        get_user: (state): CurrentUserObject => {
            return state.curr_user
        },

        get_user_profile: (state): UserObject => {
            return state.user_profile
        },

        get_email: (state): CurrentEmailObject => {
            return state.curr_regi_email
        },

        get_result: (state) => {
            return state.curr_search
        },

        get_home_page_move: (state) => {
            return state.home_page_movie.items
        }
    },
    plugins: [new VuexPersistence({
        storage: window.sessionStorage
    }).plugin]
})
export default stores;
