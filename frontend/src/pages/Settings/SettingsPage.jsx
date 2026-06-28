import { useEffect, useState } from 'react'
import AppLayout from '../../components/common/AppLayout'
import { useAuth } from '../../context/AuthContext'
import { settingsService } from '../../services/settingsService'
import { apiError } from '../../services/api'

const TABS = ['Profile', 'Integrations']

function ProfileTab() {
  const { user } = useAuth()
  return (
    <div className="card" style={{ maxWidth: 560 }}>
      <strong style={{ color: 'var(--text-primary)' }}>Profile</strong>
      <div className="kv" style={{ marginTop: 16 }}>
        <div><span>Username</span><b>{user?.username}</b></div>
        <div><span>Email</span><b>{user?.email}</b></div>
        <div><span>Roles</span><b>{user?.roles?.join(', ') || '—'}</b></div>
      </div>
      <p style={{ color: 'var(--text-muted)', fontSize: 13, marginTop: 16 }}>
        Profile editing (name, password, 2FA) is part of a later build phase.
      </p>
    </div>
  )
}

function IntegrationsTab() {
  const { user } = useAuth()
  const isAdmin = user?.roles?.includes('admin')
  const [cfg, setCfg] = useState(null)
  const [apiKey, setApiKey] = useState('')
  const [model, setModel] = useState('gpt-4o-mini')
  const [msg, setMsg] = useState(null) // {ok, text}
  const [busy, setBusy] = useState(false)

  const load = () =>
    settingsService.getIntegrations().then((c) => {
      setCfg(c)
      setModel(c.openai_model || 'gpt-4o-mini')
    })
  useEffect(() => { load() }, [])

  const save = async () => {
    setBusy(true); setMsg(null)
    try {
      const payload = { openai_model: model }
      if (apiKey) payload.openai_api_key = apiKey
      await settingsService.updateIntegrations(payload)
      setApiKey('')
      await load()
      setMsg({ ok: true, text: 'Saved.' })
    } catch (e) {
      setMsg({ ok: false, text: apiError(e, 'Save failed (admin only).') })
    } finally { setBusy(false) }
  }

  const clearKey = async () => {
    setBusy(true); setMsg(null)
    try {
      await settingsService.updateIntegrations({ openai_api_key: '' })
      await load()
      setMsg({ ok: true, text: 'Key cleared.' })
    } catch (e) {
      setMsg({ ok: false, text: apiError(e) })
    } finally { setBusy(false) }
  }

  const test = async () => {
    setBusy(true); setMsg(null)
    try {
      const r = await settingsService.testIntegrations()
      setMsg({ ok: r.ok, text: r.message })
    } catch (e) {
      setMsg({ ok: false, text: apiError(e) })
    } finally { setBusy(false) }
  }

  if (!cfg) return <div className="card">Loading…</div>

  return (
    <div className="card" style={{ maxWidth: 640 }}>
      <strong style={{ color: 'var(--text-primary)' }}>OpenAI integration</strong>
      <p style={{ color: 'var(--text-muted)', fontSize: 13, margin: '6px 0 16px' }}>
        Used to draft compliance statements. Your key is stored securely on the server and
        never shown again in full.
      </p>

      <div className="kv" style={{ marginBottom: 16 }}>
        <div>
          <span>Status</span>
          <b style={{ color: cfg.openai_configured ? 'var(--success-text)' : 'var(--text-muted)' }}>
            {cfg.openai_configured ? `Configured (${cfg.openai_source})` : 'Not configured'}
          </b>
        </div>
        {cfg.openai_key_masked && (
          <div><span>Current key</span><b>{cfg.openai_key_masked}</b></div>
        )}
      </div>

      <div className="field">
        <label>API key {cfg.openai_configured ? '(leave blank to keep current)' : ''}</label>
        <input className="input" type="password" placeholder="sk-…" value={apiKey}
          onChange={(e) => setApiKey(e.target.value)} disabled={!isAdmin} />
      </div>
      <div className="field">
        <label>Model</label>
        <input className="input" value={model} onChange={(e) => setModel(e.target.value)} disabled={!isAdmin}
          placeholder="gpt-4o-mini" />
      </div>

      {!isAdmin && (
        <div className="alert-error" style={{ background: 'var(--warning-bg)', color: 'var(--warning)', border: 'none' }}>
          Only admins can change integration settings.
        </div>
      )}

      {msg && (
        <div style={{
          marginTop: 4, marginBottom: 12, fontSize: 13,
          color: msg.ok ? 'var(--success-text)' : 'var(--error)',
        }}>{msg.text}</div>
      )}

      <div style={{ display: 'flex', gap: 8 }}>
        <button className="btn btn-primary" onClick={save} disabled={busy || !isAdmin}>Save</button>
        <button className="btn btn-secondary" onClick={test} disabled={busy || !isAdmin}>Test connection</button>
        {cfg.openai_source === 'database' && (
          <button className="btn btn-secondary" style={{ color: 'var(--error)' }} onClick={clearKey} disabled={busy || !isAdmin}>
            Clear key
          </button>
        )}
      </div>
    </div>
  )
}

export default function SettingsPage() {
  const [tab, setTab] = useState('Integrations')
  return (
    <AppLayout title="Settings">
      <h1>Settings</h1>
      <div className="tabs" style={{ margin: '16px 0 24px' }}>
        {TABS.map((t) => (
          <button key={t} className={`tab${tab === t ? ' active' : ''}`} onClick={() => setTab(t)}>{t}</button>
        ))}
      </div>
      {tab === 'Profile' ? <ProfileTab /> : <IntegrationsTab />}
    </AppLayout>
  )
}
