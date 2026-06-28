import { useEffect, useRef, useState } from 'react'
import AppLayout from '../../components/common/AppLayout'
import { submittalService, statusStyle } from '../../services/submittalService'
import { templateService } from '../../services/templateService'
import { productService } from '../../services/productService'
import { apiError } from '../../services/api'

function GeneratePanel({ onClose, onDone }) {
  const [templates, setTemplates] = useState([])
  const [products, setProducts] = useState([])
  const [form, setForm] = useState({ template_id: '', product_id: '', project_name: '', project_code: '', consultant_id: '' })
  const [error, setError] = useState('')
  const [progress, setProgress] = useState(null) // {pct, message}
  const timer = useRef(null)

  useEffect(() => {
    templateService.list({ page_size: 100 }).then((d) => setTemplates(d.templates || []))
    productService.list({ page_size: 100 }).then((d) => setProducts(d.products || []))
    return () => clearTimeout(timer.current)
  }, [])

  const set = (k) => (e) => setForm((f) => ({ ...f, [k]: e.target.value }))

  const poll = (taskId) => {
    submittalService
      .taskStatus(taskId)
      .then((s) => {
        setProgress({ pct: s.progress, message: s.message })
        if (s.status === 'completed') return onDone()
        if (s.status === 'failed') {
          setError('Generation failed. Check the worker logs.')
          setProgress(null)
          return
        }
        timer.current = setTimeout(() => poll(taskId), 1200)
      })
      .catch(() => {
        timer.current = setTimeout(() => poll(taskId), 1500)
      })
  }

  const submit = async () => {
    setError('')
    if (!form.template_id || !form.product_id)
      return setError('Template and product are required.')
    setProgress({ pct: 5, message: 'Queuing…' })
    try {
      const res = await submittalService.generate({
        template_id: Number(form.template_id),
        product_id: Number(form.product_id),
        project_name: form.project_name || null,
        project_code: form.project_code || null,
        consultant_id: form.consultant_id || null,
      })
      poll(res.task_id)
    } catch (e) {
      setProgress(null)
      setError(apiError(e, 'Could not start generation.'))
    }
  }

  return (
    <div className="card" style={{ marginTop: 24 }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <strong style={{ color: 'var(--text-primary)' }}>Generate submittal</strong>
        <button className="btn btn-secondary" style={{ height: 32 }} onClick={onClose}>Close</button>
      </div>

      {error && <div className="alert-error" style={{ marginTop: 16 }}>{error}</div>}

      <div className="gen-grid">
        <div className="field">
          <label>Template *</label>
          <select className="input" value={form.template_id} onChange={set('template_id')}>
            <option value="">— Select —</option>
            {templates.map((t) => <option key={t.id} value={t.id}>{t.name} (v{t.version})</option>)}
          </select>
        </div>
        <div className="field">
          <label>Product *</label>
          <select className="input" value={form.product_id} onChange={set('product_id')}>
            <option value="">— Select —</option>
            {products.map((p) => <option key={p.id} value={p.id}>{p.name}</option>)}
          </select>
        </div>
        <div className="field">
          <label>Project name</label>
          <input className="input" value={form.project_name} onChange={set('project_name')} placeholder="Downtown Office Complex" />
        </div>
        <div className="field">
          <label>Project code</label>
          <input className="input" value={form.project_code} onChange={set('project_code')} placeholder="DOC-2026-001" />
        </div>
        <div className="field">
          <label>Consultant ID</label>
          <input className="input" value={form.consultant_id} onChange={set('consultant_id')} placeholder="CONS-001" />
        </div>
      </div>

      {progress ? (
        <div style={{ marginTop: 8 }}>
          <div className="progress-bar"><div className="progress-fill" style={{ width: `${progress.pct}%` }} /></div>
          <div style={{ fontSize: 13, color: 'var(--text-muted)', marginTop: 6 }}>{progress.message} ({progress.pct}%)</div>
        </div>
      ) : (
        <button className="btn btn-primary" style={{ marginTop: 8 }} onClick={submit}>Generate</button>
      )}
    </div>
  )
}

export default function SubmittalsPage() {
  const [data, setData] = useState(null)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)
  const [showGen, setShowGen] = useState(false)

  const load = () => {
    setLoading(true)
    submittalService.list().then(setData).catch((e) => setError(apiError(e))).finally(() => setLoading(false))
  }
  useEffect(load, [])

  const [busyId, setBusyId] = useState(null)

  const onDone = () => { setShowGen(false); load() }

  const download = async (s) => {
    try { await submittalService.download(s.id, s.submission_number) }
    catch (e) { setError(apiError(e, 'Download failed.')) }
  }

  const regenerate = async (s) => {
    setBusyId(s.id)
    setError('')
    try {
      const res = await submittalService.regenerate(s.id)
      // Poll the task to completion, then refresh the list.
      const poll = async () => {
        const st = await submittalService.taskStatus(res.task_id)
        if (st.status === 'completed' || st.status === 'failed') {
          setBusyId(null)
          load()
        } else {
          setTimeout(poll, 1200)
        }
      }
      poll()
    } catch (e) {
      setBusyId(null)
      setError(apiError(e, 'Regeneration failed.'))
    }
  }

  return (
    <AppLayout title="Submittals">
      <div className="page-head">
        <div>
          <h1>Submittals</h1>
          <p style={{ color: 'var(--text-muted)', marginTop: 4 }}>Generate and download consultant-ready submittal packages.</p>
        </div>
        {!showGen && <button className="btn btn-primary" onClick={() => setShowGen(true)}>+ Generate submittal</button>}
      </div>

      {error && <div className="alert-error" style={{ marginTop: 16 }}>{error}</div>}
      {showGen && <GeneratePanel onClose={() => setShowGen(false)} onDone={onDone} />}

      <div className="card" style={{ marginTop: 24, padding: 0, overflow: 'hidden' }}>
        {loading ? (
          <div style={{ padding: 24, color: 'var(--text-muted)' }}>Loading…</div>
        ) : !data?.submittals?.length ? (
          <div style={{ padding: 32, textAlign: 'center', color: 'var(--text-muted)' }}>
            No submittals yet. Generate your first one above.
          </div>
        ) : (
          <table className="table">
            <thead>
              <tr><th>Submission</th><th>Project</th><th>Status</th><th>Pages</th><th>Created</th><th></th></tr>
            </thead>
            <tbody>
              {data.submittals.map((s) => {
                const st = statusStyle(s.status)
                return (
                  <tr key={s.id}>
                    <td><strong style={{ color: 'var(--text-primary)' }}>{s.submission_number}</strong></td>
                    <td style={{ color: 'var(--text-muted)' }}>{s.project_name || '—'}</td>
                    <td><span className="badge" style={{ background: st.bg, color: st.color }}>{st.label}</span></td>
                    <td>{s.page_count ?? '—'}</td>
                    <td style={{ color: 'var(--text-muted)' }}>{new Date(s.created_at).toLocaleDateString()}</td>
                    <td style={{ textAlign: 'right', whiteSpace: 'nowrap' }}>
                      <button
                        className="btn btn-secondary"
                        style={{ height: 32, padding: '0 12px' }}
                        disabled={busyId === s.id || s.status === 'generating'}
                        onClick={() => regenerate(s)}
                        title="Re-assemble the PDF (includes approved compliance statements)"
                      >
                        {busyId === s.id ? 'Regenerating…' : 'Regenerate'}
                      </button>
                      <button
                        className="btn btn-secondary"
                        style={{ height: 32, padding: '0 12px', marginLeft: 8 }}
                        disabled={s.status !== 'generated'}
                        onClick={() => download(s)}
                      >
                        Download PDF
                      </button>
                    </td>
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
