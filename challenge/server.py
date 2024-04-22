import dotenv
import os
from challenge.slack.api import SlackPlugin
from challenge.models import (
    LLMs,
    embeddingModels,
)
from challenge.rag import (
    RAGAgent,
    QueryEngine,
)
from challenge.vector_store import (
    ChromaVS,
)
from llama_index.core import Settings

dotenv.load_dotenv()

# Setting embedding and llm models
Settings.embed_model = embeddingModels()
Settings.llm = LLMs()

# Create Vector Store
vector_store = ChromaVS()

# Create Query Engine 
query_engine_builder = QueryEngine(vector_store)
query_engine = query_engine_builder.buildQueryEngine()

# Create Agent for RAG queries
agent_builder = RAGAgent(Settings.llm, query_engine)
agent = agent_builder.buildAgent()

# Create Integration App
slack_plugin = SlackPlugin(agent)
handler = slack_plugin.handler

if __name__ == "__main__":
    handler.start()
