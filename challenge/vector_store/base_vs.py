import os
from llama_index.core import (
    StorageContext,
    VectorStoreIndex,
)
from llama_index.core.schema import Document
from abc import abstractmethod
from typing import (
    List,
    Union,
    Tuple,
)
from llama_index.core.vector_stores.types import (
    BasePydanticVectorStore,
    VectorStore,
)


class BaseVectorStore:
    """Base vector store interface"""

    def __init__(self, db_name : str) -> None:
        self.docs_path = os.environ.get('DOCS_PATH')
        self.db_path = os.environ.get('DB_PATH')
        self.db_name = db_name

    @abstractmethod
    def getDocuments(self) -> List[Document]:
        """Read documents on DOCS_PATH for database

        Returns:
            List of documents
        """

    @abstractmethod
    def getDatabase(self) -> Tuple[Union[VectorStore,BasePydanticVectorStore], StorageContext]:
        """Load/Create database on DB_PATH

        Returns:
            List of VectorStore and StorageContext
        """

    @abstractmethod
    def buildIndex(self) -> VectorStoreIndex:
        """Build vector store indexes for further querying

        Returns:
            VectorStoreIndex for querying
        """


