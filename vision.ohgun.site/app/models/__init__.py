"""Model management package for LLM models."""

from app.models.base import BaseLLMModel, BaseEmbeddingModel
from app.models.loader import ModelLoader
from app.models.manager import ModelManager

# Import model implementations
try:
    from app.models.midm import MidmLLM
    __all__ = [
        "BaseLLMModel",
        "BaseEmbeddingModel",
        "ModelLoader",
        "ModelManager",
        "MidmLLM",
    ]
except ImportError:
    __all__ = [
        "BaseLLMModel",
        "BaseEmbeddingModel",
        "ModelLoader",
        "ModelManager",
    ]

