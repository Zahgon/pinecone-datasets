import json
import logging
import os
import warnings
from typing import TYPE_CHECKING, Optional

from .fs import CloudOrLocalFS, get_cloud_fs
from .retry import create_cloud_storage_retry_decorator

if TYPE_CHECKING:
    import pandas as pd

    from .dataset import Dataset
else:
    pd = None

logger = logging.getLogger(__name__)

retry_decorator = create_cloud_storage_retry_decorator()


class DatasetFSWriter:
    @staticmethod
    def write_dataset(dataset_path: str, dataset: "Dataset", **kwargs):
        """
        Saves the dataset to a local or cloud storage path.
        """
        pass

    @staticmethod
    @retry_decorator
    def _write_documents(fs: CloudOrLocalFS, dataset_path: str, dataset: "Dataset"):
        pass

    @staticmethod
    @retry_decorator
    def _write_queries(fs: CloudOrLocalFS, dataset_path: str, dataset: "Dataset"):
        pass

    @staticmethod
    @retry_decorator
    def _write_metadata(fs: CloudOrLocalFS, dataset_path: str, dataset: "Dataset"):
        metadata_path = os.path.join(dataset_path, "metadata.json")
        logger.debug(
            f"writing dataset {dataset.metadata.name} metadata to {metadata_path}"
        )
        with fs.open(metadata_path, "w") as f:
            json.dump(dataset.metadata.model_dump(), f)

    @staticmethod
    def _convert_metadata_from_dict_to_json(metadata: Optional[dict]) -> str:
        pass
