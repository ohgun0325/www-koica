from pydantic import BaseModel, Field
from typing import Optional


class SentimentRequest(BaseModel):
    """감성 분석 요청 스키마"""
    text: str = Field(..., description="분석할 텍스트", min_length=1, max_length=512)
    
    class Config:
        json_schema_extra = {
            "example": {
                "text": "이 영화 정말 재미있었어요! 강력 추천합니다."
            }
        }


class SentimentResponse(BaseModel):
    """감성 분석 응답 스키마"""
    text: str = Field(..., description="입력된 텍스트")
    sentiment: str = Field(..., description="감성 분석 결과 (positive/negative)")
    confidence: float = Field(..., description="신뢰도 (0.0 ~ 1.0)")
    positive_score: float = Field(..., description="긍정 점수")
    negative_score: float = Field(..., description="부정 점수")
    
    class Config:
        json_schema_extra = {
            "example": {
                "text": "이 영화 정말 재미있었어요! 강력 추천합니다.",
                "sentiment": "positive",
                "confidence": 0.95,
                "positive_score": 0.95,
                "negative_score": 0.05
            }
        }

