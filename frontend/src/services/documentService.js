import api from './api'

export const DOCUMENT_TYPES = [
  'datasheets',
  'certificates',
  'manuals',
  'catalogues',
  'vendor_lists',
  'compliance_docs',
  'company_profile',
]

export const documentService = {
  async list(params = {}) {
    const { data } = await api.get('/documents', { params })
    return data
  },
  async get(id) {
    const { data } = await api.get(`/documents/${id}`)
    return data
  },
  async upload({ file, product_id, document_type, title, description }) {
    const form = new FormData()
    form.append('file', file)
    form.append('product_id', product_id)
    form.append('document_type', document_type)
    form.append('title', title)
    if (description) form.append('description', description)
    const { data } = await api.post('/documents/upload', form, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    return data
  },
  async versions(id) {
    const { data } = await api.get(`/documents/${id}/versions`)
    return data
  },
  async remove(id) {
    const { data } = await api.delete(`/documents/${id}`)
    return data
  },
}

const TYPE_STYLE = {
  datasheets: { bg: '#e8f1fd', color: '#0066cc' },
  certificates: { bg: '#eaf6ec', color: '#1e7a32' },
  compliance_docs: { bg: '#fdf0e9', color: '#c2620f' },
  manuals: { bg: '#f0ecfd', color: '#6b4ed8' },
  catalogues: { bg: '#e7f6f7', color: '#0a8a93' },
  vendor_lists: { bg: '#fdf2f7', color: '#bd2a72' },
  company_profile: { bg: '#eef0f3', color: '#6b7685' },
}

export function docTypeStyle(t) {
  return TYPE_STYLE[t] || { bg: '#eef0f3', color: '#6b7685' }
}

export function formatBytes(n) {
  if (!n) return '—'
  const u = ['B', 'KB', 'MB', 'GB']
  let i = 0
  let v = n
  while (v >= 1024 && i < u.length - 1) { v /= 1024; i++ }
  return `${v.toFixed(v < 10 && i > 0 ? 1 : 0)} ${u[i]}`
}
