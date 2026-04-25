import json
import logging
import os
import warnings
from typing import Literal, Optional

import pandas as pd
import pyarrow.parquet as pq

from .cfg import Schema
from .dataset_metadata import DatasetMetadata
from .fs import CloudOrLocalFS, get_cached_path, is_cloud_path
from .retry import create_cloud_storage_retry_decorator
from .tqdm import tqdm

logger = logging.getLogger(__name__)

retry_decorator = create_cloud_storage_retry_decorator()


class DatasetFSReader:
    @staticmethod
    @retry_decorator
    def read_documents(fs: CloudOrLocalFS, dataset_path: str) -> pd.DataFrame:
        pass

    @staticmethod
    @retry_decorator
    def read_queries(fs: CloudOrLocalFS, dataset_path: str) -> pd.DataFrame:
        pass

    @staticmethod
    @retry_decorator
    def read_metadata(fs: CloudOrLocalFS, dataset_path: str) -> DatasetMetadata:
        pass

    @staticmethod
    def _convert_metadata_from_json_to_dict(metadata: Optional[str] = None) -> dict:
        pass

    @staticmethod
    def _does_datatype_exist(
        fs: CloudOrLocalFS,
        dataset_path: str,
        data_type: Literal["documents", "queries"],
    ) -> bool:
        pass

    @staticmethod
    def _safe_read_from_path(
        fs: CloudOrLocalFS,
        dataset_path: str,
        data_type: Literal["documents", "queries"],
    ) -> pd.DataFrame:
        pass
