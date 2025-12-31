"""Base classes and interfaces for LLM models."""

from abc import ABC, abstractmethod
from typing import Any, List, Optional


class BaseLLMModel(ABC):
    """Base interface for LLM chat models.

    모든 LLM 모델은 이 인터페이스를 구현해야 합니다.
    LangChain의 BaseChatModel과 호환되도록 설계되었습니다.
    """

    def __init__(self, model_path: str, **kwargs):
        """Initialize the model.

        Args:
            model_path: Path to the model directory or identifier.
            **kwargs: Additional model-specific parameters.
        """
        self.model_path = model_path
        self._model = None
        self._is_loaded = False

    @abstractmethod
    def load(self) -> None:
        """Load the model into memory."""
        pass

    @abstractmethod
    def unload(self) -> None:
        """Unload the model from memory."""
        pass

    @abstractmethod
    def invoke(self, messages: List[Any]) -> Any:
        """Invoke the model with messages.

        Args:
            messages: List of message objects (e.g., HumanMessage, SystemMessage).

        Returns:
            Model response.
        """
        pass

    @property
    def is_loaded(self) -> bool:
        """Check if model is loaded."""
        return self._is_loaded

    @property
    def model(self) -> Any:
        """Get the underlying model object."""
        return self._model


class BaseEmbeddingModel(ABC):
    """Base interface for embedding models.

    모든 임베딩 모델은 이 인터페이스를 구현해야 합니다.
    LangChain의 Embeddings와 호환되도록 설계되었습니다.
    """

    def __init__(self, model_path: str, **kwargs):
        """Initialize the embedding model.

        Args:
            model_path: Path to the model directory or identifier.
            **kwargs: Additional model-specific parameters.
        """
        self.model_path = model_path
        self._model = None
        self._is_loaded = False
        self._dimension: Optional[int] = None

    @abstractmethod
    def load(self) -> None:
        """Load the embedding model into memory."""
        pass

    @abstractmethod
    def unload(self) -> None:
        """Unload the embedding model from memory."""
        pass

    @abstractmethod
    def embed_query(self, text: str) -> List[float]:
        """Generate embedding for a single query text.

        Args:
            text: Input text to embed.

        Returns:
            Embedding vector as a list of floats.
        """
        pass

    @abstractmethod
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple documents.

        Args:
            texts: List of input texts to embed.

        Returns:
            List of embedding vectors.
        """
        pass

    @property
    def is_loaded(self) -> bool:
        """Check if model is loaded."""
        return self._is_loaded

    @property
    def dimension(self) -> int:
        """Get the embedding dimension."""
        if self._dimension is None:
            raise ValueError("Model dimension not determined. Load model first.")
        return self._dimension

    @property
    def model(self) -> Any:
        """Get the underlying model object."""
        return self._model

