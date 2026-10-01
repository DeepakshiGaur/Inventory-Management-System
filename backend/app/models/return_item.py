from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class ReturnItem(Base):
    __tablename__ = "return_items"

    id = Column(Integer, primary_key=True, index=True)

    return_id = Column(
        Integer,
        ForeignKey("returns.id"),
        nullable=False,
        index=True
    )

    issuance_item_id = Column(
        Integer,
        ForeignKey("issuance_items.id"),
        nullable=False,
        index=True
    )

    quantity = Column(
        Integer,
        nullable=False
    )

    condition = Column(
        String(30),
        nullable=True
    )

    notes = Column(
        Text,
        nullable=True
    )

    return_record = relationship(
        "Return",
        back_populates="items"
    )

    issuance_item = relationship(
        "IssuanceItem"
    )