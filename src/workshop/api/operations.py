from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..models.operations import Operation, OperationKind, OperationCreate
from .. import tables
from ..database import get_session
from ..services.operations import OperationService

router = APIRouter(
    prefix='/operations'
)


@router.get('/', response_model=List[Operation])
def get_operation(
        kind: Optional[OperationKind] = None,
        service: OperationService = Depends()
):
    return service.get_list(kind=kind)


@router.post('/', response_model=Operation)
def create_operation(
        operation_data: OperationCreate,
        service: OperationService = Depends(),
):
    return service.create(operation_data)
