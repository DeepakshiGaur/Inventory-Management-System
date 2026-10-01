from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.category import Category
from app.models.product import Product
from app.schemas.product import (
    ProductCreate,
    ProductResponse,
    ProductUpdate,
)

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.post("/", response_model=ProductResponse)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    # Check category exists
    category = (
        db.query(Category)
        .filter(Category.id == product.category_id)
        .first()
    )

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    # Check SKU is unique
    existing_product = (
        db.query(Product)
        .filter(Product.sku == product.sku)
        .first()
    )

    if existing_product:
        raise HTTPException(
            status_code=400,
            detail="SKU already exists"
        )

    # Validate item type
    if product.item_type not in ["CONSUMABLE", "ASSET"]:
        raise HTTPException(
            status_code=400,
            detail="item_type must be CONSUMABLE or ASSET"
        )

    new_product = Product(
        name=product.name,
        sku=product.sku,
        description=product.description,
        category_id=product.category_id,
        item_type=product.item_type,
        unit_price=product.unit_price,
        cost_price=product.cost_price,
        current_stock=product.current_stock,
        minimum_stock=product.minimum_stock,
        unit=product.unit,
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


@router.get("/", response_model=list[ProductResponse])
def get_products(
    db: Session = Depends(get_db)
):
    return db.query(Product).all()


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    product = (
        db.query(Product)
        .filter(Product.id == product_id)
        .first()
    )

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db)
):
    product = (
        db.query(Product)
        .filter(Product.id == product_id)
        .first()
    )

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    update_data = product_data.model_dump(
        exclude_unset=True
    )

    if "category_id" in update_data:
        category = (
            db.query(Category)
            .filter(Category.id == update_data["category_id"])
            .first()
        )

        if not category:
            raise HTTPException(
                status_code=404,
                detail="Category not found"
            )

    if "item_type" in update_data:
        if update_data["item_type"] not in [
            "CONSUMABLE",
            "ASSET"
        ]:
            raise HTTPException(
                status_code=400,
                detail="item_type must be CONSUMABLE or ASSET"
            )

    for key, value in update_data.items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)

    return product


@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    product = (
        db.query(Product)
        .filter(Product.id == product_id)
        .first()
    )

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    product.is_active = False

    db.commit()

    return {
        "message": "Product deactivated successfully"
    }