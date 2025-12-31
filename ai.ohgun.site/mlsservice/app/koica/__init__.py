"""
KOICA ML Module
KOICA 국제기구사업 데이터셋을 활용한 머신러닝 모듈
"""

from .koica_model import KoicaModels
from .koica_service import KoicaService
from .koica_router import koica_router

__version__ = "1.0.0"

__all__ = [
    "KoicaModels",
    "KoicaService",
    "koica_router",
]

