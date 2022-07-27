from fastapi import FastAPI
from endpoints.v1 import api_v1_router


tags = [
    {
        "name": "Category",
        "description": "Endpoints for category"
    },
    {
        "name": "Product",
        "description": "Endpoints for product"
    }
]


app = FastAPI(
    title="BELHARD",
    description="Belhard lesson",
    version="0.0.1",
    openapi_tags=tags
)
app.include_router(api_v1_router)
