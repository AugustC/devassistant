import chromadb

from llama_index.core import (
    SimpleDirectoryReader,
    StorageContext,
    VectorStoreIndex
)
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core.schema import Document
from .base_vs import (
    BaseVectorStore,
)
from typing import (
    List,
    Tuple,
)
import os

class ChromaVS(BaseVectorStore):
    """ChromaVS object creates or load the vector database using ChromaDB framework for further querying

    Args:
        db_name (str) : Name of the Chroma collection

    Attributes:
        docs_path (str) : Documents path
        db_path (str) : Database path
        db_name (str) : Chroma collection name
        index (VectorStoreIndex) : Indexed database
    """

    def __init__(self, db_name: str = 'chroma_docs') -> None:
        super().__init__('chroma_docs')
        self.loaded = False

    def buildIndex(self) -> VectorStoreIndex:
        vector_store, storage_context = self.getDatabase()

        if self.loaded:
            self.index = VectorStoreIndex.from_vector_store(
                vector_store,
                storage_context = storage_context,
            )
            return self.index
        else:
            documents = self.getDocuments()
            print('Getting ' + str(len(documents)) + ' documents')
            self.index = VectorStoreIndex.from_documents(
                documents,
                storage_context = storage_context,
            )
            self.index.storage_context.persist(persist_dir = self.db_path + '/index')
            return self.index


    def getDocuments(self) -> List[Document]:
        try:
            reader = SimpleDirectoryReader(input_dir = self.docs_path)
            docs = reader.load_data()
            return docs

        except ValueError as e:
            raise SystemExit('No files in directory ' + str(self.docs_path))


    def getDatabase(self) -> Tuple["ChromaVectorStore", StorageContext]:

        if os.path.exists(self.db_path):
            # Load database
            print('Collection exists')
            client = chromadb.PersistentClient(path = self.db_path)
            collection = client.get_or_create_collection(name = self.db_name)
            self.loaded = True
        else:
            # If there's no db with that name, create it instead 
            print('Collection doesnt exist')
            client = chromadb.PersistentClient(path = self.db_path)
            collection = client.create_collection(name = self.db_name)
            self.loaded = False

        vector_store = ChromaVectorStore(chroma_collection = collection)
        storage_context = StorageContext.from_defaults(vector_store = vector_store)

        return vector_store, storage_context
