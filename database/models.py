from sqlalchemy import Integer, String, Float, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime
from typing import Optional


class Base(DeclarativeBase):
    pass


class Part(Base):
    __tablename__ = "parts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nomi: Mapped[str] = mapped_column(String(200))
    narx: Mapped[float] = mapped_column(Float)
    kodi: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    model: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    kategoriya: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    dukonda_nechta: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    tavsif: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    sana: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)