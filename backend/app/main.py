from fastapi import FastAPI
from app.routers.categories import router as categories_router

app = FastAPI(
    title="Inventory Management System API",
    description="Backend API for managing products, inventory, purchases and sales.",
    version="1.0.0",
)

app.include_router(categories_router)

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