import { useEffect, useRef, useState } from 'react'
import AppLayout from '../../components/common/AppLayout'
import Modal from '../../components/common/Modal'
import {
  documentService,
  DOCUMENT_TYPES,
  docTypeStyle,
  formatBytes,
} from '../../services/documentService'
import { productService } from '../../services/productService'
import { apiError } from '../../services/api'

function UploadModal({ products, onClose, onUploaded }) {
  const [form, setForm] = useState({ product_id: '', document_type: 'datasheets', title: '' })
  const [file, setFile] = useState(null)
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)
  const fileRef = useRef()
  const set = (k) => (e) => setForm((f) => ({ ...f, [k]: e.target.value }))

  const submit = async () => {
    setError('')
    if (!file) return setError('Choose a PDF file.')
    if (!form.product_id) return setError('Select a product.')
    if (!form.title.trim()) return setError('Title is required.')
    setBusy(true)
    try {
      await documentService.upload({ ...form, title: form.title.trim(), file })
      onUploaded()
    } catch (e) {
      setError(apiError(e, 'Upload failed.'))
    } finally {
      setBusy(false)
    }
  }

  return (
    <Modal title="Upload document" onClose={onClose} width={600}>
      {error && <div className="alert-error">{error}</div>}
      <div
        className="dropzone"
        onClick={() => fileRef.current?.click()}
        onDragOver={(e) => e.preventDefault()}
        onDrop={(e) => { e.preventDefault(); setFile(e.dataTransfer.files[0]) }}
      >
        <input ref={fileRef} type="file" accept="application/pdf" style={{ display: 'none' }}
          onChange={(e) => setFile(e.target.files[0])} />
        {file ? <b>{file.name}</b> : <span style={{ color: 'var(--text-muted)' }}>Drop a PDF here or click to browse</span>}
      </div>
      <div className="field" style={{ marginTop: 16 }}><label>Product *</label>
        <select className="input" value={form.product_id} onChange={set('product_id')}>
          <option value="">— Select —</option>
          {products.map((p) => <option key={p.id} value={p.id}>{p.name}</option>)}
        </select>
      </div>
      <div className="field"><label>Document type *</label>
        <select className="input" value={form.document_type} onChange={set('document_type')}>
          {DOCUMENT_TYPES.map((t) => <option key={t} value={t}>{t}</option>)}
        </select>
      </div>
      <div className="field"><label>Title *</label>
        <input className="input" value={form.title} onChange={set('title')} placeholder="Rooftop Datasheet v2.1" /></div>
      <div style={{ display: 'flex', justifyContent: 'flex-end', gap: 8, marginTop: 8 }}>
        <button className="btn btn-secondary" onClick={onClose}>Cancel</button>
        <button className="btn btn-primary" onClick={submit} disabled={busy}>{busy ? 'Uploading…' : 'Upload'}</button>
      </div>
    </Modal>
  )
}

