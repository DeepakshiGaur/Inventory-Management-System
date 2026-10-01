from datetime import date, datetime

from sqlalchemy import Boolean, Column, DateTime, Date, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    asset_tag = Column(String(100), unique=True, nullable=False, index=True)
    serial_number = Column(String(100), unique=True, nullable=True, index=True)
    status = Column(String(30), nullable=False, default="AVAILABLE")

    condition = Column(String(30), nullable=False, default = "GOOD")

    location = Column(String(150), nullable=True)

    purchase_date = Column(Date, nullable=True)
    

    warranty_expiry = Column(Date, nullable=True)
    notes = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    product = relationship("Product", back_populates="assets")