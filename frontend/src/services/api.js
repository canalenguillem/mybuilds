import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

export const TOKEN_KEY = 'mb_access_token'
export const REFRESH_KEY = 'mb_refresh_token'

const api = axios.create({
  baseURL: API_URL,
  headers: { 'Content-Type': 'application/json' },
})

// Attach the access token to every request.
api.interceptors.request.use((config) => {
  const token = localStorage.getItem(TOKEN_KEY)
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

// On a 401, try a one-shot refresh, then replay the original request.
let refreshing = null

api.interceptors.response.use(
  (res) => res,
  async (error) => {
    const original = error.config
    const refreshToken = localStorage.getItem(REFRESH_KEY)

    if (
      error.response?.status === 401 &&
      !original._retry &&
      refreshToken &&
      !original.url?.includes('/auth/')
    ) {
      original._retry = true
      try {
        refreshing =
          refreshing ||
          axios.post(`${API_URL}/auth/refresh`, { refresh_token: refreshToken })
        const { data } = await refreshing
        refreshing = null
        localStorage.setItem(TOKEN_KEY, data.access_token)
        original.headers.Authorization = `Bearer ${data.access_token}`
        return api(original)
      } catch (e) {
        refreshing = null
        localStorage.removeItem(TOKEN_KEY)
        localStorage.removeItem(REFRESH_KEY)
        window.location.href = '/login'
        return Promise.reject(e)
      }
    }
    return Promise.reject(error)
  }
)

/** Extract a human-readable message from the standard error envelope. */
export function apiError(error, fallback = 'Something went wrong.') {
  return error?.response?.data?.error?.message || fallback
}

export default api
