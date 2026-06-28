import api from './api'

export const documentService = {
  async list(params = {}) {
    const { data } = await api.get('/documents', { params })
    return data
  },
  async get(id) {
    const { data } = await api.get(`/documents/${id}`)
    return data
  },
}
