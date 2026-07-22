# test121212 — TODO Notes (Single-page)

Overview

A minimal single-page TODO Notes application. Frontend is a Vite + React SPA; backend is FastAPI (Python) with SQLite for storage. Users can create, complete, search, and delete notes from a single screen. No authentication required.

Tech stack

- Frontend: React (Vite)
- Backend: Python 3.12+, FastAPI
- Database: SQLite
- ORM/DB: SQLAlchemy
- Validation: Pydantic

Repository visibility

This repository is public. NO run test

File structure (key files)

- README.md (this file)
- index.html
- src/
  - App.jsx (main React component)
  - main.jsx (React entry)
  - api.js (frontend API helpers)
  - components/NoteItem.jsx (presentational component)
  - styles.css (styles and responsive layout)
  - main.py (FastAPI app entry)
  - database.py (SQLite engine & session)
  - models.py (SQLAlchemy models)
  - schemas.py (Pydantic schemas)
  - crud.py (DB access functions)

Running the backend (local)

1. Create virtual environment and install dependencies (example using pip):

   python3.12 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt

   If you prefer pnpm/other, adjust accordingly.

2. Create the database tables (optional — the app may auto-create):

   python -c "from src.database import create_tables; create_tables()"

3. Run the FastAPI server (development):

   uvicorn src.main:app --reload --host 127.0.0.1 --port 8000

Running the frontend (local)

1. Install frontend dependencies (npm example):

   npm install

   Or with pnpm:

   pnpm install

2. Run the Vite dev server:

   npm run dev

3. Open the app at the address shown by Vite (typically http://localhost:5173). The frontend expects API under /api — configure proxy or run both servers on same host.

API endpoints

- GET /api/notes — Retrieve all notes (newest first)
- POST /api/notes — Create a new note. Body: { "text": "your note" } (required, max 500 chars)
- PUT /api/notes/{id}/complete — Mark a note as completed
- DELETE /api/notes/{id} — Delete a completed note

Notes and constraints

- The app is a single-page application with no routing.
- Search is real-time and case-insensitive.
- Notes must be non-empty and <= 500 characters.
- Deleting a note requires confirmation.
- Repository is public; do not include any secrets or credentials.
- NO run test — do not configure CI to run tests or include test-run steps in CI.

Troubleshooting / Gotchas

- If the frontend cannot reach the backend, ensure CORS is enabled (the FastAPI app ships with permissive CORS for development).
- For SQLite, ensure write permissions in the project directory for the db file.

Contact

For questions about this repository, open an issue in the GitHub repository: https://github.com/johnwick22012026-source/test121212
