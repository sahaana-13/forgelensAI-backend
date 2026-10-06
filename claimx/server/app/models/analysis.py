from datetime import datetime
from sqlalchemy import String, Integer, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
class StatementComparison(Base):
    __tablename__ = "statement_comparisons"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    accident_id: Mapped[int] = mapped_column(ForeignKey("accidents.id"))
    result: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime)
    accident = relationship("Accident", back_populates="comparisons")
class EvidenceAnalysis(Base):
    __tablename__ = "evidence_analysis"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    accident_id: Mapped[int] = mapped_column(ForeignKey("accidents.id"))
    result: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime)
    accident = relationship("Accident", back_populates="evidence_analyses")
class MissingInformation(Base):
    __tablename__ = "missing_information"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    accident_id: Mapped[int] = mapped_column(ForeignKey("accidents.id"))
    item: Mapped[str] = mapped_column(String(255))
    reason: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(30), default="MISSING")
    created_at: Mapped[datetime] = mapped_column(DateTime)
    accident = relationship("Accident", back_populates="missing_information")
