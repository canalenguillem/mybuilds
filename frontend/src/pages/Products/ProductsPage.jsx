import { useEffect, useState } from 'react'
import AppLayout from '../../components/common/AppLayout'
import Modal from '../../components/common/Modal'
import { productService } from '../../services/productService'
import { apiError } from '../../services/api'

function CreateModal({ onClose, onCreated }) {
  const [form, setForm] = useState({ name: '', category: '', sku: '', description: '' })
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)
  const set = (k) => (e) => setForm((f) => ({ ...f, [k]: e.target.value }))

  const submit = async () => {
    setError('')
    if (!form.name.trim()) return setError('Name is required.')
    setBusy(true)
    try {
      await productService.create({
        name: form.name.trim(),
        category: form.category.trim() || null,
        sku: form.sku.trim() || null,
        description: form.description.trim() || null,
      })
      onCreated()
    } catch (e) {
      setError(apiError(e, 'Create failed.'))
    } finally {
      setBusy(false)
    }
  }

  return (
    <Modal title="New product" onClose={onClose}>
      {error && <div className="alert-error">{error}</div>}
      <div className="field"><label>Name *</label>
        <input className="input" value={form.name} onChange={set('name')} placeholder="HVAC Rooftop Unit" autoFocus /></div>
      <div className="field"><label>Category</label>
        <input className="input" value={form.category} onChange={set('category')} placeholder="HVAC" /></div>
      <div className="field"><label>SKU</label>
        <input className="input" value={form.sku} onChange={set('sku')} placeholder="PRD-HVAC-001" /></div>
      <div className="field"><label>Description</label>
        <input className="input" value={form.description} onChange={set('description')} /></div>
      <div style={{ display: 'flex', justifyContent: 'flex-end', gap: 8, marginTop: 8 }}>
        <button className="btn btn-secondary" onClick={onClose}>Cancel</button>
        <button className="btn btn-primary" onClick={submit} disabled={busy}>Create</button>
      </div>
    </Modal>
  )
}

export default function ProductsPage() {
  const [data, setData] = useState(null)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)
  const [showCreate, setShowCreate] = useState(false)

  const load = () => {
    setLoading(true)
    productService.list({ page_size: 100 }).then(setData).catch((e) => setError(apiError(e))).finally(() => setLoading(false))
  }
  useEffect(load, [])

  return (
    <AppLayout title="Products">
      <div className="page-head">
        <div>
          <h1>Products</h1>
          <p style={{ color: 'var(--text-muted)', marginTop: 4 }}>
            Each product groups its datasheets, certificates and templates.
          </p>
        </div>
        <button className="btn btn-primary" onClick={() => setShowCreate(true)}>+ New product</button>
      </div>

      {error && <div className="alert-error" style={{ marginTop: 16 }}>{error}</div>}
      {showCreate && <CreateModal onClose={() => setShowCreate(false)} onCreated={() => { setShowCreate(false); load() }} />}

      <div className="card" style={{ marginTop: 24, padding: 0, overflow: 'hidden' }}>
        {loading ? (
          <div style={{ padding: 24, color: 'var(--text-muted)' }}>Loading…</div>
        ) : !data?.products?.length ? (
          <div style={{ padding: 32, textAlign: 'center', color: 'var(--text-muted)' }}>
            No products yet. Create one to start uploading documents.
          </div>
        ) : (
          <table className="table">
            <thead><tr><th>Name</th><th>Category</th><th>SKU</th><th>Documents</th><th>Templates</th></tr></thead>
            <tbody>
              {data.products.map((p) => (
                <tr key={p.id}>
                  <td><strong style={{ color: 'var(--text-primary)' }}>{p.name}</strong></td>
                  <td style={{ color: 'var(--text-muted)' }}>{p.category || '—'}</td>
                  <td style={{ color: 'var(--text-muted)' }}>{p.sku || '—'}</td>
                  <td>{p.document_count}</td>
                  <td>{p.templates_count}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </AppLayout>
  )
}
