from typing import List, Optional

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from ..models.operations import Operation, OperationKind, OperationCreate, OperationUpdate
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


@router.get('/{operation_id}', response_model=Operation)
def get_operation(
        operation_id: int,
        service: OperationService = Depends()
):
    return service.get(operation_id)


@router.put('/{operation_id}', response_model=Operation)
def update_operation(
        operation_id: int,
        operation_data: OperationUpdate,
        service: OperationService = Depends()
):
    return service.update(operation_id=operation_id, operation_data=operation_data)


@router.delete('/{operation_id}')
def delete_operation(
        operation_id: int,
        service: OperationService = Depends(),
):
    service.delete(operation_id)
    # когда ничего не возвращаем, например при удалении, то
    # нужно делать так
    return Response(status_code=status.HTTP_204_NO_CONTENT)
