export default function Modal({ title, onClose, children, width = 520 }) {
  return (
    <div className="modal-overlay" onMouseDown={onClose}>
      <div
        className="modal-card"
        style={{ width }}
        onMouseDown={(e) => e.stopPropagation()}
      >
        <div className="modal-head">
          <strong>{title}</strong>
          <button className="icon-btn" onClick={onClose} aria-label="Close">✕</button>
        </div>
        <div className="modal-body">{children}</div>
      </div>
    </div>
  )
}
