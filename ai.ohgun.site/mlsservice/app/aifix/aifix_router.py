"""
AIFIX Router
AIFIX ESG 평가 데이터 관련 API 라우터
"""

from fastapi import APIRouter, HTTPException
from typing import List, Optional, Dict, Any
import pandas as pd
import os
from pathlib import Path
from .aifix_service import AifixService

# APIRouter 생성 (prefix와 tags 설정)
aifix_router = APIRouter(prefix="/aifix", tags=["aifix"])

# 서비스 인스턴스 생성
_service_instance: Optional[AifixService] = None

def get_service() -> AifixService:
    """서비스 싱글톤 인스턴스 반환"""
    global _service_instance
    if _service_instance is None:
        _service_instance = AifixService()
    return _service_instance


@aifix_router.get("/")
async def aifix_root():
    """AIFIX 서비스 상태 확인"""
    service = get_service()
    return {
        "message": "AIFIX ESG 평가 머신러닝 서비스",
        "status": "running",
        "description": "AIFIX ESG 평가 데이터셋을 활용한 머신러닝 서비스"
    }


@aifix_router.post("/preprocess")
async def preprocess():
    """데이터 전처리 실행"""
    service = get_service()
    service.preprogress()
    return {
        "message": "전처리 완료",
        "status": "success"
    }


@aifix_router.post("/modeling")
async def modeling():
    """모델링 실행"""
    service = get_service()
    service.modeling()
    return {
        "message": "모델링 완료",
        "status": "success"
    }


@aifix_router.post("/learning")
async def learning():
    """학습 실행"""
    service = get_service()
    service.learning()
    return {
        "message": "학습 완료",
        "status": "success"
    }


@aifix_router.post("/evaluating")
async def evaluating():
    """평가 실행"""
    service = get_service()
    service.evaluating()
    return {
        "message": "평가 완료",
        "status": "success"
    }


@aifix_router.post("/submit")
async def submit():
    """제출 실행"""
    service = get_service()
    service.submit()
    return {
        "message": "제출 완료",
        "status": "success"
    }


@aifix_router.get("/companies/top10")
async def get_top_10_companies():
    """
    grade.csv 파일에서 상위 10개 기업 목록을 조회합니다.
    
    NO 컬럼 기준으로 내림차순 정렬하여 상위 10개를 반환합니다.
    
    Returns:
        {
            "success": bool,
            "count": int,
            "data": List[Dict] - 상위 10개 기업 정보 리스트
        }
    """
    try:
        # CSV 파일 경로 설정
        current_dir = Path(__file__).parent
        csv_path = current_dir / "grade.csv"
        
        # 파일 존재 확인
        if not csv_path.exists():
            raise HTTPException(
                status_code=404, 
                detail=f"grade.csv 파일을 찾을 수 없습니다: {csv_path}"
            )
        
        # CSV 파일 읽기 (UTF-8 인코딩)
        df = pd.read_csv(csv_path, encoding='utf-8')
        
        # NO 컬럼이 있는지 확인
        if 'NO' not in df.columns:
            raise HTTPException(
                status_code=400,
                detail="CSV 파일에 'NO' 컬럼이 없습니다."
            )
        
        # NO 기준으로 내림차순 정렬 (NO가 큰 순서대로)
        df_sorted = df.sort_values('NO', ascending=False)
        
        # 상위 10개 선택
        top_10 = df_sorted.head(10)
        
        # NaN, inf 값을 None으로 변환하여 JSON 직렬화 가능하게 함
        top_10 = top_10.replace([float('inf'), float('-inf')], None)
        top_10 = top_10.where(pd.notna(top_10), None)
        
        # DataFrame을 딕셔너리 리스트로 변환
        companies_list = top_10.to_dict(orient='records')
        
        # 딕셔너리 내부의 모든 값도 확인하여 inf, nan, 빈 문자열 처리
        for company in companies_list:
            for key, value in company.items():
                # NaN, inf 값 처리
                if pd.isna(value) or (isinstance(value, float) and (value == float('inf') or value == float('-inf'))):
                    company[key] = None
                # 빈 문자열 처리
                elif isinstance(value, str) and value.strip() == '':
                    company[key] = None
        
        return {
            "success": True,
            "count": len(companies_list),
            "data": companies_list
        }
        
    except HTTPException:
        # HTTPException은 그대로 전달
        raise
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except pd.errors.EmptyDataError:
        raise HTTPException(
            status_code=400,
            detail="CSV 파일이 비어있습니다."
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"데이터 조회 중 오류 발생: {str(e)}"
        )


