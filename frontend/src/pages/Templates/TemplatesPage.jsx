import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import AppLayout from '../../components/common/AppLayout'
import { templateService } from '../../services/templateService'
import { apiError } from '../../services/api'

export default function TemplatesPage() {
  const navigate = useNavigate()
  const [data, setData] = useState(null)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)

  const load = () => {
    setLoading(true)
    templateService
      .list()
      .then(setData)
      .catch((e) => setError(apiError(e, 'Failed to load templates.')))
      .finally(() => setLoading(false))
  }

  useEffect(load, [])

  const onDelete = async (id, name) => {
    if (!window.confirm(`Delete template "${name}"? This cannot be undone.`)) return
    try {
      await templateService.remove(id)
      load()
    } catch (e) {
      setError(apiError(e, 'Delete failed (admin role required).'))
    }
  }

  return (
    <AppLayout title="Templates">
      <div className="page-head">
        <div>
          <h1>Templates</h1>
          <p style={{ color: 'var(--text-muted)', marginTop: 4 }}>
            Define section order and structure for generated submittals.
          </p>
        </div>
        <button className="btn btn-primary" onClick={() => navigate('/templates/new')}>
          + New template
        </button>
      </div>

      {error && <div className="alert-error" style={{ marginTop: 16 }}>{error}</div>}

      <div className="card" style={{ marginTop: 24, padding: 0, overflow: 'hidden' }}>
        {loading ? (
          <div style={{ padding: 24, color: 'var(--text-muted)' }}>Loading…</div>
        ) : !data?.templates?.length ? (
          <div style={{ padding: 32, textAlign: 'center', color: 'var(--text-muted)' }}>
            No templates yet. Create your first one to get started.
          </div>
        ) : (
          <table className="table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Type</th>
                <th>Sections</th>
                <th>Version</th>
                <th>Status</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {data.templates.map((t) => (
                <tr key={t.id}>
                  <td>
                    <strong style={{ color: 'var(--text-primary)' }}>{t.name}</strong>
                  </td>
                  <td style={{ color: 'var(--text-muted)' }}>{t.template_type || '—'}</td>
                  <td>{t.section_count}</td>
                  <td>v{t.version}</td>
                  <td>
                    <span
                      className="badge"
                      style={{
                        background: t.is_active ? 'var(--success-bg)' : '#eef0f3',
                        color: t.is_active ? 'var(--success-text)' : 'var(--text-muted)',
                      }}
                    >
                      {t.is_active ? 'Active' : 'Inactive'}
                    </span>
                  </td>
                  <td style={{ textAlign: 'right', whiteSpace: 'nowrap' }}>
                    <button
                      className="btn btn-secondary"
                      style={{ height: 32, padding: '0 14px' }}
                      onClick={() => navigate(`/templates/${t.id}/edit`)}
                    >
                      Edit
                    </button>
                    <button
                      className="btn btn-secondary"
                      style={{ height: 32, padding: '0 14px', marginLeft: 8, color: 'var(--error)' }}
                      onClick={() => onDelete(t.id, t.name)}
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </AppLayout>
  )
}
