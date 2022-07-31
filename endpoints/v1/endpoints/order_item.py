from fastapi import APIRouter, HTTPException, Query, Depends, Request
from schemas import OrderItemSchema, OrderItemInDBSchema
from crud import CRUDOrderItem, CRUDUser
from jose import JWTError, jwt
from core.config import CONFIG

order_item_router = APIRouter(
    prefix="/order_item"
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


async def check_order_item_id(order_item_id: int = Query(ge=1)) -> int:
    order_item = await CRUDOrderItem.get(order_item_id=order_item_id)
    if order_item:
        return order_item_id
    raise HTTPException(status_code=404, detail=f"Order_item with id {order_item_id} not found")


@order_item_router.get("/get", response_model=OrderItemInDBSchema, tags=["Order_item"])
async def get_order_item(order_item_id: int = Depends(check_order_item_id)):
    return await CRUDOrderItem.get(order_item_id=order_item_id)


@order_item_router.get("/all", response_model=list[OrderItemInDBSchema], tags=["Order_item"])
async def get_all_order_items(parent_id: int = Query(ge=1, default=None)):
    return await CRUDOrderItem.get_all(parent_id=parent_id)


@order_item_router.post("/add", response_model=OrderItemInDBSchema, tags=["Order_item"])
async def add_order_item(order_item: OrderItemSchema, request: Request = Depends(validate_user)):
    if request:
        return await CRUDOrderItem.add(order_item=order_item) or HTTPException(status_code=404,
                                                                               detail="Order_item is exist")
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")


@order_item_router.delete("/del", tags=["Order_item"])
async def delete_order_item(order_item_id: int = Depends(check_order_item_id),
                            request: Request = Depends(validate_user)):
    if request:
        await CRUDOrderItem.delete(order_item_id=order_item_id)
        raise HTTPException(status_code=200, detail="Order_item was deleted")
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")


@order_item_router.put("/update", tags=["Order_item"])
async def update_order_item(order_item: OrderItemInDBSchema, request: Request = Depends(validate_user)):
    if request:
        await CRUDOrderItem.update(order_item=order_item)
        raise HTTPException(status_code=200, detail="Order_item was updated")
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
