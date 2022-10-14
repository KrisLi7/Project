/**
 *
**/

export interface ErrorObject {
    code: number
    message: string
}

export class CurrentUserClass {
    u_id: string = ""
    u_token: string = ""
    u_username: string = ""
}


export class ProfileClass {
    u_id: string = ""
    u_email: string = ""
    u_username: string = ""
    u_avatar: string = ""
    u_firstname: string = ""
    u_lastname: string = ""
    u_date_of_brith: string = ""
    u_about_me: string = ""
}

export interface UserObject {
    u_id: string
    u_email: string
    u_username: string
    u_avatar: string
    u_firstname: string
    u_lastname: string
    u_level: number
    u_exp: number
    u_is_critic_reviewer: boolean
    u_notification: boolean
    u_wishlist: Array<MovieObject>
    u_banned_list: Array<BanObject>
}

export interface VisitUserObject {
    u_id: string
    u_email: string
    u_username: string
    u_avatar: string
    u_firstname: string
    u_lastname: string
    u_level: number
    u_exp: number
    u_is_critic_reviewer: boolean
    u_is_banned: boolean
    u_wishlist: Array<MovieObject>
}

export interface BanObject {
    u_id: string
    u_username: string
    a_u_avatar: string
}

export interface RegisterObject {
    u_username: string
    u_email: string
    u_password: string
}

export interface LoginObject {
    u_email: string
    u_password: string
}

export interface LogoutObject {
    u_token: string
}

export interface CurrentUserObject {
    u_id: string
    u_token: string
    u_username: string
    u_is_login: number
}

export interface CurrentEmailObject {
    u_email: string
}

export interface RequestResetObject {
    u_email: string
}

export interface ResetObject {
    u_password: string
    u_reset_code: string
}

export interface HomePageMovieObject {
    m_id: string
    m_title: string
    m_poster: string
    m_year: string
    m_imdb_rate: number
}

export interface MovieCardObject {
    m_id: string
    m_year: string
    m_title: string
    m_poster: string
    m_web_rate: number
    m_imdb_rate: number
}

export interface MovieObject {
    m_id: string
    m_title: string
    m_info: string
    m_poster: string
    m_year: string
    m_star: Array<Array<string>>
    m_cast: Array<Array<string>>
    m_director: Array<Array<string>>
    m_imdb_rate: number
    m_web_rate: number
    m_critic_web_rate: number
    m_country: string
    m_language: string
    m_genre: string
    m_similar: Array<MovieCardObject>
}

export interface SearchMovieObject {
    keyword: string
}

export interface SearchMovieReturnObject {
    m_id: string
    m_title: string
    m_poster: string
}

export interface ActorObject {
    p_id: string
    p_name: string
    p_nick_name: string
    p_birth_name: string
    p_akas: string
    p_filmography: Array<MovieObject>
    p_biography: string
    p_height: string
    p_headshot: string
    p_birth_date: string
    p_bio_expand: boolean
}

export interface ReviewObject {
    r_id: string
    r_info: string
    user_object: UserObject
}


////////////////////////////////////////////////////////////////////////////////


export interface AdvanceSearchObject {
    title: string
    actor: string
    director: string
    year: string
    country: string
    r18: boolean
    genre: string
}


export interface UploadAvatarObject {
    u_token: string
    u_data: string
}


export interface MovieReviewObject {
    r_id: string
    u_id: string
    u_username: string
    r_rate: number
    r_review: string
    r_time_created: string
    r_like: string
    r_dislike: string
    u_avatar: string
    u_is_critic_reviewer: boolean
    r_is_like: boolean
    r_is_dislike: boolean
}

export interface PostReviewObject {
    m_id: string
    u_token: string
    u_text: string
    u_rate: number
}


export interface MessageObject {
    ms_id: string
    m_id: string
    message: string
}