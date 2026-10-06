from datetime import datetime
from sqlalchemy import String, Integer, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
class Interview(Base):
    __tablename__ = "interviews"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    accident_id: Mapped[int] = mapped_column(ForeignKey("accidents.id"))
    party_label: Mapped[str] = mapped_column(String(20))
    status: Mapped[str] = mapped_column(String(30), default="ACTIVE")
    started_at: Mapped[datetime] = mapped_column(DateTime)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime)
    accident = relationship("Accident", back_populates="interviews")
    messages = relationship("InterviewMessage", back_populates="interview", cascade="all, delete-orphan")
class InterviewMessage(Base):
    __tablename__ = "interview_messages"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    interview_id: Mapped[int] = mapped_column(ForeignKey("interviews.id"))
    sender: Mapped[str] = mapped_column(String(20))
    message: Mapped[str] = mapped_column(Text)
    extracted: Mapped[dict | None] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime)
    interview = relationship("Interview", back_populates="messages")
class Statement(Base):
    __tablename__ = "statements"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    accident_id: Mapped[int] = mapped_column(ForeignKey("accidents.id"))
    party_label: Mapped[str] = mapped_column(String(20))
    raw_text: Mapped[str] = mapped_column(Text)
    structured_data: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime)
    accident = relationship("Accident", back_populates="statements")
