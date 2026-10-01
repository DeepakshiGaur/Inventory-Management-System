from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.asset import Asset
from app.models.product import Product
from app.schemas.asset import (
    AssetCreate,
    AssetResponse,
    AssetUpdate,
)

router = APIRouter(
    prefix="/assets",
    tags=["Assets"]
)


@router.post("/", response_model=AssetResponse)
def create_asset(
    asset: AssetCreate,
    db: Session = Depends(get_db)
):
    # Check that product exists
    product = (
        db.query(Product)
        .filter(Product.id == asset.product_id)
        .first()
    )

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    # Only ASSET products can have individual assets
    if product.item_type != "ASSET":
        raise HTTPException(
            status_code=400,
            detail="Assets can only be created for ASSET type products"
        )

    # Check asset tag uniqueness
    existing_asset_tag = (
        db.query(Asset)
        .filter(Asset.asset_tag == asset.asset_tag)
        .first()
    )

    if existing_asset_tag:
        raise HTTPException(
            status_code=400,
            detail="Asset tag already exists"
        )

    # Check serial number uniqueness
    existing_serial = (
        db.query(Asset)
        .filter(Asset.serial_number == asset.serial_number)
        .first()
    )

    if existing_serial:
        raise HTTPException(
            status_code=400,
            detail="Serial number already exists"
        )

    new_asset = Asset(
        product_id=asset.product_id,
        asset_tag=asset.asset_tag,
        serial_number=asset.serial_number,
        status=asset.status,
        condition=asset.condition,
        location=asset.location,
        purchase_date=asset.purchase_date,
        warranty_expiry=asset.warranty_expiry,
        notes=asset.notes,
    )

    db.add(new_asset)
    db.commit()
    db.refresh(new_asset)

    return new_asset


@router.get("/", response_model=list[AssetResponse])
def get_assets(
    db: Session = Depends(get_db)
):
    return db.query(Asset).all()


@router.get("/{asset_id}", response_model=AssetResponse)
def get_asset(
    asset_id: int,
    db: Session = Depends(get_db)
):
    asset = (
        db.query(Asset)
        .filter(Asset.id == asset_id)
        .first()
    )

    if not asset:
        raise HTTPException(
            status_code=404,
            detail="Asset not found"
        )

    return asset


@router.put("/{asset_id}", response_model=AssetResponse)
def update_asset(
    asset_id: int,
    asset_data: AssetUpdate,
    db: Session = Depends(get_db)
):
    asset = (
        db.query(Asset)
        .filter(Asset.id == asset_id)
        .first()
    )

    if not asset:
        raise HTTPException(
            status_code=404,
            detail="Asset not found"
        )

    update_data = asset_data.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(asset, key, value)

    db.commit()
    db.refresh(asset)

    return asset


@router.delete("/{asset_id}")
def delete_asset(
    asset_id: int,
    db: Session = Depends(get_db)
):
    asset = (
        db.query(Asset)
        .filter(Asset.id == asset_id)
        .first()
    )

    if not asset:
        raise HTTPException(
            status_code=404,
            detail="Asset not found"
        )

    asset.status = "RETIRED"

    db.commit()

    return {
        "message": "Asset retired successfully"
    }