import AppLayout from '../components/common/AppLayout'

export default function Placeholder({ title }) {
  return (
    <AppLayout title={title}>
      <h1>{title}</h1>
      <div className="card" style={{ marginTop: 24 }}>
        <p style={{ color: 'var(--text-muted)' }}>
          This screen is part of a later build phase. The backend foundation and
          Templates are ready — this UI is coming next.
        </p>
      </div>
    </AppLayout>
  )
}
