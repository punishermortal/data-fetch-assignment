from commons.db import get_records_collection
from pymongo import ASCENDING
from models.record import Record, PaginatedRecordsResponse, RecordFilterRequestModel
from typing import List, Literal
from commons.exceptions import BlackCofferException
from fastapi import status
import math


class DataService:
    def __init__(self):
        self.__records_collection = get_records_collection()

    def __get_records(self, count: int, page: int, filters: dict):
        count = min(20, max(5, count))
        page = max(1, page)

        records: List[Record] = []

        total_count = self.__records_collection.count_documents(filters)

        for record in self.__records_collection.find(filters).sort("_id", ASCENDING).skip((page-1)*count).limit(count):
            records.append(Record.parse_obj(record))

        total_pages = math.ceil(total_count / count)

        return PaginatedRecordsResponse(
            count=count,
            page=page,
            total_pages=total_pages,
            records=records
        )

    def get_records(self, count: int, page: int, filters: RecordFilterRequestModel):
        return self.__get_records(count, page, filters.dict(by_alias=True, exclude_unset=True))
    
    def get_distinct(self, param: Literal['sector', 'topic', 'insight', 'region', 'country', 'pestle', 'source', 'title'], filter: RecordFilterRequestModel):
        if param not in ['sector', 'topic', 'insight', 'region', 'country', 'pestle', 'source', 'title']:
            raise BlackCofferException("Invalid distinct param call", status_code=status.HTTP_400_BAD_REQUEST)
        
        return self.__records_collection.distinct(param, filter.dict(by_alias=True, exclude_unset=True))