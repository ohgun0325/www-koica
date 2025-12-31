"""
AIFIX ML Module
AIFIX ESG 평가 데이터셋을 활용한 머신러닝 모듈
"""

from .aifix_model import AifixModels
from .aifix_service import AifixService
from .aifix_router import aifix_router

__version__ = "1.0.0"

__all__ = [
    "AifixModels",
    "AifixService",
    "aifix_router",
]

