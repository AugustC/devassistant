import os
from challenge.vector_store.base_vs import BaseVectorStore
from llama_index.core import VectorStoreIndex
from llama_index.core import PromptTemplate
from challenge.prompts.query_engine_prompt import QUERY_ENGINE_PROMPT

class QueryEngine:
    """QueryEngine object creates the engine that will query the vector store
    for similar documents

    Args:
        vector_store (BaseVectorStore) : Vector store that will be used for querying
        top_k (int) : Amount of documents to be retrieved when querying

    Attributes:
        vector_store (BaseVectorStore) : Vector store to be queryied
        query_engine (QueryEngine) : Resulting query engine
        prompt_template (PromptTemplate) : Prompt for the query engine
        prompt_template (str) : Prompt added to user query
        top_k (int) : Documents to be retrieved when querying
        index (VectorStoreIndex) : Indexed database
    """

    def __init__(
        self,
        vector_store: BaseVectorStore,
        top_k: int = 2
    ) -> None:
        self.top_k = top_k
        self.vector_store = vector_store
        self.index = None

    def addPromptTemplate(self, template: str) -> str:
        """Add prompt template for final querying

        Returns:
            Added prompt template
        """
        self.prompt_template = PromptTemplate(template)
        self.query_engine.update_prompts({"response_synthesizer:text_qa_template": self.prompt_template})
        return self.prompt_template

    def buildIndex(self) -> VectorStoreIndex:
        """Retrieve indexed database from vector store

        Returns:
            Indexed vector store for the query engine
        """
        self.index = self.vector_store.buildIndex()
        return self.index

    def buildQueryEngine(self) -> "QueryEngine":
        """Build and returns the final query engine

        Returns:
            QueryEngine for input querying
        """
        if self.index == None:
            self.index = self.buildIndex()
        self.query_engine = self.index.as_query_engine(
            similarity_top_k = self.top_k
        )
        return self.query_engine

