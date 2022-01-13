from io import StringIO
import csv
from typing import Any

from fastapi import Depends

from ..models.operations import OperationCreate, Operation
from .operations import OperationService


class ReportsService:
    def __init__(self, operations_service: OperationService = Depends()):
        self.operations_service = operations_service

    def import_csv(self, user_id: int, file: Any):
        reader = csv.DictReader(
            (line.decode() for line in file),
            fieldnames=[
                'date',
                'kind',
                'amount',
                'description',
            ],
        )
        operations = []
        next(reader)
        for row in reader:
            operation_data = OperationCreate.parse_obj(row)
            if operation_data.description == '':
                operation_data.description = None
            operations.append(operation_data)

        self.operations_service.create_many(
            user_id=user_id,
            operations_data=operations,
        )

    def export_csv(self, user_id: int) -> Any:
        output = StringIO()
        writer = csv.DictWriter(
            output,
            fieldnames=[
                'date',
                'kind',
                'amount',
                'description',
            ],
            extrasaction='ignore',      # игнор лишних параметров
        )

        operations = self.operations_service.get_list(user_id=user_id)
        writer.writeheader()
        for operation in operations:
            operation_data = Operation.from_orm(operation)
            writer.writerow(operation_data.dict())

        output.seek(0)
        return output
