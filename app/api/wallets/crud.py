from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.models import Wallet
from app import exceptions

from .schemas import WalletUpdate, WalletUpdatePartial


async def get_wallets_balances(session: AsyncSession) -> dict:
    balances = {}
    stmt = select(Wallet).order_by(Wallet.created_at.desc())
    result: Result = await session.execute(stmt)
    wallets = result.scalars().all()
    for wallet in wallets:
        balances[wallet.id] = wallet.balance
    return balances


async def get_wallet_balance(session: AsyncSession, wallet_id: int) -> dict:
    result = await session.get(Wallet, wallet_id)
    return {result.id: result.balance}


async def create_wallet(session: AsyncSession) -> Wallet:
    stmt = select(Wallet).order_by(Wallet.created_at.desc()).limit(1)
    result = await session.execute(stmt)
    last_wallet = result.scalars().first()
    if not last_wallet:
        wallet_id = 10000000
    else:
        wallet_id = int(last_wallet.id) + 1
    wallet = Wallet(
        id=wallet_id
    )
    session.add(wallet)
    await session.commit()
    # await session.refresh(product)
    return wallet


async def update_wallet(
        session: AsyncSession,
        wallet: Wallet,
        wallet_update: WalletUpdate | WalletUpdatePartial,
        partial: bool = False,
) -> Wallet:
    for name, value in wallet_update.model_dump(exclude_unset=partial).items():
        setattr(wallet, name, value)
    await session.commit()
    return wallet


async def delete_wallet(
        session: AsyncSession,
        wallet: Wallet,
) -> None:
    await session.delete(wallet)
    await session.commit()


async def transfer(
        session: AsyncSession,
        source_wallet_id: int,
        destination_wallet_id: int,
        amount: int
) -> dict:
    result = await session.execute(select(Wallet).filter(Wallet.id == destination_wallet_id))
    destination_wallet = result.scalars().first()
    result = await session.execute(select(Wallet).filter(Wallet.id == source_wallet_id))
    source_wallet = result.scalars().first()
    if not destination_wallet or not source_wallet:
        raise exceptions.ContentNotFound
    if source_wallet.balance < amount:
        raise exceptions.NotEnoughFunds
    source_wallet.balance -= amount
    destination_wallet.balance += amount
    await session.commit()
    return {"ok": True}


async def deposit(
        session: AsyncSession,
        destination_wallet_id: int,
        amount: int,
) -> dict:
    result = await session.execute(select(Wallet).filter(Wallet.id == destination_wallet_id))
    destination_wallet = result.scalars().first()
    if not destination_wallet:
        raise exceptions.ContentNotFound
    destination_wallet.balance += amount
    await session.commit()
    return {"ok": True}


async def withdraw(
        session: AsyncSession,
        source_wallet_id: int,
        amount: int,
) -> dict:
    result = await session.execute(select(Wallet).filter(Wallet.id == source_wallet_id))
    source_wallet = result.scalars().first()
    if not source_wallet:
        raise exceptions.ContentNotFound
    if amount > source_wallet.balance:
        raise exceptions.NotEnoughFunds
    source_wallet.balance -= amount
    await session.commit()
    return {"ok": True}


async def get_batch_balance(
        session: AsyncSession,
        addresses_list: list,
) -> dict:
    balances = {}
    result: Result = await session.execute(select(Wallet).filter(Wallet.id.in_(addresses_list)))
    wallets = result.scalars().all()
    for wallet in wallets:
        balances[wallet.id] = wallet.balance
    return balances
