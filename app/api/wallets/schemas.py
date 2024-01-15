from pydantic import BaseModel, ConfigDict
import datetime
from typing import List


class WalletBase(BaseModel):
    balance: int
    created_at: datetime.datetime


class WalletUpdate(WalletBase):
    pass


class WalletUpdatePartial(WalletBase):
    balance: int


class Wallet(WalletBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class Transfer(BaseModel):
    source_wallet_id: int
    destination_wallet_id: int
    amount: int


class Deposit(BaseModel):
    destination_wallet_id: int
    amount: int


class Withdraw(BaseModel):
    source_wallet_id: int
    amount: int


class BatchBalance(BaseModel):
    addresses_list: List[int]
