from typing import Annotated
from fastapi import Path, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import db_helper, Wallet
from . import crud
from app.core.config import config


async def wallet_by_id(
        wallet_id: Annotated[int, Path],
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> dict:
    wallet = await crud.get_wallet_balance(session=session, wallet_id=wallet_id)
    if wallet is not None:
        return wallet

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Wallet {wallet_id} not found!",
    )


async def verify_token(req: Request):
    token = req.headers.get("Authorization")
    if token != config.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong API key"
        )
