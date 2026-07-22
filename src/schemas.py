from __future__ import annotations

from typing import Optional
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, Field, field_validator, ConfigDict


class NoteCreate(BaseModel):
    """
    Schema for creating a new note.
    - text: required, non-empty (no whitespace-only), max length 500
    """
    model_config = ConfigDict(extra="forbid")

    text: str = Field(
        ...,
        max_length=500,
        description="Note content (required, max 500 characters)",
        example="Buy groceries",
    )

    @field_validator("text")
    @classmethod
    def _validate_text(cls, v: str) -> str:
        if not isinstance(v, str):
            raise TypeError("text must be a string")
        v_stripped = v.strip()
        if not v_stripped:
            raise ValueError("text must not be empty or whitespace-only")
        if len(v_stripped) > 500:
            raise ValueError("text must be at most 500 characters")
        return v_stripped


class NoteRead(BaseModel):
    """
    Schema returned by the API for a note.
    Includes id, text, is_completed, created_at, completed_at.
    """
    # allow population from ORM objects or DB rows with attributes
    model_config = ConfigDict(from_attributes=True)

    id: UUID = Field(..., description="UUID of the note")
    text: str = Field(..., description="Note content")
    is_completed: bool = Field(False, description="Whether the note is completed")
    created_at: datetime = Field(..., description="Creation timestamp in ISO 8601")
    completed_at: Optional[datetime] = Field(
        None, description="Completion timestamp in ISO 8601, if completed"
    )


class NoteUpdate(BaseModel):
    """
    Optional schema for partial updates to a note.
    - text: optional, if provided must be non-empty (no whitespace-only) and <= 500 chars
    - is_completed: optional boolean
    """
    model_config = ConfigDict(extra="forbid")

    text: Optional[str] = Field(
        None,
        max_length=500,
        description="Updated note content (optional, max 500 characters)",
        example="Updated note text",
    )
    is_completed: Optional[bool] = Field(
        None, description="Set to true to mark completed, false to mark not completed"
    )

    @field_validator("text")
    @classmethod
    def _validate_text_optional(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        if not isinstance(v, str):
            raise TypeError("text must be a string")
        v_stripped = v.strip()
        if not v_stripped:
            raise ValueError("text must not be empty or whitespace-only")
        if len(v_stripped) > 500:
            raise ValueError("text must be at most 500 characters")
        return v_stripped
