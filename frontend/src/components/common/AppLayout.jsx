import { NavLink } from 'react-router-dom'
import { useAuth } from '../../context/AuthContext'

const NAV = [
  { label: 'Dashboard', to: '/' },
  { label: 'Documents', to: '/documents' },
  { label: 'Templates', to: '/templates' },
  { label: 'Submittals', to: '/submittals' },
  { label: 'Compliance', to: '/compliance' },
  { label: 'Analytics', to: '/analytics' },
]

export default function AppLayout({ title = 'Submittal Automation', children }) {
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
          <NavLink
            key={item.to}
            to={item.to}
            end={item.to === '/'}
            className={({ isActive }) => `nav-item${isActive ? ' active' : ''}`}
          >
            {item.label}
          </NavLink>
        ))}
      </aside>

      <div className="main">
        <header className="topbar">
          <strong style={{ color: 'var(--text-primary)' }}>{title}</strong>
          <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
            <span style={{ color: 'var(--text-muted)', fontSize: 13 }}>{user?.email}</span>
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
