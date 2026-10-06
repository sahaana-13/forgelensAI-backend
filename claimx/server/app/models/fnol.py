from datetime import datetime
from sqlalchemy import String, Integer, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
class FnolReport(Base):
    __tablename__ = "fnol_reports"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    accident_id: Mapped[int] = mapped_column(ForeignKey("accidents.id"), unique=True)
    status: Mapped[str] = mapped_column(String(30), default="DRAFT")
    content: Mapped[str] = mapped_column(Text)
    generated_at: Mapped[datetime] = mapped_column(DateTime)
    updated_at: Mapped[datetime] = mapped_column(DateTime)
    accident = relationship("Accident", back_populates="fnol")
