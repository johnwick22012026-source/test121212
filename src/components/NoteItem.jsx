import React from "react";
import PropTypes from "prop-types";

/**
 * Presentational component that renders a single note row.
 *
 * Props:
 * - note: { id, text, is_completed, created_at }
 * - toggleComplete: (id: string) => void
 * - onDeleteConfirm: (id: string) => void
 *
 * Notes:
 * - Strike-through style applied when note.is_completed is true.
 * - Delete button is disabled until the note is completed (per requirements).
 * - Date displayed via toLocaleString.
 */
export default function NoteItem({ note, toggleComplete, onDeleteConfirm }) {
  const { id, text, is_completed = false, created_at } = note ?? {};

  function formatDate(iso) {
    if (!iso) return "Unknown";
    const d = new Date(iso);
    if (Number.isNaN(d.getTime())) return "Invalid date";
    return d.toLocaleString();
  }

  return (
    <div
      className="note-item"
      role="listitem"
      aria-labelledby={`note-text-${id}`}
      style={{
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        padding: "10px 12px",
        borderBottom: "1px solid #e8e8e8",
        gap: 12,
      }}
    >
      <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
        <input
          type="checkbox"
          aria-label={is_completed ? "Mark as not completed" : "Mark as completed"}
          checked={Boolean(is_completed)}
          onChange={() => toggleComplete(id)}
        />

        <div>
          <div
            id={`note-text-${id}`}
            className={`note-text ${is_completed ? "completed" : ""}`}
            style={{
              fontSize: 16,
              lineHeight: 1.3,
              textDecoration: is_completed ? "line-through" : "none",
              color: is_completed ? "#6b6b6b" : "#111827",
              maxWidth: 520,
              wordBreak: "break-word",
            }}
          >
            {text}
          </div>

          <div
            className="note-meta"
            style={{ fontSize: 12, color: "#6b6b6b", marginTop: 6 }}
            aria-hidden="true"
          >
            {formatDate(created_at)}
          </div>
        </div>
      </div>

      <div>
        <button
          type="button"
          onClick={() => onDeleteConfirm(id)}
          disabled={!is_completed}
          aria-disabled={!is_completed}
          aria-label="Delete note"
          title={is_completed ? "Delete note" : "Complete the note to enable delete"}
          style={{
            background: "transparent",
            border: "none",
            padding: 6,
            fontSize: 18,
            lineHeight: 1,
            cursor: is_completed ? "pointer" : "not-allowed",
            color: is_completed ? "#b91c1c" : "#9ca3af",
          }}
        >
          🗑
        </button>
      </div>
    </div>
  );
}

NoteItem.propTypes = {
  note: PropTypes.shape({
    id: PropTypes.string.isRequired,
    text: PropTypes.string.isRequired,
    is_completed: PropTypes.bool,
    created_at: PropTypes.