import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func

from .base import Base


class Wallet(Base):

    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    balance: Mapped[int] = mapped_column(server_default='0')

    def to_dict(self):
        return {
            "id": Base.id,
            "balance": self.balance / 100
        }