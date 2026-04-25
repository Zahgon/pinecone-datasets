import logging
from collections.abc import Generator, Iterator
from typing import TYPE_CHECKING, Any, Optional
from urllib.parse import urlparse

from .cfg import Schema
from .dataset_metadata import DatasetMetadata
from .fs import get_cloud_fs
from .utils import deprecated

if TYPE_CHECKING:
    import pandas as pd

    from .dataset_fsreader import DatasetFSReader
else:
    pd = None  # Placeholder for runtime
    DatasetFSReader = None  # Placeholder for runtime

logger = logging.getLogger(__name__)


def iter_pandas_dataframe_slices(
    df: "pd.DataFrame", batch_size: int, return_indexes: bool
) -> Generator[list[dict[str, Any]], None, None]:
    pass


def iter_pandas_dataframe_single(
    df: "pd.DataFrame",
) -> Generator[dict[str, Any], None, None]:
    pass


class Dataset:
    @classmethod
    def from_path(cls, dataset_path: str, **kwargs: Any) -> "Dataset":
        """
        Create a Dataset object from local or cloud storage
        Args:
            dataset_path (str): a path to a local or cloud storage path containing a valid dataset.

        Returns:
            Dataset: a Dataset object
        """
        return cls(dataset_path=dataset_path, **kwargs)

    @classmethod
    def from_pandas(
        cls,
        documents: "pd.DataFrame",
        metadata: DatasetMetadata,
        documents_column_mapping: Optional[dict] = None,
        queries: Optional["pd.DataFrame"] = None,
        queries_column_mapping: Optional[dict] = None,
        **kwargs: Any,
    ) -> "Dataset":
        """
        Create a Dataset object from a pandas DataFrame

        Args:
            documents (pd.DataFrame): a pandas DataFrame containing the documents
            documents_column_mapping (Dict): a dictionary mapping the columns of the documents DataFrame to the Pinecone Datasets Schema
            queries (pd.DataFrame): a pandas DataFrame containing the queries
            queries_column_mapping (Dict): a dictionary mapping the columns of the queries DataFrame to the Pinecone Datasets Schema

        Keyword Args:
            kwargs (Dict): additional arguments to pass to the fsspec constructor

        Returns:
            Dataset: a Dataset object
        """
        pass

    @staticmethod
    def _read_pandas_dataframe(
        df: "pd.DataFrame",
        column_mapping: dict[str, str],
        schema: list[tuple[str, bool, Any]],
    ) -> "pd.DataFrame":
        """
        Reads a pandas DataFrame and validates it against a schema.

        Args:
            df (pd.DataFrame): the pandas DataFrame to read
            column_mapping (Dict[str, str]): a dictionary mapping the columns of the DataFrame to the Pinecone Datasets Schema (col_name, pinecone_name)
            schema (List[Tuple[str, bool]]): the schema to validate against (column_name, is_nullable)

        Returns:
            pd.DataFrame: the validated, renamed DataFrame
        """
        pass

    def __init__(
        self,
        dataset_path: str,
        **kwargs,
    ) -> None:
        """
        Dataset class to load and query datasets from the Pinecone Datasets catalog.
        See `from_path` and `from_dataset_id` for examples on how to load a dataset.

        Examples:
            ```python
            from pinecone_datasets import Dataset
            dataset = Dataset.from_dataset_id("dataset_name")
            # or
            dataset = Dataset.from_path("gs://my-bucket/my-dataset")

            for doc in dataset.iter_documents(batch_size=100):
                index.upsert(doc)
            for query in dataset.iter_queries(batch_size):
                results = index.search(query)
                # do something with the results
            # or
            dataset.documents # returns a pandas/polars DataFrame
            dataset.queries # returns a pandas/polars DataFrame
            ```

        """
        if dataset_path is not None:
            endpoint = urlparse(dataset_path)._replace(path="").geturl()
            self._fs = get_cloud_fs(endpoint, **kwargs)
            self._dataset_path = dataset_path
            if not self._fs.exists(self._dataset_path):
                raise FileNotFoundError(
                    f"Dataset does not exist at path {self._dataset_path}"
                )
        else:
            self._dataset_path = None
            self._fs = None
        self._documents = None
        self._queries = None
        self._metadata = None

    def __getitem__(self, key: str):
        if key in ["documents", "queries"]:
            return getattr(self, key)
        else:
            raise KeyError(f"Dataset does not have key: {key}")

    def __len__(self) -> int:
        return self.documents.shape[0]

    @property
    def documents(self) -> "pd.DataFrame":
        pass

    @property
    def queries(self) -> "pd.DataFrame":
        pass

    @property
    def metadata(self) -> DatasetMetadata:
        pass

    def iter_documents(
        self, batch_size: int = 1, return_indexes=False
    ) -> Iterator[list[dict[str, Any]]]:
        """
        Iterates over the documents in the dataset.

        Args:
            batch_size (int, optional): The batch size to use for the iterator. Defaults to 1.

        Returns:
            Iterator[List[Dict[str, Any]]]: An iterator over the documents in the dataset.

        Examples:
            for batch in dataset.iter_documents(batch_size=100):
                index.upsert(batch)
        """
        pass

    def iter_queries(self) -> Iterator[dict[str, Any]]:
        """
        Iterates over the queries in the dataset.

        Returns:
            Iterator[Dict[str, Any]]: An iterator over the queries in the dataset.

        Examples:
            for query in dataset.iter_queries():
                results = index.query(**query)
                # do something with the results
        """
        pass

    def head(self, n: int = 5) -> "pd.DataFrame":
        pass

    @deprecated
    @classmethod
    def from_catalog(cls, dataset_id, catalog_base_path: str = "", **kwargs):
        """
        DEPRECATED: This method has been removed. Please use `Catalog.load_dataset` instead.
        """
        raise Exception(
            "This method has been removed. Please use `Catalog.load_dataset` instead."
        )

    @deprecated
    def to_catalog(
        self,
        dataset_id: str,
        catalog_base_path: str = "",
        **kwargs,
    ):
        """
        DEPRECATED: This method has been removed. Please use `Catalog.save_dataset` instead.
        """
        raise Exception(
            "This method has been removed. Please use `Catalog.save_dataset` instead."
        )

    @deprecated
    def to_pinecone_index(self, *args, **kwargs):
        """
        DEPRECATED: This method has been removed. Please use the `pinecone.Index.upsert` method instead from the `pinecone` SDK package.
        """
        raise Exception(
            "This method has been removed. Please use the `pinecone.Index.upsert` method instead from the `pinecone` SDK package."
        )
