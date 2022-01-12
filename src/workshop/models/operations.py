# то что будет возвращать в ответе (response)
from pydantic import BaseModel

from typing import Optional
from datetime import date
from enum import Enum


class OperationKind(str, Enum):
    INCOME = 'income'
    OUTCOME = 'outcome'


class OperationBase(BaseModel):
    date: date
    kind: OperationKind
    amount: float
    description: Optional[str]


class Operation(OperationBase):
    id: int

    class Config:
        orm_mode = True


class OperationCreate(OperationBase):
    pass
