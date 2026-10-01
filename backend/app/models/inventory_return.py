from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class Return(Base):
    __tablename__ = "returns"

    id = Column(Integer, primary_key=True, index=True)

    issuance_id = Column(
        Integer,
        ForeignKey("issuances.id"),
        nullable=False,
        index=True
    )

    received_by_user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    return_date = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    notes = Column(
        Text,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    issuance = relationship(
        "Issuance",
        back_populates="returns"
    )

    received_by_user = relationship(
        "User"
    )

    items = relationship(
        "ReturnItem",
        back_populates="return_record",
        cascade="all, delete-orphan"
    )