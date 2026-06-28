import api from './api'

export const templateService = {
  async list(params = {}) {
    const { data } = await api.get('/templates', { params })
    return data
  },
  async get(id) {
    const { data } = await api.get(`/templates/${id}`)
    return data
  },
  async create(payload) {
    const { data } = await api.post('/templates', payload)
    return data
  },
  async update(id, payload) {
    const { data } = await api.put(`/templates/${id}`, payload)
    return data
  },
  async reorder(id, sections) {
    const { data } = await api.post(`/templates/${id}/sections/reorder`, { sections })
    return data
  },
  async remove(id) {
    const { data } = await api.delete(`/templates/${id}`)
    return data
  },
}
