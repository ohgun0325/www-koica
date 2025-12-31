"""
Titanic ML Module
타이타닉 데이터셋을 활용한 머신러닝 모듈
"""

from .titanic_model import TitanicModels
from .titanic_service import TitanicService
from .titanic_router import titanic_router

__version__ = "1.0.0"

__all__ = [
    "TitanicModels",
    "TitanicService",
    "titanic_router",
]

