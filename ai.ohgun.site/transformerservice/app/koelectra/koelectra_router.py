from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
import logging

from .koelectra_service import get_sentiment_service, KoELECTRASentimentService
from .schemas import SentimentRequest, SentimentResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/sentiment", tags=["sentiment"])


def get_service() -> KoELECTRASentimentService:
    """의존성 주입을 위한 서비스 인스턴스 반환"""
    return get_sentiment_service()


@router.post("/predict", response_model=SentimentResponse)
async def predict_sentiment(
    request: SentimentRequest,
    service: KoELECTRASentimentService = Depends(get_service)
) -> SentimentResponse:
    """
    영화 리뷰 텍스트의 감성을 분석합니다.
    
    - **text**: 분석할 텍스트 (최대 512자)
    
    반환값:
    - **sentiment**: 감성 분석 결과 (positive/negative)
    - **confidence**: 신뢰도 (0.0 ~ 1.0)
    - **positive_score**: 긍정 점수
    - **negative_score**: 부정 점수
    """
    try:
        # 텍스트 길이 검증
        if len(request.text.strip()) == 0:
            raise HTTPException(status_code=400, detail="텍스트가 비어있습니다.")
        
        if len(request.text) > 512:
            raise HTTPException(status_code=400, detail="텍스트는 최대 512자까지 입력 가능합니다.")
        
        # 감성 분석 수행
        result = service.predict(request.text)
        
        return SentimentResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in predict_sentiment: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"감성 분석 중 오류가 발생했습니다: {str(e)}")


@router.get("/health")
async def health_check():
    """서비스 헬스 체크"""
    return {"status": "healthy", "service": "koelectra-sentiment-analysis"}