function VersionsModal({ doc, onClose }) {
  const [data, setData] = useState(null)
  useEffect(() => { documentService.versions(doc.id).then(setData) }, [doc.id])
  return (
    <Modal title={`Version history — ${doc.title}`} onClose={onClose}>
      {!data ? 'Loading…' : (
        <table className="table">
          <thead><tr><th>Version</th><th>Size</th><th>Changed by</th><th>Reason</th></tr></thead>
          <tbody>
            {data.versions.map((v) => (
              <tr key={v.version}>
                <td>v{v.version}{v.version === data.current_version ? ' (current)' : ''}</td>
                <td>{formatBytes(v.file_size)}</td>
                <td>{v.changed_by || '—'}</td>
                <td style={{ color: 'var(--text-muted)' }}>{v.change_reason || '—'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </Modal>
  )
}

function TypeBadge({ type }) {
  const s = docTypeStyle(type)
  return <span className="badge" style={{ background: s.bg, color: s.color }}>{type}</span>
}

export default function DocumentsPage() {
  const [data, setData] = useState(null)
  const [products, setProducts] = useState([])
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)
  const [view, setView] = useState('list')
  const [filters, setFilters] = useState({ product_id: '', document_type: '', search: '' })
  const [showUpload, setShowUpload] = useState(false)
  const [versionsDoc, setVersionsDoc] = useState(null)

  const load = () => {
    setLoading(true)
    const params = {}
    if (filters.product_id) params.product_id = filters.product_id
    if (filters.document_type) params.document_type = filters.document_type
    if (filters.search) params.search = filters.search
    documentService.list(params).then(setData).catch((e) => setError(apiError(e))).finally(() => setLoading(false))
  }

  useEffect(() => { productService.list({ page_size: 100 }).then((d) => setProducts(d.products || [])) }, [])
  useEffect(load, [filters.product_id, filters.document_type, filters.search])

  const productName = (id) => products.find((p) => p.id === id)?.name || `#${id}`
  const set = (k) => (e) => setFilters((f) => ({ ...f, [k]: e.target.value }))

  const onDelete = async (d) => {
    if (!window.confirm(`Delete "${d.title}"? This removes all versions.`)) return
    try { await documentService.remove(d.id); load() }
    catch (e) { setError(apiError(e, 'Delete failed.')) }
  }

  return (
    <AppLayout title="Documents">
      <div className="page-head">
        <div>
          <h1>Documents</h1>
          <p style={{ color: 'var(--text-muted)', marginTop: 4 }}>
            Product datasheets, certificates, manuals and more.
          </p>
        </div>
        <button className="btn btn-primary" onClick={() => setShowUpload(true)}>+ Upload</button>
      </div>

      {error && <div className="alert-error" style={{ marginTop: 16 }}>{error}</div>}

      <div className="toolbar">
        <select className="input" style={{ width: 200 }} value={filters.product_id} onChange={set('product_id')}>
          <option value="">All products</option>
          {products.map((p) => <option key={p.id} value={p.id}>{p.name}</option>)}
        </select>
        <select className="input" style={{ width: 180 }} value={filters.document_type} onChange={set('document_type')}>
          <option value="">All types</option>
          {DOCUMENT_TYPES.map((t) => <option key={t} value={t}>{t}</option>)}
        </select>
        <input className="input" style={{ flex: 1, minWidth: 160 }} placeholder="Search title…"
          value={filters.search} onChange={set('search')} />
        <div className="view-toggle">
          <button className={view === 'list' ? 'active' : ''} onClick={() => setView('list')}>List</button>
          <button className={view === 'grid' ? 'active' : ''} onClick={() => setView('grid')}>Grid</button>
        </div>
      </div>

      {showUpload && <UploadModal products={products} onClose={() => setShowUpload(false)} onUploaded={() => { setShowUpload(false); load() }} />}
      {versionsDoc && <VersionsModal doc={versionsDoc} onClose={() => setVersionsDoc(null)} />}

      {loading ? (
        <div className="card" style={{ marginTop: 16, color: 'var(--text-muted)' }}>Loading…</div>
      ) : !data?.documents?.length ? (
        <div className="card" style={{ marginTop: 16, textAlign: 'center', color: 'var(--text-muted)', padding: 32 }}>
          No documents found. Upload your first PDF.
        </div>
      ) : view === 'grid' ? (
        <div className="doc-grid">
          {data.documents.map((d) => (
            <div className="card doc-card" key={d.id}>
              <TypeBadge type={d.document_type} />
              <strong style={{ color: 'var(--text-primary)', marginTop: 10, display: 'block' }}>{d.title}</strong>
              <div style={{ color: 'var(--text-muted)', fontSize: 13, marginTop: 4 }}>{productName(d.product_id)}</div>
              <div style={{ color: 'var(--text-faint)', fontSize: 12, marginTop: 8 }}>v{d.version} · {formatBytes(d.file_size)}</div>
              <div style={{ display: 'flex', gap: 8, marginTop: 12 }}>
                <button className="btn btn-secondary" style={{ height: 30, padding: '0 12px' }} onClick={() => setVersionsDoc(d)}>Versions</button>
                <button className="btn btn-secondary" style={{ height: 30, padding: '0 12px', color: 'var(--error)' }} onClick={() => onDelete(d)}>Delete</button>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="card" style={{ marginTop: 16, padding: 0, overflow: 'hidden' }}>
          <table className="table">
            <thead><tr><th>Title</th><th>Type</th><th>Product</th><th>Version</th><th>Size</th><th></th></tr></thead>
            <tbody>
              {data.documents.map((d) => (
                <tr key={d.id}>
                  <td><strong style={{ color: 'var(--text-primary)' }}>{d.title}</strong></td>
                  <td><TypeBadge type={d.document_type} /></td>
                  <td style={{ color: 'var(--text-muted)' }}>{productName(d.product_id)}</td>
                  <td>v{d.version}</td>
                  <td style={{ color: 'var(--text-muted)' }}>{formatBytes(d.file_size)}</td>
                  <td style={{ textAlign: 'right', whiteSpace: 'nowrap' }}>
                    <button className="btn btn-secondary" style={{ height: 32, padding: '0 12px' }} onClick={() => setVersionsDoc(d)}>Versions</button>
                    <button className="btn btn-secondary" style={{ height: 32, padding: '0 12px', marginLeft: 8, color: 'var(--error)' }} onClick={() => onDelete(d)}>Delete</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </AppLayout>
  )
}
