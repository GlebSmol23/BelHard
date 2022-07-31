from fastapi import APIRouter, HTTPException, Query, Depends, Request
from schemas import ProductSchema, ProductInDBSchema
from crud import CRUDProduct, CRUDUser
from jose import JWTError, jwt
from core.config import CONFIG

product_router = APIRouter(
    prefix="/product"
)


async def validate_user(request: Request) -> bool:
    try:
        access_token = request.headers["Authorization"]
        data = jwt.decode(access_token, CONFIG.AUTH.SECRET_KEY, algorithms=[CONFIG.AUTH.ALGORITHM])
        username = data["sub"]
        if not await CRUDUser.get_by_username(username=username):
            return False
        token_expire_date = data["exp"]
        token_expire_date = datetime.utcfromtimestamp(token_expire_date)
        if datetime.utcnow() < token_expire_date:
            return True
        else:
            return False
    except Exception:
        return False


async def check_product_id(product_id: int = Query(ge=1)) -> int:
    product = await CRUDProduct.get(product_id=product_id)
    if product:
        return product_id
    raise HTTPException(status_code=404, detail=f"Product with id {product_id} not found")


@product_router.get("/get", response_model=ProductInDBSchema, tags=["Product"])
async def get_product(product_id: int = Depends(check_product_id)):
    return await CRUDProduct.get(product_id=product_id)


@product_router.get("/all", response_model=list[ProductInDBSchema], tags=["Product"])
async def get_all_product(parent_id: int = Query(ge=1, default=None)):
    return await CRUDProduct.get_all(parent_id=parent_id)


@product_router.post("/add", response_model=ProductInDBSchema, tags=["Product"])
async def add_product(product: ProductSchema, request: Request = Depends(validate_user)):
    if request:
        return await CRUDProduct.add(product=product) or HTTPException(status_code=404, detail="Product is exist")
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")


@product_router.delete("/del", tags=["Product"])
async def delete_product(product_id: int = Depends(check_product_id), request: Request = Depends(validate_user)):
    if request:
        await CRUDProduct.delete(product_id=product_id)
        raise HTTPException(status_code=200, detail="Product was deleted")
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")


@product_router.put("/update", tags=["Product"])
async def update_product(product: ProductInDBSchema, request: Request = Depends(validate_user)):
    if request:
        await CRUDProduct.update(product=product)
        raise HTTPException(status_code=200, detail="Product was updated")
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
    