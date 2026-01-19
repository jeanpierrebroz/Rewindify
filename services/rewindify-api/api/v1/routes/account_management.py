"""Routes for account management."""

from fastapi import APIRouter

account_router = APIRouter(prefix="/account/")

@account_router.post("create")
async def create_account(id_token: str):
    try:

    except 401