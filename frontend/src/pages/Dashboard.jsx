import { useEffect, useState } from 'react'
import AppLayout from '../components/common/AppLayout'
import { useAuth } from '../context/AuthContext'
import { analyticsService } from '../services/analyticsService'
import { statusStyle } from '../services/submittalService'

export default function Dashboard() {
  const { user } = useAuth()
  const [data, setData] = useState(null)

  useEffect(() => { analyticsService.dashboard().then(setData).catch(() => {}) }, [])

  const m = data?.metrics
  const kpis = [
    { label: 'Submittals (month)', value: m ? m.submittals_this_month : '—', sub: m ? `${m.total_submittals} total` : '' },
    { label: 'Documents', value: m ? m.total_documents : '—', sub: m ? `${m.total_products} products` : '' },
    { label: 'Templates', value: m ? m.total_templates : '—' },
    { label: 'Compliance pending', value: m ? m.compliance_pending_review : '—', sub: m ? `${m.compliance_approved} approved` : '' },
  ]

  return (
    <AppLayout title="Dashboard">
      <h1>Dashboard</h1>
      <p style={{ color: 'var(--text-muted)', marginTop: 4 }}>
        Welcome back, {user?.username}.
      </p>

      <div className="kpi-grid">
        {kpis.map((k) => (
          <div className="card" key={k.label}>
            <div className="kpi-label">{k.label}</div>
            <div className="kpi-value">{k.value}</div>
            {k.sub ? <div style={{ color: 'var(--text-faint)', fontSize: 12, marginTop: 4 }}>{k.sub}</div> : null}
          </div>
        ))}
      </div>

      <div className="card" style={{ marginTop: 24, padding: 0, overflow: 'hidden' }}>
        <div style={{ padding: '16px 20px', borderBottom: '1px solid var(--border)' }}>
          <strong style={{ color: 'var(--text-primary)' }}>Recent submittals</strong>
        </div>
        {!data ? (
          <div style={{ padding: 20, color: 'var(--text-muted)' }}>Loading…</div>
        ) : !data.recent_submittals.length ? (
          <div style={{ padding: 20, color: 'var(--text-muted)' }}>
            No submittals yet. Generate one from the Submittals page.
          </div>
        ) : (
          <table className="table">
            <thead><tr><th>Submission</th><th>Project</th><th>Status</th><th>Pages</th></tr></thead>
            <tbody>
              {data.recent_submittals.map((s) => {
                const st = statusStyle(s.status)
                return (
                  <tr key={s.id}>
                    <td><strong style={{ color: 'var(--text-primary)' }}>{s.submission_number}</strong></td>
                    <td style={{ color: 'var(--text-muted)' }}>{s.project_name || '—'}</td>
                    <td><span className="badge" style={{ background: st.bg, color: st.color }}>{st.label}</span></td>
                    <td>{s.page_count ?? '—'}</td>
                  </tr>
                )
              })}
            </tbody>
          </table>
        )}
      </div>
    </AppLayout>
  )
}
