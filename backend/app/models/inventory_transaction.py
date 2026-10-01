from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class InventoryTransaction(Base):
    __tablename__ = "inventory_transactions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    product_id = Column(
        Integer,
        ForeignKey("products.id"),
        nullable=False,
        index=True
    )

    asset_id = Column(
        Integer,
        ForeignKey("assets.id"),
        nullable=True,
        index=True
    )

    transaction_type = Column(
        String(30),
        nullable=False
    )

    quantity = Column(
        Integer,
        nullable=False
    )

    reference_id = Column(
        Integer,
        nullable=True
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

    product = relationship(
        "Product"
    )

    asset = relationship(
        "Asset"
    )