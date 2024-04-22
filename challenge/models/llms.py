from llama_index.llms.ollama import Ollama
from llama_index.llms.openai import OpenAI
from llama_index.core.llms.llm import LLM
import os

def LLMs(model_name : str = "") -> LLM:
    """A wrapper for choosing large language models"""
    if model_name == "":
        model_name = os.environ.get("MODEL_NAME")
    if model_name == 'llama2':
        return Ollama(model = 'llama2', request_timeout=600.0)
    elif model_name == 'llama3':
        return Ollama(model = 'llama3', request_timeout=600.0)
    elif model_name == 'GPT-3':
        return OpenAI(model = 'gpt-3.5-turbo')
    raise SystemExit('Model not implemented yet!')

