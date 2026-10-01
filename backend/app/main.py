from fastapi import FastAPI

from app.routers.category import router as category_router
from app.routers.product import router as product_router
from app.routers.asset import router as asset_router

app = FastAPI(
    title="Inventory Management System API",
    description="Backend API for managing products, inventory, purchases and sales.",
    version="1.0.0",
)

app.include_router(category_router)
app.include_router(product_router)
app.include_router(asset_router)

@app.get("/")
def root():
    return {
        "message": "Inventory Management System API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }