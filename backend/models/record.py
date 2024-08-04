from pydantic import BaseModel, Field, root_validator
from typing import Optional, List, Union, Literal
from datetime import datetime

class Record(BaseModel):
    end_year: Optional[int] = Field(None)
    intensity: Optional[int] = Field(None)
    sector: Optional[str] = Field(None)
    topic: Optional[str] = Field(None)
    insight: str
    url: str
    region: Optional[str] = Field(None)
    start_year: Optional[int] = Field(None)
    impact: Optional[int] = Field(None)
    added: datetime
    published: datetime
    country: Optional[str] = Field(None)
    relevance: Optional[int] = Field(None)
    pestle: Optional[str] = Field(None)
    source: Optional[str] = Field(None)
    title: str
    likelihood: Optional[int] = Field(None)

class IntFilter(BaseModel):
    gt: Optional[int] = Field(None, alias='$gt')
    lt: Optional[int] = Field(None, alias='$lt')
    gte: Optional[int] = Field(None, alias='$gte')
    lte: Optional[int] = Field(None, alias='$lte')
    In: Optional[List[int]] = Field(None, alias='$in')
    nin: Optional[List[int]] = Field(None, alias='$nin')

    @root_validator(pre=False)
    def ensure_atleast_one(cls, values: dict):
        gt_present = values.get('gt') is not None
        gte_present = values.get('gte') is not None
        lt_present = values.get('lt') is not None
        lte_present = values.get('lte') is not None
        in_present = values.get('In') is not None
        nin_present = values.get('nin') is not None
        if gt_present and gte_present:
            raise ValueError("Both $gt and $gte cannot be present")
        if lt_present and lte_present:
            raise ValueError("Both $gt and $gte cannot be present")
        if not (gte_present or gt_present or lte_present or lt_present):
            if not in_present and not nin_present:
                raise ValueError("Atleast one filter required")
        if in_present and len(values.get('$in')) == 0:
                raise ValueError("$in does not have any item")
        if nin_present and len(values.get('$nin')) == 0:
            raise ValueError("$nin does not have any item")
        return values

class DatetimeFilter(BaseModel):
    gt: Optional[datetime] = Field(None, alias='$gt')
    lt: Optional[datetime] = Field(None, alias='$lt')
    gte: Optional[datetime] = Field(None, alias='$gte')
    lte: Optional[datetime] = Field(None, alias='$lte')

    @root_validator(pre=False)
    def ensure_atleast_one(cls, values: dict):
        gt_present = values.get('gt') is not None
        gte_present = values.get('gte') is not None
        lt_present = values.get('lt') is not None
        lte_present = values.get('lte') is not None
        if gt_present and gte_present:
            raise ValueError("Both $gt and $gte cannot be present")
        if lt_present and lte_present:
            raise ValueError("Both $gt and $gte cannot be present")
        return values


class StrFilter(BaseModel):
    In: Optional[List[int]] = Field(None, alias='$in')
    nin: Optional[List[int]] = Field(None, alias='$nin')

    @root_validator(pre=False)
    def ensure_atleast_one(cls, values: dict):
        in_present = values.get('In') is not None
        nin_present = values.get('nin') is not None
        if not in_present and not nin_present:
            raise ValueError("Atleast one filter required")
        if in_present and len(values.get('$in')) == 0:
                raise ValueError("$in does not have any item")
        if nin_present and len(values.get('$nin')) == 0:
            raise ValueError("$nin does not have any item")
        return values

class RecordFilterRequestModel(BaseModel):
    end_year: Union[IntFilter, int, None]
    start_year: Union[int, IntFilter, None]
    impact: Union[int, IntFilter, None]
    intensity: Union[int, IntFilter, None]
    relevance: Union[int, IntFilter, None]
    likelihood: Union[int, IntFilter, None]

    added: Union[datetime, DatetimeFilter, None]
    published: Union[datetime, DatetimeFilter, None]

    sector: Union[str, StrFilter, None]
    topic: Union[str, StrFilter, None]
    insight: Union[str, StrFilter, None]
    region: Union[str, StrFilter, None]
    country: Union[str, StrFilter, None]
    pestle: Union[str, StrFilter, None]
    source: Union[str, StrFilter, None]
    title: Union[str, StrFilter, None]

    @root_validator(pre=False)
    def ensure_atleast_one(cls, values: dict):
        keys = ['end_year', 'start_year', 'impact', 'intensity', 'relevance', 'likelihood', 'added', 'published', 
                'sector', 'topic', 'insight', 'region', 'country', 'pestle', 'source', 'title']
        
        for key in keys:
            val = values.get(key, None)
            if val is not None:
                return values
        # raise ValueError("Atleast one filter expected")
        return values

class PaginatedRecordsResponse(BaseModel):
    count: int
    page: int
    total_pages: int
    records: List[Record]

if __name__ == "__main__":
    print(RecordFilterRequestModel.parse_obj({
        'end_year': {'$gt': 2011}
    }).json(by_alias=True, exclude_unset=True))