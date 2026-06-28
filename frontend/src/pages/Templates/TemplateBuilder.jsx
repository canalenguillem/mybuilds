import { useEffect, useRef, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import AppLayout from '../../components/common/AppLayout'
import { templateService } from '../../services/templateService'
import { productService } from '../../services/productService'
import { apiError } from '../../services/api'

const SECTION_TYPES = [
  { value: 'static_document', label: 'Static document' },
  { value: 'dynamic_compliance', label: 'Dynamic compliance' },
  { value: 'custom_html', label: 'Custom HTML' },
]

let TMP = 0
const tmpId = () => `tmp-${++TMP}`

export default function TemplateBuilder() {
  const { id } = useParams()
  const isEdit = Boolean(id)
  const navigate = useNavigate()

  const [name, setName] = useState('')
  const [productId, setProductId] = useState('')
  const [consultantId, setConsultantId] = useState('')
  const [templateType, setTemplateType] = useState('product_generic')
  const [sections, setSections] = useState([])
  const [products, setProducts] = useState([])
  const [productDocs, setProductDocs] = useState([])
  const [error, setError] = useState('')
  const [saving, setSaving] = useState(false)
  const [loading, setLoading] = useState(isEdit)
  const dragIndex = useRef(null)

  // Load product list + (if editing) the template.
  useEffect(() => {
    productService.list({ page_size: 100 }).then((d) => setProducts(d.products || []))
    if (isEdit) {
      templateService
        .get(id)
        .then((t) => {
          setName(t.name)
          setProductId(t.product_id ? String(t.product_id) : '')
          setConsultantId(t.consultant_id || '')
          setTemplateType(t.template_type || 'product_generic')
          setSections(
            (t.sections || []).map((s) => ({
              key: tmpId(),
              section_name: s.section_name,
              section_type: s.section_type || 'static_document',
              document_ids: s.document_ids || [],
              is_mandatory: s.is_mandatory,
            }))
          )
        })
        .catch((e) => setError(apiError(e, 'Failed to load template.')))
        .finally(() => setLoading(false))
    }
  }, [id, isEdit])

  // Load the selected product's documents (flattened) for the picker.
  useEffect(() => {
    if (!productId) return setProductDocs([])
    productService
      .documents(productId)
      .then((d) => setProductDocs(Object.values(d.documents || {}).flat()))
      .catch(() => setProductDocs([]))
  }, [productId])

  const addSection = () =>
    setSections((s) => [
      ...s,
      { key: tmpId(), section_name: '', section_type: 'static_document', document_ids: [], is_mandatory: true },
    ])

  const updateSection = (key, patch) =>
    setSections((s) => s.map((sec) => (sec.key === key ? { ...sec, ...patch } : sec)))

  const removeSection = (key) => setSections((s) => s.filter((sec) => sec.key !== key))

  const onDrop = (index) => {
    const from = dragIndex.current
    if (from === null || from === index) return
    setSections((s) => {
      const next = [...s]
      const [moved] = next.splice(from, 1)
      next.splice(index, 0, moved)
      return next
    })
    dragIndex.current = null
  }

  const toggleDoc = (key, docId, current) => {
    const set = new Set(current)
    set.has(docId) ? set.delete(docId) : set.add(docId)
    updateSection(key, { document_ids: [...set] })
  }

  const save = async () => {
    setError('')
    if (!name.trim()) return setError('Template name is required.')
    if (!sections.length) return setError('Add at least one section.')
    if (sections.some((s) => !s.section_name.trim()))
      return setError('Every section needs a name.')

    const payload = {
      name: name.trim(),
      product_id: productId ? Number(productId) : null,
      consultant_id: consultantId.trim() || null,
      template_type: templateType,
      sections: sections.map((s, i) => ({
        section_name: s.section_name.trim(),
        section_order: i + 1,
        section_type: s.section_type,
        document_ids: s.document_ids,
        is_mandatory: s.is_mandatory,
      })),
    }
    setSaving(true)
    try {
      if (isEdit) await templateService.update(id, payload)
      else await templateService.create(payload)
      navigate('/templates')
    } catch (e) {
      setError(apiError(e, 'Save failed.'))
    } finally {
      setSaving(false)
    }
  }

  if (loading)
    return (
      <AppLayout title="Template builder">
        <div style={{ color: 'var(--text-muted)' }}>Loading…</div>
      </AppLayout>
    )

  return (
    <AppLayout title="Template builder">
      <div className="page-head">
        <h1>{isEdit ? 'Edit template' : 'New template'}</h1>
        <div style={{ display: 'flex', gap: 8 }}>
          <button className="btn btn-secondary" onClick={() => navigate('/templates')}>
            Cancel
          </button>
          <button className="btn btn-primary" onClick={save} disabled={saving}>
            {saving ? <span className="spinner" /> : isEdit ? 'Save changes' : 'Create template'}
          </button>
        </div>
      </div>

      {error && <div className="alert-error" style={{ marginTop: 16 }}>{error}</div>}

      <div className="builder-grid">
        {/* Settings */}
        <div className="card">
          <strong style={{ color: 'var(--text-primary)' }}>Settings</strong>
          <div className="field" style={{ marginTop: 16 }}>
            <label>Name *</label>
            <input className="input" value={name} onChange={(e) => setName(e.target.value)} placeholder="e.g. HVAC System Submittal" />
          </div>
          <div className="field">
            <label>Product</label>
            <select className="input" value={productId} onChange={(e) => setProductId(e.target.value)}>
              <option value="">— None —</option>
              {products.map((p) => (
                <option key={p.id} value={p.id}>{p.name}</option>
              ))}
            </select>
          </div>
          <div className="field">
            <label>Consultant ID</label>
            <input className="input" value={consultantId} onChange={(e) => setConsultantId(e.target.value)} placeholder="e.g. CONS-001" />
          </div>
          <div className="field">
            <label>Template type</label>
            <select className="input" value={templateType} onChange={(e) => setTemplateType(e.target.value)}>
              <option value="product_generic">Product generic</option>
              <option value="consultant_specific">Consultant specific</option>
              <option value="custom">Custom</option>
            </select>
          </div>
        </div>

        {/* Sections */}
        <div className="card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <strong style={{ color: 'var(--text-primary)' }}>Sections</strong>
            <button className="btn btn-secondary" style={{ height: 34 }} onClick={addSection}>
              + Add section
            </button>
          </div>
          <p style={{ color: 'var(--text-muted)', fontSize: 13, margin: '8px 0 16px' }}>
            Drag the ⠿ handle to reorder. Order here is the order in the generated PDF.
          </p>

          {!sections.length && (
            <div style={{ color: 'var(--text-faint)', padding: '12px 0' }}>No sections yet.</div>
          )}

          {sections.map((s, i) => (
            <div
              key={s.key}
              className="section-row"
              draggable
              onDragStart={() => (dragIndex.current = i)}
              onDragOver={(e) => e.preventDefault()}
              onDrop={() => onDrop(i)}
            >
              <div className="section-head">
                <span className="drag-handle" title="Drag to reorder">⠿</span>
                <span className="section-order">{i + 1}</span>
                <input
                  className="input"
                  style={{ flex: 1 }}
                  placeholder="Section name"
                  value={s.section_name}
                  onChange={(e) => updateSection(s.key, { section_name: e.target.value })}
                />
                <select
                  className="input"
                  style={{ width: 180 }}
                  value={s.section_type}
                  onChange={(e) => updateSection(s.key, { section_type: e.target.value })}
                >
                  {SECTION_TYPES.map((t) => (
                    <option key={t.value} value={t.value}>{t.label}</option>
                  ))}
                </select>
                <button
                  className="btn btn-secondary"
                  style={{ height: 40, color: 'var(--error)' }}
                  onClick={() => removeSection(s.key)}
                >
                  Remove
                </button>
              </div>

              {s.section_type === 'static_document' && (
                <div className="doc-picker">
                  {!productId ? (
                    <span style={{ color: 'var(--text-faint)', fontSize: 13 }}>
                      Select a product to attach its documents.
                    </span>
                  ) : !productDocs.length ? (
                    <span style={{ color: 'var(--text-faint)', fontSize: 13 }}>
                      This product has no documents yet.
                    </span>
                  ) : (
                    productDocs.map((d) => (
                      <label key={d.id} className="doc-chip">
                        <input
                          type="checkbox"
                          checked={s.document_ids.includes(d.id)}
                          onChange={() => toggleDoc(s.key, d.id, s.document_ids)}
                        />
                        {d.title}
                      </label>
                    ))
                  )}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </AppLayout>
  )
}
