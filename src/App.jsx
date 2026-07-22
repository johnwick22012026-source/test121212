import React, { useEffect, useState, useRef } from "react";
import {
  listNotes,
  createNote,
  completeNote,
  deleteNote,
} from "./api";

/**
 * Single-page TODO Notes Application UI
 *
 * - Uses functions imported from './api' for network operations:
 *   listNotes(), createNote({ text }), completeNote(id), deleteNote(id)
 *
 * - Features:
 *   - Title
 *   - Input + Add button (Add on click or Enter)
 *   - Search box (real-time, case-insensitive)
 *   - Notes list (newest first)
 *   - Complete checkbox (marks completed, strike-through, records completed timestamp)
 *   - Delete button (only for completed notes) with in-UI confirmation dialog
 *
 * Notes shape assumed from backend:
 * {
 *   id: string,
 *   text: string,
 *   is_completed: boolean,
 *   created_at: string (ISO),
 *   completed_at: string | null (ISO)
 * }
 */

function formatDateTime(iso) {
  if (!iso) return "";
  try {
    const d = new Date(iso);
    return d.toLocaleString();
  } catch {
    return iso;
  }
}

export default function App() {
  const [notes, setNotes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [input, setInput] = useState("");
  const [adding, setAdding] = useState(false);

  const [search, setSearch] = useState("");

  const [deleteConfirm, setDeleteConfirm] = useState(null); // { id, text } or null
  const confirmButtonRef = useRef(null);

  useEffect(() => {
    fetchNotes();
  }, []);

  useEffect(() => {
    if (deleteConfirm && confirmButtonRef.current) {
      confirmButtonRef.current.focus();
    }
  }, [deleteConfirm]);

  async function fetchNotes() {
    setLoading(true);
    setError(null);
    try {
      const all = await listNotes();
      // Ensure newest first by created_at descending
      const sorted = (all || []).slice().sort((a, b) => {
        const ta = new Date(a.created_at).getTime();
        const tb = new Date(b.created_at).getTime();
        return tb - ta;
      });
      setNotes(sorted);
    } catch (err) {
      setError("Failed to load notes.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  function filteredNotes() {
    if (!search.trim()) return notes;
    const q = search.toLowerCase();
    return notes.filter((n) => (n.text || "").toLowerCase().includes(q));
  }

  async function handleAdd(e) {
    if (e) e.preventDefault();
    const text = input.trim();
    if (!text) return;
    if (text.length > 500) {
      setError("Note must be 500 characters or less.");
      return;
    }
    setAdding(true);
    setError(null);
    try {
      const created = await createNote({ text });
      // If API returned the created note, use it; otherwise build a local fallback
      const note = created || {
        id: String(Date.now()),
        text,
        is_completed: false,
        created_at: new Date().toISOString(),
        completed_at: null,
      };
      setNotes((prev) => [note, ...prev]);
      setInput("
"}]}