from fastapi import APIRouter, HTTPException, Query, Depends, Request
from schemas import OrderSchema, OrderInDBSchema
from crud import CRUDOrder, CRUDUser
from jose import JWTError, jwt
from core.config import CONFIG

order_router = APIRouter(
    prefix="/order"
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


async def check_order_id(order_id: int = Query(ge=1)) -> int:
    order = await CRUDOrder.get(order_id=order_id)
    if order:
        return order_id
    raise HTTPException(status_code=404, detail=f"Order with id {order_id} not found")


@order_router.get("/get", response_model=OrderInDBSchema, tags=["Order"])
async def get_order(order_id: int = Depends(check_order_id)):
    return await CRUDOrder.get(order_id=order_id)


@order_router.get("/all", response_model=list[OrderInDBSchema], tags=["Order"])
async def get_all_orders(order_id: int = Query(ge=1, default=None)):
    return await CRUDOrder.get_all(order_id=order_id)


@order_router.post("/add", response_model=OrderInDBSchema, tags=["Order"])
async def add_order(order: OrderSchema, request: Request = Depends(validate_user)):
    if request:
        return await CRUDOrder.add(order=order) or HTTPException(status_code=404, detail="Order is exist")
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")


@order_router.delete("/del", tags=["Order"])
async def delete_order(order_id: int = Depends(check_order_id), request: Request = Depends(validate_user)):
    if request:
        await CRUDOrder.delete(order_id=order_id)
        raise HTTPException(status_code=200, detail="Order was deleted")
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")


@order_router.put("/update", tags=["Order"])
async def update_order(order: OrderInDBSchema, request: Request = Depends(validate_user)):
    if request:
        await CRUDOrder.update(order=order)
        raise HTTPException(status_code=200, detail="Order was updated")
    else:
        HTTPException(status_code=401, detail="Unauthorized")
