from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel


class DenseModelMetadata(BaseModel):
    name: str
    tokenizer: Optional[str] = None
    dimension: int


class SparseModelMetdata(BaseModel):
    name: Optional[str] = None
    tokenizer: Optional[str] = None


def get_time_now() -> str:
    pass


class DatasetMetadata(BaseModel):
    name: str
    created_at: str
    documents: int
    queries: int
    source: Optional[str] = None
    license: Optional[str] = None
    bucket: Optional[str] = None
    task: Optional[str] = None
    dense_model: DenseModelMetadata
    sparse_model: Optional[SparseModelMetdata] = None
    description: Optional[str] = None
    tags: Optional[list[str]] = None
    args: Optional[dict[str, Any]] = None

    @staticmethod
    def empty() -> "DatasetMetadata":
        pass

    def is_empty(self) -> bool:
        pass
