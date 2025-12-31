"""Model loader for loading LLM models from disk."""

import os
from pathlib import Path
from typing import Optional, Type, TypeVar

from app.models.base import BaseEmbeddingModel, BaseLLMModel

T = TypeVar("T", bound=BaseLLMModel)
E = TypeVar("E", bound=BaseEmbeddingModel)


class ModelLoader:
    """Loader for LLM models from local storage or HuggingFace.

    모델을 로드하고 초기화하는 책임을 가집니다.
    다양한 모델 형식(HuggingFace, ONNX 등)을 지원할 수 있도록 확장 가능하게 설계되었습니다.
    """

    def __init__(self, models_dir: str = "models"):
        """Initialize the model loader.

        Args:
            models_dir: Base directory where models are stored.
        """
        self.models_dir = Path(models_dir)
        self.models_dir.mkdir(parents=True, exist_ok=True)

    def get_model_path(self, model_name: str) -> Path:
        """Get the full path to a model directory.

        Args:
            model_name: Name of the model (directory name).

        Returns:
            Path to the model directory.
        """
        return self.models_dir / model_name

    def model_exists(self, model_name: str) -> bool:
        """Check if a model exists.

        Args:
            model_name: Name of the model.

        Returns:
            True if model directory exists and contains required files.
            Also returns True if model can be loaded from HuggingFace Hub.
        """
        model_path = self.get_model_path(model_name)

        # Check local directory first
        if model_path.exists():
            # Check for common model files
            required_files = ["config.json"]
            if all((model_path / f).exists() for f in required_files):
                return True

        # If local model doesn't exist, check if it's a HuggingFace model ID
        # This allows loading from HuggingFace Hub even if not downloaded locally
        # Note: This is a simple check - actual loading will happen in the model class
        return True  # Allow loading from HuggingFace Hub

    def list_models(self) -> list[str]:
        """List all available models.

        Returns:
            List of model names (directory names).
        """
        if not self.models_dir.exists():
            return []

        models = []
        for item in self.models_dir.iterdir():
            if item.is_dir() and not item.name.startswith("."):
                if self.model_exists(item.name):
                    models.append(item.name)

        return models

    def load_chat_model(
        self,
        model_name: str,
        model_class: Type[T],
        **kwargs
    ) -> Optional[T]:
        """Load a chat model.

        Args:
            model_name: Name of the model to load (local directory name or HuggingFace ID).
            model_class: Class that implements BaseLLMModel.
            **kwargs: Additional arguments to pass to model_class.

        Returns:
            Initialized model instance, or None if loading fails.
        """
        # Model name to HuggingFace ID mapping
        MODEL_MAPPING = {
            "midm": "K-intelligence/Midm-2.0-Mini-Instruct",
            "midm-2.0-mini-instruct": "K-intelligence/Midm-2.0-Mini-Instruct",
        }

        # Check if local model exists
        model_path = self.get_model_path(model_name)
        local_model_exists = model_path.exists() and any(
            (model_path / f).exists()
            for f in ["config.json", "model.safetensors", "pytorch_model.bin"]
        )

        if local_model_exists:
            # Use local model path
            load_path = str(model_path)
            print(f"📦 Loading local model: {load_path}")
        else:
            # Try to use as HuggingFace model ID
            # Check if it looks like a HuggingFace ID (contains /)
            if "/" in model_name:
                load_path = model_name
                print(f"📦 Loading from HuggingFace Hub: {load_path}")
            elif model_name.lower() in MODEL_MAPPING:
                # Map model name to HuggingFace ID
                hf_id = MODEL_MAPPING[model_name.lower()]
                load_path = hf_id
                print(f"📦 Loading '{model_name}' from HuggingFace Hub: {load_path}")
            else:
                print(f"⚠️  Model '{model_name}' not found locally and doesn't look like a HuggingFace ID")
                print(f"   Expected local path: {model_path}")
                print(f"   Try using HuggingFace ID format: 'org/model-name'")
                return None

        try:
            model = model_class(model_path=load_path, **kwargs)
            model.load()
            print(f"✅ Model '{model_name}' loaded successfully")
            return model
        except Exception as e:
            print(f"❌ Failed to load model '{model_name}': {str(e)[:100]}")
            import traceback
            traceback.print_exc()
            return None

    def load_embedding_model(
        self,
        model_name: str,
        model_class: Type[E],
        **kwargs
    ) -> Optional[E]:
        """Load an embedding model.

        Args:
            model_name: Name of the model to load.
            model_class: Class that implements BaseEmbeddingModel.
            **kwargs: Additional arguments to pass to model_class.

        Returns:
            Initialized embedding model instance, or None if loading fails.
        """
        if not self.model_exists(model_name):
            print(f"⚠️  Embedding model '{model_name}' not found in {self.models_dir}")
            return None

        model_path = str(self.get_model_path(model_name))

        try:
            model = model_class(model_path=model_path, **kwargs)
            model.load()
            print(f"✅ Embedding model '{model_name}' loaded successfully")
            return model
        except Exception as e:
            print(f"❌ Failed to load embedding model '{model_name}': {str(e)[:100]}")
            return None

