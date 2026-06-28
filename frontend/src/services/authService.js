import api, { REFRESH_KEY, TOKEN_KEY } from './api'

export const authService = {
  async login(email, password) {
    const { data } = await api.post('/auth/login', { email, password })
    localStorage.setItem(TOKEN_KEY, data.access_token)
    localStorage.setItem(REFRESH_KEY, data.refresh_token)
    return data.user
  },

  async register(payload) {
    const { data } = await api.post('/auth/register', payload)
    return data
  },

  async me() {
    const { data } = await api.get('/auth/me')
    return data
  },

  async logout() {
    const refresh_token = localStorage.getItem(REFRESH_KEY)
    try {
      if (refresh_token) await api.post('/auth/logout', { refresh_token })
    } finally {
      localStorage.removeItem(TOKEN_KEY)
      localStorage.removeItem(REFRESH_KEY)
    }
  },

  isAuthenticated() {
    return Boolean(localStorage.getItem(TOKEN_KEY))
  },
}
