from sqlalchemy import String, Integer, Date, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(30), default="CLAIMANT")
    created_at: Mapped[Date] = mapped_column(Date, nullable=False)
    profile = relationship("UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    vehicles = relationship("Vehicle", back_populates="owner", cascade="all, delete-orphan")
    policies = relationship("InsurancePolicy", back_populates="owner", cascade="all, delete-orphan")
    accidents = relationship("Accident", back_populates="claimant", cascade="all, delete-orphan")

class UserProfile(Base):
    __tablename__ = "user_profiles"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    full_name: Mapped[str | None] = mapped_column(String(150))
    date_of_birth: Mapped[Date | None] = mapped_column(Date)
    phone: Mapped[str | None] = mapped_column(String(30))
    address: Mapped[str | None] = mapped_column(Text)
    emergency_contact: Mapped[str | None] = mapped_column(String(150))
    licence_number: Mapped[str | None] = mapped_column(String(80))
    licence_type: Mapped[str | None] = mapped_column(String(40))
    licence_issue_date: Mapped[Date | None] = mapped_column(Date)
    licence_expiry_date: Mapped[Date | None] = mapped_column(Date)
    licence_document: Mapped[str | None] = mapped_column(String(500))
    user = relationship("User", back_populates="profile")
