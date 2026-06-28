import api from './api'

export const analyticsService = {
  async dashboard() {
    const { data } = await api.get('/analytics/dashboard')
    return data
  },
}
