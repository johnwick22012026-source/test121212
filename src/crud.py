from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import List, Optional, Union

from sqlalchemy.orm import Session

from src.models import Notes


def _ensure_uuid(id: Union[str, uuid.UUID]) -> uuid.UUID:
    """
    Validate and convert input to UUID.
    Raises ValueError if invalid.
    """
    try:
        return uuid.UUID(str(id))
    except (ValueError, TypeError) as exc:
        raise ValueError(f"Invalid UUID: {id}") from exc


def get_all_notes(session: Session) -> List[Notes]:
    """
    Retrieve all notes ordered newest-first (created_at DESC).

    Returns:
        List[Notes]: SQLAlchemy Notes instances ordered by created_at desc.
    """
    return session.query(Notes).order_by(Notes.created_at.desc()).all()


def create_note(session: Session, text: str) -> Notes:
    """
    Create a new note with the provided text.

    Validations:
    - text must be non-empty and not only whitespace
    - max length 500 characters

    Returns:
        Notes: The created Notes instance (refreshed from DB)

    Raises:
        ValueError: if validation fails
        Exception: on DB commit failure (session will be rolled back)
    """
    if text is None:
        raise ValueError("Note text is required.")
    cleaned = text.strip()
    if not cleaned:
        raise ValueError("Note text must not be empty or whitespace.")
    if len(cleaned) > 500:
        raise ValueError("Note text must be 500 characters or fewer.")

    note = Notes(text=cleaned)
    session.add(note)
    try:
        session.commit()
        session.refresh(note)
    except Exception:
        session.rollback()
        raise
    return note


def complete_note(session: Session, id: Union[str, uuid.UUID]) -> Notes:
    """
    Mark a note as completed and set completed_at timestamp.

    Args:
        id: UUID (or string) of the note.

    Returns:
        Notes: The updated Notes instance.

    Raises:
        ValueError: if id is not a valid UUID
        LookupError: if note with given id does not exist
        Exception: on DB commit failure (session will be rolled back)
    """
    note_id = _ensure_uuid(id)
    note: Optional[Notes] = session.get(Notes, note_id)
    if note is None:
        raise LookupError(f"Note not found: {note_id}")

    # If already completed, update completed_at if missing; else set both.
    note.is_completed = True
    note.completed_at = datetime.now(timezone.utc)

    session.add(note)
    try:
        session.commit()
        session.refresh(note)
    except Exception:
        session.rollback()
        raise
    return note


def delete_note(session: Session, id: Union[str, uuid.UUID]) -> None:
    """
    Delete a note. Only completed notes may be deleted.

    Args:
        id: UUID (or string) of the note.

    Raises:
        ValueError: if id is not a valid UUID or note is not completed
        LookupError: if note with given id does not exist
        Exception: on DB commit failure (sess