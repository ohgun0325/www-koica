from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
import uvicorn
import pandas as pd
import os

# 타이타닉 라우터 import
from app.titanic.titanic_router import titanic_router
# AIFIX 라우터 import
from app.aifix.aifix_router import aifix_router
# KOICA 라우터 import
from app.koica.koica_router import koica_router
# 서울 범죄 라우터 import
from app.seoul_crime.seoul_router import seoul_router
# NLP 라우터 import
from app.nlp.nlp_router import nlp_router
# USA Unemployment 라우터 import
from app.us_unemployment.router import usa_router

app = FastAPI(
    title="ML Service API",
    description="""
    ## Machine Learning 서비스 API
    
    타이타닉, AIFIX ESG 평가, KOICA 국제기구사업, 서울 범죄 데이터셋을 활용한 머신러닝 서비스입니다.
    
    ### 주요 기능
    - 타이타닉 승객 데이터 CRUD 작업
    - AIFIX ESG 평가 데이터 CRUD 작업
    - KOICA 국제기구사업 데이터 CRUD 작업
    - 서울 범죄, CCTV, 인구 데이터 조회 및 분석
    - 자연어 처리 및 워드클라우드 생성
    - 생존 여부, 객실 등급, 성별 등 다양한 조건으로 조회
    - ESG 등급, 환경, 사회, 지배구조 등급 조회
    - 데이터 통계 정보 제공
    
    ### 사용 방법
    1. **Swagger UI**: `/docs` 엔드포인트에서 인터랙티브 API 문서 확인
    2. **ReDoc**: `/redoc` 엔드포인트에서 상세 문서 확인
    3. **OpenAPI JSON**: `/openapi.json` 엔드포인트에서 스키마 다운로드
    """,
    version="1.0.0",
    contact={
        "name": "ML Service Team",
        "email": "mlservice@example.com",
    },
    license_info={
        "name": "MIT",
    },
    servers=[
        {
            "url": "http://localhost:9004",
            "description": "로컬 개발 서버"
        },
        {
            "url": "http://localhost:9004",
            "description": "Docker 컨테이너 서버"
        }
    ],
    tags_metadata=[
        {
            "name": "titanic",
            "description": "타이타닉 승객 데이터 관련 API",
            "externalDocs": {
                "description": "타이타닉 데이터셋 정보",
                "url": "https://www.kaggle.com/c/titanic",
            },
        },
        {
            "name": "aifix",
            "description": "AIFIX ESG 평가 데이터 관련 API",
            "externalDocs": {
                "description": "AIFIX ESG 평가 데이터셋",
                "url": "https://www.ohgun.site",
            },
        },
        {
            "name": "koica",
            "description": "KOICA 국제기구사업 데이터 관련 API",
            "externalDocs": {
                "description": "KOICA 국제기구사업 데이터셋",
                "url": "https://www.koica.go.kr",
            },
        },
        {
            "name": "seoul",
            "description": "서울 범죄 데이터 관련 API",
            "externalDocs": {
                "description": "서울시 범죄, CCTV, 인구 데이터셋",
                "url": "https://data.seoul.go.kr",
            },
        },
        {
            "name": "nlp",
            "description": "자연어 처리 및 워드클라우드 생성 API",
            "externalDocs": {
                "description": "NLTK 자연어 처리",
                "url": "https://www.nltk.org",
            },
        },
    ]
)

# 타이타닉 라우터 등록
app.include_router(titanic_router)
# AIFIX 라우터 등록
app.include_router(aifix_router)
# KOICA 라우터 등록
app.include_router(koica_router)
# 서울 범죄 라우터 등록
app.include_router(seoul_router)
# NLP 라우터 등록
app.include_router(nlp_router)
# USA 실업률 라우터 등록
app.include_router(usa_router)

# 루트 엔드포인트
@app.get("/")
async def root():
    return {
        "message": "ML Service",
        "status": "running",
        "services": ["titanic", "aifix", "koica", "seoul", "nlp"]
    }

# 헬스 체크 엔드포인트
@app.get("/health", tags=["health"])
async def health():
    """
    서비스 헬스 체크
    
    서비스가 정상적으로 동작 중인지 확인합니다.
    """
    return {"status": "healthy"}


# Swagger 커스터마이징
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    # 추가 커스터마이징
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi


if __name__ == "__main__":
    # train.csv 파일에서 상위 10명 출력
    try:
        # CSV 파일 경로 설정
        csv_path = os.path.join(os.path.dirname(__file__), "titanic", "train.csv")
        
        # CSV 파일 읽기
        df = pd.read_csv(csv_path)
        
        # 상위 10명 선택 (PassengerId 기준)
        top_10 = df.head(10)
        
        # 터미널에 출력
        print("\n" + "="*80)
        print("Train.csv 상위 10명")
        print("="*80)
        print(top_10.to_string(index=False))
        print("="*80 + "\n")
        
    except Exception as e:
        print(f"CSV 파일 읽기 오류: {e}")
    
    uvicorn.run(app, host="0.0.0.0", port=9004)