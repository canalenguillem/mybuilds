import AppLayout from '../components/common/AppLayout'
import { useAuth } from '../context/AuthContext'

// Placeholder KPIs — these will be wired to GET /analytics/dashboard.
const KPIS = [
  { label: 'Submittals (month)', value: '—' },
  { label: 'Documents', value: '—' },
  { label: 'Templates', value: '—' },
  { label: 'Avg. generation', value: '—' },
]

export default function Dashboard() {
  const { user } = useAuth()
  return (
    <AppLayout>
      <h1>Dashboard</h1>
      <p style={{ color: 'var(--text-muted)', marginTop: 4 }}>
        Welcome back, {user?.username}. Roles: {user?.roles?.join(', ') || '—'}
      </p>

      <div className="kpi-grid">
        {KPIS.map((k) => (
          <div className="card" key={k.label}>
            <div className="kpi-label">{k.label}</div>
            <div className="kpi-value">{k.value}</div>
          </div>
        ))}
      </div>

      <div className="card" style={{ marginTop: 24 }}>
        <strong style={{ color: 'var(--text-primary)' }}>Recent submittals</strong>
        <p style={{ color: 'var(--text-muted)', marginTop: 8 }}>
          No submittals yet. The generator wizard and submittals list arrive in the next
          build phase.
        </p>
      </div>
    </AppLayout>
  )
}
