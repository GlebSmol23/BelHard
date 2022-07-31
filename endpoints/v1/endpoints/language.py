from fastapi import APIRouter, HTTPException, Query, Depends, Request
from schemas import LanguageSchema, LanguageInDBSchema
from crud import CRUDLanguage, CRUDUser
from jose import JWTError, jwt
from core.config import CONFIG

language_router = APIRouter(
    prefix="/language"
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


async def check_language_id(language_id: int = Query(ge=1)) -> int:
    language = await CRUDLanguage.get(language_id=language_id)
    if language:
        return language_id
    raise HTTPException(status_code=404, detail=f"Language with id {language_id} not found")


@language_router.get("/get", response_model=LanguageInDBSchema, tags=["Language"])
async def get_language(language_id: int = Depends(check_language_id)):
    return await CRUDLanguage.get(language_id=language_id)


@language_router.get("/all", response_model=list[LanguageInDBSchema], tags=["Language"])
async def get_all_categories(parent_id: int = Query(ge=1, default=None)):
    return await CRUDLanguage.get_all(parent_id=parent_id)


@language_router.post("/add", response_model=LanguageInDBSchema, tags=["Language"])
async def add_language(language: LanguageSchema, request: Request = Depends(validate_user)):
    if request:
        return await CRUDLanguage.add(language=language) or HTTPException(status_code=404, detail="Language is exist")
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")


@language_router.delete("/del", tags=["Language"])
async def delete_language(language_id: int = Depends(check_language_id), request: Request = Depends(validate_user)):
    if request:
        await CRUDLanguage.delete(language_id=language_id)
        raise HTTPException(status_code=200, detail="Language was deleted")
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")


@language_router.put("/update", tags=["Language"])
async def update_language(language: LanguageInDBSchema, request: Request = Depends(validate_user)):
    if request:
        await CRUDLanguage.update(language=language)
        raise HTTPException(status_code=200, detail="Language was updated")
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
