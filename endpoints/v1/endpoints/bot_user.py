from fastapi import APIRouter, HTTPException, Query, Depends, Request
from schemas import BotUserSchema, BotUserInDBSchema
from crud import CRUDBotUser, CRUDUser
from jose import JWTError, jwt
from core.config import CONFIG

bot_user_router = APIRouter(
    prefix="/bot_user"
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


async def check_bot_user_id(bot_user_id: int = Query(ge=1)) -> int:
    bot_user = await CRUDBotUser.get(bot_user_id=bot_user_id)
    if bot_user:
        return bot_user_id
    raise HTTPException(status_code=404, detail=f"Bot_user with id {bot_user_id} not found")


@bot_user_router.get("/get", response_model=BotUserInDBSchema, tags=["Bot_user"])
async def get_bot_user(bot_user_id: int = Depends(check_bot_user_id)):
    return await CRUDBotUser.get(bot_user_id=bot_user_id)


@bot_user_router.get("/all", response_model=list[BotUserInDBSchema], tags=["Bot_user"])
async def get_all_bot_user(parent_id: int = Query(ge=1, default=None)):
    return await CRUDBotUser.get_all(parent_id=parent_id)


@bot_user_router.post("/add", response_model=BotUserInDBSchema, tags=["Bot_user"])
async def add_bot_user(bot_user: BotUserSchema, request: Request = Depends(validate_user)):
    if request:
        return await CRUDBotUser.add(bot_user=bot_user) or HTTPException(status_code=404, detail="Bot_user is exist")
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")


@bot_user_router.delete("/del", tags=["Bot_user"])
async def delete_bot_user(bot_user_id: int = Depends(check_bot_user_id), request: Request = Depends(validate_user)):
    if request:
        await CRUDBotUser.delete(bot_user_id=bot_user_id)
        raise HTTPException(status_code=200, detail="Bot_user was deleted")
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")


@bot_user_router.put("/update", tags=["Bot_user"])
async def update_bot_user(bot_user: BotUserInDBSchema, request: Request = Depends(validate_user)):
    if request:
        await CRUDBotUser.update(bot_user=bot_user)
        raise HTTPException(status_code=200, detail="Bot_user was updated")
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
