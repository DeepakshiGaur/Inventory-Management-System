from sqlalchemy import Column, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class IssuanceItem(Base):
    __tablename__ = "issuance_items"

    id = Column(Integer, primary_key=True, index=True)

    issuance_id = Column(
        Integer,
        ForeignKey("issuances.id"),
        nullable=False,
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

    quantity = Column(
        Integer,
        nullable=False
    )

    notes = Column(
        Text,
        nullable=True
    )

    issuance = relationship(
        "Issuance",
        back_populates="items"
    )

    product = relationship("Product")

    asset = relationship("Asset")