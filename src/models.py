from sqlalchemy import Column, String, Text, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
import uuid
import datetime

Base = declarative_base()

class Notes(Base):
    __tablename__ = "notes"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    text = Column(Text, nullable=False)
    is_completed = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    def __repr__(self) -> str:
        return f"<Notes(id={self.id!r}, is_completed={self.is_completed}, created_at={self.created_at})>"
