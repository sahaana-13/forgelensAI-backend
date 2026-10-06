from datetime import datetime
from sqlalchemy import String, Integer, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
class Accident(Base):
    __tablename__ = "accidents"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    incident_id: Mapped[str] = mapped_column(String(40), unique=True, index=True)
    claimant_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    vehicle_id: Mapped[int | None] = mapped_column(ForeignKey("vehicles.id"))
    accident_time: Mapped[datetime] = mapped_column(DateTime)
    latitude: Mapped[float | None] = mapped_column(Float)
    longitude: Mapped[float | None] = mapped_column(Float)
    location_text: Mapped[str | None] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(40), default="OPEN")
    claim_type: Mapped[str | None] = mapped_column(String(30))
    description: Mapped[str | None] = mapped_column(Text)
    claimant = relationship("User", back_populates="accidents")
    vehicle = relationship("Vehicle", back_populates="accidents")
    parties = relationship("AccidentParty", back_populates="accident", cascade="all, delete-orphan")
    evidence = relationship("Evidence", back_populates="accident", cascade="all, delete-orphan")
    interviews = relationship("Interview", back_populates="accident", cascade="all, delete-orphan")
    statements = relationship("Statement", back_populates="accident", cascade="all, delete-orphan")
    comparisons = relationship("StatementComparison", back_populates="accident", cascade="all, delete-orphan")
    evidence_analyses = relationship("EvidenceAnalysis", back_populates="accident", cascade="all, delete-orphan")
    missing_information = relationship("MissingInformation", back_populates="accident", cascade="all, delete-orphan")
    fnol = relationship("FnolReport", back_populates="accident", uselist=False, cascade="all, delete-orphan")

class AccidentParty(Base):
    __tablename__ = "accident_parties"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    accident_id: Mapped[int] = mapped_column(ForeignKey("accidents.id"))
    party_label: Mapped[str] = mapped_column(String(20))
    name: Mapped[str | None] = mapped_column(String(150))
    contact: Mapped[str | None] = mapped_column(String(80))
    vehicle_registration: Mapped[str | None] = mapped_column(String(30))
    accident = relationship("Accident", back_populates="parties")
