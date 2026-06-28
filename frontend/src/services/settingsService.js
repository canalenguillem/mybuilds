import api from './api'

export const settingsService = {
  async getIntegrations() {
    const { data } = await api.get('/settings/integrations')
    return data
  },
  async updateIntegrations(payload) {
    const { data } = await api.put('/settings/integrations', payload)
    return data
  },
  async testIntegrations() {
    const { data } = await api.post('/settings/integrations/test')
    return data
  },
}
