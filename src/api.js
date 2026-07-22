const API_BASE = '/api';

/**
 * Helper to handle fetch responses.
 * Returns parsed JSON for 2xx responses, otherwise throws an Error.
 * @param {Response} res
 * @returns {Promise<any>}
 */
async function handleResponse(res) {
  const contentType = res.headers.get('content-type') || '';
  const isJson = contentType.includes('application/json');
  if (res.ok) {
    return isJson ? res.json() : res.text();
  }

  // attempt to include server-provided error info
  let details = '';
  try {
    details = isJson ? JSON.stringify(await res.json()) : await res.text();
  } catch {
    details = '<unreadable response body>';
  }
  throw new Error(`Request failed (${res.status} ${res.statusText}): ${details}`);
}

/**
 * Fetch all notes.
 * GET /api/notes
 * @returns {Promise<any>}
 */
export async function fetchNotes() {
  const res = await fetch(`${API_BASE}/notes`, {
    method: 'GET',
    headers: {
      Accept: 'application/json',
    },
  });
  return handleResponse(res);
}

/**
 * Create a new note.
 * POST /api/notes
 * Body: { text: string }
 * @param {string} text
 * @returns {Promise<any>}
 */
export async function createNote(text) {
  const payload = { text };
  const res = await fetch(`${API_BASE}/notes`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Accept: 'application/json',
    },
    body: JSON.stringify(payload),
  });
  return handleResponse(res);
}

/**
 * Mark a note as completed.
 * PUT /api/notes/{id}/complete
 * @param {string} id - UUID of the note
 * @returns {Promise<any>}
 */
export async function completeNote(id) {
  const res = await fetch(`${API_BASE}/notes/${encodeURIComponent(id)}/complete`, {
    method: 'PUT',
    headers: {
      Accept: 'application/json',
    },
  });
  return handleResponse(res);
}

/**
 * Delete a completed note.
 * DELETE /api/notes/{id}
 * @param {string} id - UUID of the note
 * @returns {Promise<any>}
 */
export async function deleteNote(id) {
  const res = await fetch(`${API_BASE}/notes/${encodeURIComponent(id)}`, {
    method: 'DELETE',
    headers: {
      Accept: 'application/json',
    },
  });
  return handleResponse(res);
}
