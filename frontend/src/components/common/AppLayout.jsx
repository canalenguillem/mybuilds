import { useAuth } from '../../context/AuthContext'

const NAV = [
  { label: 'Dashboard', active: true },
  { label: 'Documents' },
  { label: 'Templates' },
  { label: 'Submittals' },
  { label: 'Compliance' },
  { label: 'Analytics' },
]

export default function AppLayout({ children }) {
  const { user, logout } = useAuth()
  const initials = (user?.username || 'U').slice(0, 2).toUpperCase()

  return (
    <div className="app-layout">
      <aside className="sidebar">
        <div className="auth-brand" style={{ marginBottom: 16 }}>
          <div className="auth-logo">mB</div>
          <span>myBuilds</span>
        </div>
        {NAV.map((item) => (
          <div key={item.label} className={`nav-item${item.active ? ' active' : ''}`}>
            {item.label}
          </div>
        ))}
      </aside>

      <div className="main">
        <header className="topbar">
          <strong style={{ color: 'var(--text-primary)' }}>Submittal Automation</strong>
          <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
            <span style={{ color: 'var(--text-muted)', fontSize: 13 }}>
              {user?.email}
            </span>
            <div className="avatar">{initials}</div>
            <button className="btn btn-secondary" style={{ height: 34 }} onClick={logout}>
              Sign out
            </button>
          </div>
        </header>
        <main className="content">{children}</main>
      </div>
    </div>
  )
}
