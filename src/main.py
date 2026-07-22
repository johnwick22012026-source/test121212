from uuid import UUID, uuid4
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import threading

from fastapi import FastAPI, Depends, HTTPException, Request, Response, status, Header
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from src import crud  # expected functions: get_all_notes, create_note, complete_note, delete_note
from src import schemas  # expected Pydantic v2 models: NoteCreate, NoteRead
from src.db import get_db  # expected dependency that yields a DB session

app = FastAPI(title="TODO Notes API", version="1.0.0")

# CORS - allow frontends to call the API during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Simple in-memory rate limiter and idempotency store (per-process)
_RATE_LIMIT = 120  # requests per window
_RATE_WINDOW = timedelta(minutes=1)
_rate_lock = threading.Lock()
_client_buckets: Dict[str, Dict[str, Any]] = {}  # ip -> {count, window_start}

_idempotency_lock = threading.Lock()
_idempotency_store: Dict[str, Dict[str, Any]] = {}  # idempotency_key -> {response, created_at}


# Utility: get client identifier (IP). Fallback to "anonymous".
def _get_client_id(request: Request) -> str:
    client = request.client.host if request.client else "anonymous"
    # Prefer X-Forwarded-For if present
    xff = request.headers.get("x-forwarded-for")
    if xff:
        return xff.split(",")[0].strip()
    return client


# Rate limiting dependency/middleware
@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    client_id = _get_client_id(request)
    now = datetime.utcnow()

    with _rate_lock:
        bucket = _client_buckets.get(client_id)
        if not bucket or now - bucket["window_start"] >= _RATE_WINDOW:
            # reset window
            bucket = {"count": 0, "window_start": now}
            _client_buckets[client_id] = bucket

        if bucket["count"] >= _RATE_LIMIT:
            reset_seconds = int((_RATE_WINDOW - (now - bucket["window_start"])).total_seconds())
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "code": "rate_limit_exceeded",
                    "message": "Rate limit exceeded",
                    "details": {"limit": _RATE_LIMIT, "window_seconds": int(_RATE_WINDOW.total_seconds())},
                    "request_id": str(uuid4()),
                },
                headers={
                    "X-RateLimit-Limit": str(_RATE_LIMIT),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(reset_seconds),
                },
            )
        bucket["count"] += 1
        remaining = max(0, _RATE_LIMIT - bucket["count"])
        reset_seconds = int((_RATE_WINDOW - (now - bucket["window_start"])).total_seconds())

    response = aw