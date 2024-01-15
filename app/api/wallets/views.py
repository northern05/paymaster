from fastapi import APIRouter, status, Depends, requests
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import db_helper
from . import crud
from .dependencies import wallet_by_id, verify_token
from .schemas import Wallet, BatchBalance, Deposit, Transfer, Withdraw

router = APIRouter(tags=["Wallets"])


@router.get("/", response_model=dict)
async def get_wallets(
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
        authorized: bool = Depends(verify_token)
):
    return await crud.get_wallets_balances(session=session)


@router.post(
    "/",
    response_model=Wallet,
    status_code=status.HTTP_201_CREATED,
)
async def create_wallet(
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
        authorized: bool = Depends(verify_token)
):
    return await crud.create_wallet(session=session)


@router.get("/{wallet_id}", response_model=dict)
async def get_wallet(
        wallet: Wallet = Depends(wallet_by_id),
        authorized: bool = Depends(verify_token)
):
    return wallet


@router.get("/batch/", response_model=dict)
async def get_batch_balance(
        batch_balance: BatchBalance,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
        authorized: bool = Depends(verify_token)
) -> dict:
    return await crud.get_batch_balance(
        session=session,
        addresses_list=batch_balance.addresses_list
    )


@router.delete("/{wallet_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_wallet(
        wallet: Wallet = Depends(wallet_by_id),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
        authorized: bool = Depends(verify_token)
) -> None:
    await crud.delete_wallet(session=session, wallet=wallet)


@router.post("/transfer", status_code=200, response_model=dict)
async def transfer(
        _transfer: Transfer,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
        authorized: bool = Depends(verify_token)
) -> dict:
    return await crud.transfer(
        session=session,
        source_wallet_id=_transfer.source_wallet_id,
        destination_wallet_id=_transfer.destination_wallet_id,
        amount=_transfer.amount
    )


@router.post("/deposit", status_code=200, response_model=dict)
async def deposit(
        _deposit: Deposit,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
        authorized: bool = Depends(verify_token)
) -> dict:
    return await crud.deposit(
        session=session,
        destination_wallet_id=_deposit.destination_wallet_id,
        amount=_deposit.amount
    )


@router.post("/withdraw", status_code=200, response_model=dict)
async def withdraw(
        _withdraw: Withdraw,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
        authorized: bool = Depends(verify_token)
) -> dict:
    return await crud.withdraw(
        session=session,
        source_wallet_id=_withdraw.source_wallet_id,
        amount=_withdraw.amount
    )
