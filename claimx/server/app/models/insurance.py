from sqlalchemy import String, Integer, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
class InsurancePolicy(Base):
    __tablename__ = "insurance_policies"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    vehicle_id: Mapped[int | None] = mapped_column(ForeignKey("vehicles.id"))
    insurance_company: Mapped[str] = mapped_column(String(150))
    policy_number: Mapped[str] = mapped_column(String(100))
    start_date: Mapped[Date] = mapped_column(Date)
    end_date: Mapped[Date] = mapped_column(Date)
    insurance_document: Mapped[str | None] = mapped_column(String(500))
    owner = relationship("User", back_populates="policies")
