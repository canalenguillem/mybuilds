import api from './api'

export const complianceService = {
  async analyze(payload) {
    const { data } = await api.post('/compliance/analyze', payload)
    return data
  },
  async taskStatus(taskId) {
    const { data } = await api.get(`/compliance/tasks/${taskId}`)
    return data
  },
  async listStatements(params = {}) {
    const { data } = await api.get('/compliance/statements', { params })
    return data
  },
  async review(statementId, payload) {
    const { data } = await api.post(`/compliance/statements/${statementId}/review`, payload)
    return data
  },
}

const STATUS = {
  pending_review: { bg: 'var(--warning-bg)', color: 'var(--warning)', label: 'Pending review' },
  approved: { bg: 'var(--success-bg)', color: 'var(--success-text)', label: 'Approved' },
  rejected: { bg: 'var(--error-bg)', color: 'var(--error)', label: 'Rejected' },
  needs_revision: { bg: 'var(--purple-bg)', color: 'var(--purple)', label: 'Needs revision' },
}

export function reviewStatusStyle(s) {
  return STATUS[s] || { bg: '#eef0f3', color: 'var(--text-muted)', label: s }
}
