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
  async documents(id) {
    const { data } = await api.get(`/products/${id}/documents`)
    return data
  },
}
