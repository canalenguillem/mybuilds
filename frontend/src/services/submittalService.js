import api from './api'

export const submittalService = {
  async list(params = {}) {
    const { data } = await api.get('/submittals', { params })
    return data
  },
  async get(id) {
    const { data } = await api.get(`/submittals/${id}`)
    return data
  },
  async generate(payload) {
    const { data } = await api.post('/submittals/generate', payload)
    return data
  },
  async regenerate(id) {
    const { data } = await api.post(`/submittals/${id}/regenerate`)
    return data
  },
  async taskStatus(taskId) {
    const { data } = await api.get(`/submittals/tasks/${taskId}`)
    return data
  },
  async archive(id) {
    const { data } = await api.delete(`/submittals/${id}`)
    return data
  },
  /** Download the generated PDF with the auth header, then save via a blob URL. */
  async download(id, submissionNumber) {
    const res = await api.get(`/submittals/${id}/download`, { responseType: 'blob' })
    const url = URL.createObjectURL(res.data)
    const a = document.createElement('a')
    a.href = url
    a.download = `${submissionNumber || 'submittal'}.pdf`
    document.body.appendChild(a)
    a.click()
    a.remove()
    URL.revokeObjectURL(url)
  },
}

const STATUS_STYLES = {
  generated: { bg: 'var(--primary-tint)', color: 'var(--primary)', label: 'Generated' },
  generating: { bg: 'var(--warning-bg)', color: 'var(--warning)', label: 'Generating' },
  draft: { bg: 'var(--warning-bg)', color: 'var(--warning)', label: 'Draft' },
  reviewed: { bg: 'var(--purple-bg)', color: 'var(--purple)', label: 'Reviewed' },
  approved: { bg: 'var(--success-bg)', color: 'var(--success-text)', label: 'Approved' },
  archived: { bg: '#eef0f3', color: 'var(--text-muted)', label: 'Archived' },
  failed: { bg: 'var(--error-bg)', color: 'var(--error)', label: 'Failed' },
}

export function statusStyle(status) {
  return STATUS_STYLES[status] || { bg: '#eef0f3', color: 'var(--text-muted)', label: status }
}
