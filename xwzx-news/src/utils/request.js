import axios from 'axios'
import { showToast } from 'vant'
import { apiConfig } from '../config/api'

// 创建统一的 Axios 实例
const request = axios.create({
  baseURL: apiConfig.baseURL,
  timeout: 15000,
})

// 请求拦截器：自动附加 Authorization 头
// pinia-plugin-persistedstate 会将 user store 持久化到 localStorage
request.interceptors.request.use(
  (config) => {
    try {
      const raw = localStorage.getItem('user-store')
      if (raw) {
        const parsed = JSON.parse(raw)
        if (parsed.token) {
          config.headers.Authorization = `Bearer ${parsed.token}`
        }
      }
    } catch {
      // token 不存在或解析失败，不附加 Authorization 头
    }
    return config
  },
  (error) => Promise.reject(error)
)

// 响应拦截器：统一处理业务错误
request.interceptors.response.use(
  (response) => {
    if (response.data && response.data.code !== 200) {
      const msg = response.data.message || '请求失败'
      showToast({ message: msg, position: 'bottom' })
    }
    return response
  },
  (error) => {
    let message = '网络请求失败'
    if (error.response) {
      const status = error.response.status
      if (status === 401) {
        message = '登录已过期，请重新登录'
      } else if (status === 500) {
        message = '服务器错误，请稍后重试'
      } else {
        message = error.response.data?.message || `请求失败 (${status})`
      }
    }
    showToast({ message, position: 'bottom' })
    return Promise.reject(error)
  }
)

export default request
