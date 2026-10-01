from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class Issuance(Base):
    __tablename__ = "issuances"

    id = Column(Integer, primary_key=True, index=True)

    issued_to_user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    issued_by_user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    issue_date = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    expected_return_date = Column(
        DateTime,
        nullable=True
    )

    purpose = Column(
        String(255),
        nullable=True
    )

    status = Column(
        String(30),
        nullable=False,
        default="ACTIVE"
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

    issued_to_user = relationship(
        "User",
        foreign_keys=[issued_to_user_id]
    )

    issued_by_user = relationship(
        "User",
        foreign_keys=[issued_by_user_id]
    )

    items = relationship(
        "IssuanceItem",
        back_populates="issuance",
        cascade="all, delete-orphan"
    )
    returns = relationship(
        "Return",
        back_populates="issuance",
        cascade="all, delete-orphan"
    )