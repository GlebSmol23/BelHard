from fastapi import APIRouter, HTTPException, Query, Depends, Request
from schemas import StatusSchema, StatusInDBSchema
from crud import CRUDStatus, CRUDUser
from jose import JWTError, jwt
from core.config import CONFIG

status_router = APIRouter(
    prefix="/status"
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


async def check_status_id(status_id: int = Query(ge=1)) -> int:
    status = await CRUDStatus.get(status_id=status_id)
    if status:
        return status_id
    raise HTTPException(status_code=404, detail=f"Status with id {status_id} not found")


@status_router.get("/get", response_model=StatusInDBSchema, tags=["Status"])
async def get_status(status_id: int = Depends(check_status_id)):
    return await CRUDStatus.get(status_id=status_id)


@status_router.get("/all", response_model=list[StatusInDBSchema], tags=["Status"])
async def get_all_categories(parent_id: int = Query(ge=1, default=None)):
    return await CRUDStatus.get_all(parent_id=parent_id)


@status_router.post("/add", response_model=StatusInDBSchema, tags=["Status"])
async def add_status(status: StatusSchema, request: Request = Depends(validate_user)):
    if request:
        return await CRUDStatus.add(status=status) or HTTPException(status_code=404, detail="Status is exist")
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")


@status_router.delete("/del", tags=["Status"])
async def delete_status(status_id: int = Depends(check_status_id), request: Request = Depends(validate_user)):
    if request:
        await CRUDStatus.delete(status_id=status_id)
        raise HTTPException(status_code=200, detail="Status was deleted")
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")


@status_router.put("/update", tags=["Status"])
async def update_status(status: StatusInDBSchema, request: Request = Depends(validate_user)):
    if request:
        await CRUDStatus.update(status=status)
        raise HTTPException(status_code=200, detail="Status was updated")
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
