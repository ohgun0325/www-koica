from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import os

from app.koelectra.koelectra_router import router as sentiment_router
from app.koelectra.koelectra_service import get_sentiment_service

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# FastAPI 앱 생성
app = FastAPI(
    title="KoELECTRA 감성 분석 API",
    description="KoELECTRA 모델을 사용한 영화 리뷰 감성 분석 서비스",
    version="1.0.0"
)

# CORS 설정 (필요시 수정)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 프로덕션에서는 특정 도메인만 허용하세요
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(sentiment_router)


@app.on_event("startup")
async def startup_event():
    """서버 시작 시 모델 로드"""
    logger.info("Starting up KoELECTRA Sentiment Analysis Service...")
    
    try:
        # 모델 경로 설정
        model_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "app", "koelectra", "koelectra_model"
        )
        
        # 모델 로드
        service = get_sentiment_service()
        service.load_model(model_path)
        
        logger.info("Model loaded successfully!")
        
    except Exception as e:
        logger.error(f"Failed to load model: {e}", exc_info=True)
        raise


@app.get("/")
async def root():
    """루트 엔드포인트"""
    return {
        "message": "KoELECTRA 감성 분석 API",
        "docs": "/docs",
        "health": "/api/v1/sentiment/health"
    }


@app.get("/health")
async def health():
    """전체 서비스 헬스 체크"""
    return {"status": "healthy"}

