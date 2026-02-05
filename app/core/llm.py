from langchain_openai import ChatOpenAI
from langchain_core.language_models.chat_models import BaseChatModel
from app.core.config import settings

def get_llm() -> BaseChatModel:
    """
    Returns the configured LLM instance.
    Defaults to OpenAI, but can be extended for Anthropic, etc.
    """
    if settings.OPENAI_API_KEY:
        return ChatOpenAI(
            api_key=settings.OPENAI_API_KEY,
            model=settings.MODEL_NAME,
            temperature=0
        )
    # Placeholder for Anthropic or other providers
    # elif settings.ANTHROPIC_API_KEY: ...
    
    raise ValueError("No valid LLM API Key found in settings.")
