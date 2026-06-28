import api from './api'

export const productService = {
  async list(params = {}) {
    const { data } = await api.get('/products', { params })
    return data
  },
  async get(id) {
    const { data } = await api.get(`/products/${id}`)
    return data
  },
  async create(payload) {
    const { data } = await api.post('/products', payload)
    return data
  },
  async update(id, payload) {
    const { data } = await api.put(`/products/${id}`, payload)
    return data
  },
  async remove(id) {
    const { data } = await api.delete(`/products/${id}`)
    return data
  },
  async documents(id) {
    const { data } = await api.get(`/products/${id}/documents`)
    return data
  },
}
