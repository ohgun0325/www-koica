"""Model manager for managing LLM model lifecycle."""

from typing import Optional

from app.models.base import BaseEmbeddingModel, BaseLLMModel
from app.models.loader import ModelLoader
from config import settings


class ModelManager:
    """Singleton manager for LLM models.

    모델의 생명주기를 관리하고, 모델 인스턴스를 캐싱하며,
    여러 모델을 동시에 관리할 수 있습니다.
    """

    _instance: Optional["ModelManager"] = None
    _chat_model: Optional[BaseLLMModel] = None
    _embedding_model: Optional[BaseEmbeddingModel] = None

    def __new__(cls):
        """Create singleton instance."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._loader = ModelLoader(
                models_dir=settings.local_models_dir
            )
        return cls._instance

    @property
    def loader(self) -> ModelLoader:
        """Get the model loader."""
        return self._loader

    def get_chat_model(
        self,
        model_name: Optional[str] = None,
        force_reload: bool = False
    ) -> Optional[BaseLLMModel]:
        """Get or load a chat model.

        Args:
            model_name: Name of the model to load. If None, uses default from config.
            force_reload: If True, reload the model even if already loaded.

        Returns:
            Chat model instance, or None if loading fails.
        """
        if model_name is None:
            model_name = settings.default_chat_model

        if model_name is None:
            return None

        # Return cached model if available and not forcing reload
        if self._chat_model is not None and not force_reload:
            if self._chat_model.is_loaded:
                return self._chat_model

        # Load new model
        # Try to load Midm model if model_name matches
        if model_name.lower() in ["midm", "midm-2.0-mini-instruct", "k-intelligence/midm-2.0-mini-instruct"]:
            try:
                from app.models.midm import MidmLLM
                from config import settings

                # Pass device and dtype from settings
                model = self._loader.load_chat_model(
                    model_name,
                    MidmLLM,
                    device_map=settings.model_device,
                    torch_dtype=settings.model_dtype,
                    trust_remote_code=True
                )
                if model:
                    self._chat_model = model
                    return self._chat_model
                else:
                    print(f"⚠️  Midm 모델 '{model_name}' 로드 실패 - ModelLoader가 None 반환")
            except ImportError as e:
                print(f"⚠️  Midm model not available: {e}")
                print("   Install transformers: pip install transformers torch")
            except Exception as e:
                print(f"⚠️  Failed to load Midm model: {e}")
                import traceback
                traceback.print_exc()

        # For other models, implement custom loading logic here
        print(f"📦 Loading chat model: {model_name}")
        print("   ⚠️  Model loading not implemented for this model type")

        return self._chat_model

    def get_embedding_model(
        self,
        model_name: Optional[str] = None,
        force_reload: bool = False
    ) -> Optional[BaseEmbeddingModel]:
        """Get or load an embedding model.

        Args:
            model_name: Name of the model to load. If None, uses default from config.
            force_reload: If True, reload the model even if already loaded.

        Returns:
            Embedding model instance, or None if loading fails.
        """
        if model_name is None:
            model_name = settings.default_embedding_model

        if model_name is None:
            return None

        # Return cached model if available and not forcing reload
        if self._embedding_model is not None and not force_reload:
            if self._embedding_model.is_loaded:
                return self._embedding_model

        # Load new model
        # Note: 실제 구현에서는 model_class를 전달해야 합니다
        print(f"📦 Loading embedding model: {model_name}")
        print("   ⚠️  Implement model loading logic in get_embedding_model()")

        return self._embedding_model

    def unload_chat_model(self) -> None:
        """Unload the current chat model."""
        if self._chat_model is not None:
            self._chat_model.unload()
            self._chat_model = None
            print("✅ Chat model unloaded")

    def unload_embedding_model(self) -> None:
        """Unload the current embedding model."""
        if self._embedding_model is not None:
            self._embedding_model.unload()
            self._embedding_model = None
            print("✅ Embedding model unloaded")

    def unload_all(self) -> None:
        """Unload all models."""
        self.unload_chat_model()
        self.unload_embedding_model()

    def list_available_models(self) -> list[str]:
        """List all available models.

        Returns:
            List of model names.
        """
        return self._loader.list_models()

