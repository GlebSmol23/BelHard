from fastapi import APIRouter, HTTPException, Query, Depends, Request
from schemas import CategorySchema, CategoryInDBSchema
from crud import CRUDCategory, CRUDUser
from jose import JWTError, jwt
from core.config import CONFIG

category_router = APIRouter(
    prefix="/category"
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


async def check_category_id(category_id: int = Query(ge=1)) -> int:
    category = await CRUDCategory.get(category_id=category_id)
    if category:
        return category_id
    raise HTTPException(status_code=404, detail=f"Category with id {category_id} not found")


@category_router.get("/get", response_model=CategoryInDBSchema, tags=["Category"])
async def get_category(category_id: int = Depends(check_category_id)):
    return await CRUDCategory.get(category_id=category_id)


@category_router.get("/all", response_model=list[CategoryInDBSchema], tags=["Category"])
async def get_all_categories(parent_id: int = Query(ge=1, default=None)):
    return await CRUDCategory.get_all(parent_id=parent_id)


@category_router.post("/add", response_model=CategoryInDBSchema, tags=["Category"])
async def add_category(category: CategorySchema, request: Request = Depends(validate_user)):
    if request:
        return await CRUDCategory.add(category=category) or HTTPException(status_code=404, detail="Category is exist")
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")


@category_router.delete("/del", tags=["Category"])
async def delete_category(category_id: int = Depends(check_category_id), request: Request = Depends(validate_user)):
    if request:
        await CRUDCategory.delete(category_id=category_id)
        raise HTTPException(status_code=200, detail="Category was deleted")
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")


@category_router.put("/update", tags=["Category"])
async def update_category(category: CategoryInDBSchema, request: Request = Depends(validate_user)):
    if request:
        await CRUDCategory.update(category=category)
        raise HTTPException(status_code=200, detail="Category was updated")
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
