from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.base.embeddings.base import BaseEmbedding
import os

def embeddingModels(model_name : str = "") -> BaseEmbedding:
    """A wrapper for choosing embedding models"""
    if model_name == "":
        model_name = os.environ.get("EMBEDDING_MODEL")
    if model_name == 'flagembedding':
        return HuggingFaceEmbedding(model_name = "BAAI/bge-small-en-v1.5")
    if model_name == 'snowflake':
        return HuggingFaceEmbedding(model_name = 'Snowflake/snowflake-arctic-embed-l')
    raise SystemExit("Model not implemented yet!")
