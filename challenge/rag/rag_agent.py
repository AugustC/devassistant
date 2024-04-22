from llama_index.core.agent import ReActAgent
from llama_index.core.tools import (
    QueryEngineTool,
    ToolMetadata,
)
from llama_index.core import PromptTemplate
from llama_index.core.llms.llm import LLM
from challenge.rag.query_engine import QueryEngine
from challenge.prompts.agent_prompt import AGENT_PROMPT

class RAGAgent:
    """RAGAgent object creates an agent for querying the database for AWS documentation

    Args:
        llm (LLM) : Large Language Model to be used in the agent
        query_engine (QueryEngine) : Query engine that the agent will use as its tool

    Attributes:
        llm (LLM) : LLM the agent will use
        query_engine (QueryEngine) : Query engine used by the agent
        prompt (str) : Prompt used for the agent
    """

    def __init__(self,
                 llm: LLM,
                 query_engine: QueryEngine) -> None:
        self.llm = llm
        self.query_engine = query_engine
        self.prompt = AGENT_PROMPT

    def updatePrompt(self, prompt : str) -> str:
        """Add prompt template for agent

        Returns:
            Added prompt template
        """
        self.prompt = prompt
        return prompt

    def buildAgent(self) -> "ReActAgent":
        """Builds an agent with the tool to query AWS documentation

        Returns:
            Created agent
        """
        query_engine_tools = [
            QueryEngineTool(
                query_engine = self.query_engine,
                metadata = ToolMetadata(
                    name = 'documentation_agent',
                    description = 'Provides information about AWS documentation.'
                    ' Use this tool only if the user requested information about AWS',
                ),
            ),
        ]
        agent = ReActAgent.from_tools(query_engine_tools,
                                           llm = self.llm,
                                           verbose = True)
        prompt = PromptTemplate(self.prompt)
        agent.update_prompts({ 'agent_worker:system_prompt' : prompt})
        agent.reset()

        self.agent = agent
        return self.agent
