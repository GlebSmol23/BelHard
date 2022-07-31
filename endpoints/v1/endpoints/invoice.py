from fastapi import APIRouter, HTTPException, Query, Depends, Request
from schemas import InvoiceSchema, InvoiceInDBSchema
from crud import CRUDInvoice, CRUDUser
from jose import JWTError, jwt
from core.config import CONFIG

invoice_router = APIRouter(
    prefix="/invoice"
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


async def check_invoice_id(invoice_id: int = Query(ge=1)) -> int:
    invoice = await CRUDInvoice.get(invoice_id=invoice_id)
    if invoice:
        return invoice_id
    raise HTTPException(status_code=404, detail=f"Invoice with id {invoice_id} not found")


@invoice_router.get("/get", response_model=InvoiceInDBSchema, tags=["Invoice"])
async def get_invoice(invoice_id: int = Depends(check_invoice_id)):
    return await CRUDInvoice.get(invoice_id=invoice_id)


@invoice_router.get("/all", response_model=list[InvoiceInDBSchema], tags=["Invoice"])
async def get_all_categories(parent_id: int = Query(ge=1, default=None)):
    return await CRUDInvoice.get_all(parent_id=parent_id)


@invoice_router.post("/add", response_model=InvoiceInDBSchema, tags=["Invoice"])
async def add_invoice(invoice: InvoiceSchema, request: Request = Depends(validate_user)):
    if request:
        return await CRUDInvoice.add(invoice=invoice) or HTTPException(status_code=404, detail="Invoice is exist")
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")


@invoice_router.delete("/del", tags=["Invoice"])
async def delete_invoice(invoice_id: int = Depends(check_invoice_id), request: Request = Depends(validate_user)):
    if request:
        await CRUDInvoice.delete(invoice_id=invoice_id)
        raise HTTPException(status_code=200, detail="Invoice was deleted")
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")


@invoice_router.put("/update", tags=["Invoice"])
async def update_invoice(invoice: InvoiceInDBSchema, request: Request = Depends(validate_user)):
    if request:
        await CRUDInvoice.update(invoice=invoice)
        raise HTTPException(status_code=200, detail="Invoice was updated")
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
