import { Navigate } from 'react-router-dom'
import { useAuth } from '../../context/AuthContext'

export default function ProtectedRoute({ children }) {
  const { user, loading } = useAuth()

  if (loading) {
    return (
      <div style={{ display: 'grid', placeItems: 'center', height: '100vh' }}>
        <div className="spinner" style={{ borderColor: 'rgba(0,102,204,.25)', borderTopColor: 'var(--primary)' }} />
      </div>
    )
  }
  if (!user) return <Navigate to="/login" replace />
  return children
}
