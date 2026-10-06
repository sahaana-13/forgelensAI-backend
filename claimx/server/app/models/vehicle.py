from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
class Vehicle(Base):
    __tablename__ = "vehicles"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    registration_number: Mapped[str] = mapped_column(String(30))
    make: Mapped[str] = mapped_column(String(80))
    model: Mapped[str] = mapped_column(String(80))
    vehicle_type: Mapped[str] = mapped_column(String(50))
    manufacturing_year: Mapped[int | None] = mapped_column(Integer)
    rc_number: Mapped[str | None] = mapped_column(String(80))
    rc_document: Mapped[str | None] = mapped_column(String(500))
    owner = relationship("User", back_populates="vehicles")
    accidents = relationship("Accident", back_populates="vehicle")
