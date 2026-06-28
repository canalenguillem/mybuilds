import { useEffect, useRef, useState } from 'react'
import AppLayout from '../../components/common/AppLayout'
import { complianceService, reviewStatusStyle } from '../../services/complianceService'
import { documentService } from '../../services/documentService'
import { productService } from '../../services/productService'
import { apiError } from '../../services/api'

function AnalyzePanel({ onClose, onDone }) {
  const [docs, setDocs] = useState([])
  const [products, setProducts] = useState([])
  const [docId, setDocId] = useState('')
  const [productIds, setProductIds] = useState([])
  const [error, setError] = useState('')
  const [progress, setProgress] = useState(null)
  const timer = useRef(null)

  useEffect(() => {
    documentService.list({ page_size: 100 }).then((d) => setDocs(d.documents || []))
    productService.list({ page_size: 100 }).then((d) => setProducts(d.products || []))
    return () => clearTimeout(timer.current)
  }, [])

  const toggleProduct = (id) =>
    setProductIds((s) => (s.includes(id) ? s.filter((x) => x !== id) : [...s, id]))

  const poll = (taskId) => {
    complianceService
      .taskStatus(taskId)
      .then((s) => {
        setProgress({ pct: s.progress, message: s.message, model: s.ai_model })
        if (s.status === 'completed') return onDone(s)
        if (s.status === 'failed') {
          setError('Analysis failed. Check the worker logs.')
          setProgress(null)
          return
        }
        timer.current = setTimeout(() => poll(taskId), 1200)
      })
      .catch(() => (timer.current = setTimeout(() => poll(taskId), 1500)))
  }

  const submit = async () => {
    setError('')
    if (!docId || !productIds.length)
      return setError('Pick a requirements document and at least one product.')
    setProgress({ pct: 5, message: 'Queuing…' })
    try {
      const res = await complianceService.analyze({
        consultant_requirements_doc_id: Number(docId),
        product_ids: productIds,
      })
      poll(res.task_id)
    } catch (e) {
      setProgress(null)
      setError(apiError(e, 'Could not start analysis.'))
    }
  }

  return (
    <div className="card" style={{ marginTop: 24 }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <strong style={{ color: 'var(--text-primary)' }}>AI compliance analysis</strong>
        <button className="btn btn-secondary" style={{ height: 32 }} onClick={onClose}>Close</button>
      </div>
      <p style={{ color: 'var(--text-muted)', fontSize: 13, margin: '8px 0 16px' }}>
        Reads a consultant requirements PDF, extracts requirements, and drafts compliance
        statements against each product's documents for human review.
      </p>

      {error && <div className="alert-error">{error}</div>}

      <div className="gen-grid">
        <div className="field">
          <label>Requirements document *</label>
          <select className="input" value={docId} onChange={(e) => setDocId(e.target.value)}>
            <option value="">— Select —</option>
            {docs.map((d) => (
              <option key={d.id} value={d.id}>{d.title} ({d.document_type})</option>
            ))}
          </select>
        </div>
        <div className="field">
          <label>Products *</label>
          <div className="doc-picker" style={{ paddingLeft: 0 }}>
            {products.map((p) => (
              <label key={p.id} className="doc-chip">
                <input type="checkbox" checked={productIds.includes(p.id)} onChange={() => toggleProduct(p.id)} />
                {p.name}
              </label>
            ))}
          </div>
        </div>
      </div>

      {progress ? (
        <div style={{ marginTop: 8 }}>
          <div className="progress-bar"><div className="progress-fill" style={{ width: `${progress.pct}%` }} /></div>
          <div style={{ fontSize: 13, color: 'var(--text-muted)', marginTop: 6 }}>
            {progress.message} ({progress.pct}%){progress.model ? ` · model: ${progress.model}` : ''}
          </div>
        </div>
      ) : (
        <button className="btn btn-primary" style={{ marginTop: 8 }} onClick={submit}>Run analysis</button>
      )}
    </div>
  )
}

function StatementRow({ s, onReviewed }) {
  const [open, setOpen] = useState(false)
  const [text, setText] = useState(s.statement)
  const [notes, setNotes] = useState('')
  const [busy, setBusy] = useState(false)
  const st = reviewStatusStyle(s.review_status)

  const review = async (status) => {
    setBusy(true)
    try {
      await complianceService.review(s.id, {
        review_status: status,
        review_notes: notes || null,
        revised_statement: text !== s.statement ? text : null,
      })
      onReviewed()
    } finally {
      setBusy(false)
    }
  }

  return (
    <>
      <tr>
        <td style={{ maxWidth: 520 }}>{s.statement}</td>
        <td>{s.confidence_score != null ? `${Math.round(s.confidence_score * 100)}%` : '—'}</td>
        <td><span className="badge" style={{ background: st.bg, color: st.color }}>{st.label}</span></td>
        <td style={{ textAlign: 'right' }}>
          <button className="btn btn-secondary" style={{ height: 32, padding: '0 14px' }} onClick={() => setOpen((o) => !o)}>
            {open ? 'Cancel' : 'Review'}
          </button>
        </td>
      </tr>
      {open && (
        <tr>
          <td colSpan={4} style={{ background: 'var(--subtle-surface)' }}>
            <div style={{ padding: 8 }}>
              <label style={{ fontSize: 13, fontWeight: 500 }}>Statement (editable)</label>
              <textarea className="input" style={{ height: 80, padding: 10, width: '100%', marginTop: 4 }}
                value={text} onChange={(e) => setText(e.target.value)} />
              <input className="input" style={{ width: '100%', marginTop: 8 }} placeholder="Review notes (optional)"
                value={notes} onChange={(e) => setNotes(e.target.value)} />
              <div style={{ display: 'flex', gap: 8, marginTop: 10 }}>
                <button className="btn btn-primary" disabled={busy} onClick={() => review('approved')}>Approve</button>
                <button className="btn btn-secondary" disabled={busy} onClick={() => review('needs_revision')}>Needs revision</button>
                <button className="btn btn-secondary" style={{ color: 'var(--error)' }} disabled={busy} onClick={() => review('rejected')}>Reject</button>
              </div>
            </div>
          </td>
        </tr>
      )}
    </>
  )
}

export default function CompliancePage() {
  const [data, setData] = useState(null)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)
  const [showAnalyze, setShowAnalyze] = useState(false)
  const [filter, setFilter] = useState('')

  const load = () => {
    setLoading(true)
    const params = filter ? { review_status: filter } : {}
    complianceService.listStatements(params).then(setData).catch((e) => setError(apiError(e))).finally(() => setLoading(false))
  }
  useEffect(load, [filter])

  return (
    <AppLayout title="Compliance">
      <div className="page-head">
        <div>
          <h1>Compliance</h1>
          <p style={{ color: 'var(--text-muted)', marginTop: 4 }}>
            AI-drafted compliance statements for human review.
          </p>
        </div>
        {!showAnalyze && <button className="btn btn-primary" onClick={() => setShowAnalyze(true)}>+ Run AI analysis</button>}
      </div>

      {error && <div className="alert-error" style={{ marginTop: 16 }}>{error}</div>}
      {showAnalyze && <AnalyzePanel onClose={() => setShowAnalyze(false)} onDone={() => { setShowAnalyze(false); load() }} />}

      <div style={{ display: 'flex', gap: 8, marginTop: 24 }}>
        {['', 'pending_review', 'approved', 'rejected', 'needs_revision'].map((f) => (
          <button key={f || 'all'} className={`btn btn-secondary${filter === f ? ' active-filter' : ''}`}
            style={{ height: 32, ...(filter === f ? { borderColor: 'var(--primary)', color: 'var(--primary)' } : {}) }}
            onClick={() => setFilter(f)}>
            {f ? reviewStatusStyle(f).label : 'All'}
          </button>
        ))}
      </div>

      <div className="card" style={{ marginTop: 16, padding: 0, overflow: 'hidden' }}>
        {loading ? (
          <div style={{ padding: 24, color: 'var(--text-muted)' }}>Loading…</div>
        ) : !data?.statements?.length ? (
          <div style={{ padding: 32, textAlign: 'center', color: 'var(--text-muted)' }}>
            No statements yet. Run an AI analysis to generate some.
          </div>
        ) : (
          <table className="table">
            <thead>
              <tr><th>Statement</th><th>Confidence</th><th>Status</th><th></th></tr>
            </thead>
            <tbody>
              {data.statements.map((s) => <StatementRow key={s.id} s={s} onReviewed={load} />)}
            </tbody>
          </table>
        )}
      </div>
    </AppLayout>
  )
}
