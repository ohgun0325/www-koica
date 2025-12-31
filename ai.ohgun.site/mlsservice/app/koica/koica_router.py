"""
KOICA Router
KOICA 국제기구사업 데이터 관련 API 라우터
"""

from fastapi import APIRouter, HTTPException
from typing import List, Optional, Dict, Any
import pandas as pd
import os
from pathlib import Path
from .koica_service import KoicaService

# APIRouter 생성 (prefix와 tags 설정)
koica_router = APIRouter(prefix="/koica", tags=["koica"])

# 서비스 인스턴스 생성
_service_instance: Optional[KoicaService] = None

def get_service() -> KoicaService:
    """서비스 싱글톤 인스턴스 반환"""
    global _service_instance
    if _service_instance is None:
        _service_instance = KoicaService()
    return _service_instance


@koica_router.get("/")
async def koica_root():
    """KOICA 서비스 상태 확인"""
    service = get_service()
    return {
        "message": "KOICA 국제기구사업 머신러닝 서비스",
        "status": "running",
        "description": "KOICA 국제기구사업 데이터셋을 활용한 머신러닝 서비스"
    }


@koica_router.post("/preprocess")
async def preprocess():
    """데이터 전처리 실행"""
    service = get_service()
    service.preprogress()
    return {
        "message": "전처리 완료",
        "status": "success"
    }


@koica_router.post("/modeling")
async def modeling():
    """모델링 실행"""
    service = get_service()
    service.modeling()
    return {
        "message": "모델링 완료",
        "status": "success"
    }


@koica_router.post("/learning")
async def learning():
    """학습 실행"""
    service = get_service()
    service.learning()
    return {
        "message": "학습 완료",
        "status": "success"
    }


@koica_router.post("/evaluating")
async def evaluating():
    """평가 실행"""
    service = get_service()
    service.evaluating()
    return {
        "message": "평가 완료",
        "status": "success"
    }


@koica_router.post("/submit")
async def submit():
    """제출 실행"""
    service = get_service()
    service.submit()
    return {
        "message": "제출 완료",
        "status": "success"
    }


@koica_router.get("/projects/top10")
async def get_top_10_projects():
    """
    koicainternational.csv 파일에서 상위 10개 사업 목록을 조회합니다.
    
    연번 기준으로 정렬하여 상위 10개를 반환합니다.
    
    Returns:
        {
            "success": bool,
            "count": int,
            "data": List[Dict] - 상위 10개 사업 정보 리스트
        }
    """
    try:
        # CSV 파일 경로 설정
        current_dir = Path(__file__).parent
        csv_path = current_dir / "koicainternational.csv"
        
        # 파일 존재 확인
        if not csv_path.exists():
            raise HTTPException(
                status_code=404, 
                detail=f"koicainternational.csv 파일을 찾을 수 없습니다: {csv_path}"
            )
        
        # CSV 파일 읽기 (UTF-8 BOM 인코딩 지원, 첫 3줄 스킵)
        # 4번째 줄이 헤더, 5번째 줄부터 데이터
        df = pd.read_csv(csv_path, encoding='utf-8-sig', skiprows=3)
        
        # 첫 번째 빈 컬럼 제거 (Unnamed: 0 같은 컬럼)
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        
        # 빈 컬럼 및 행 제거
        df = df.dropna(axis=1, how='all')  # 모든 값이 NaN인 컬럼 제거
        df = df.dropna(axis=0, how='all')  # 모든 값이 NaN인 행 제거
        
        # 연번 컬럼이 있는지 확인하고 정렬
        if '연번' in df.columns:
            # 연번을 숫자로 변환 (NaN이 아닌 경우만)
            df['연번'] = pd.to_numeric(df['연번'], errors='coerce')
            # 연번 기준으로 오름차순 정렬 (작은 번호가 먼저)
            df = df.sort_values('연번', ascending=True, na_position='last')
        
        # 상위 10개 선택
        top_10 = df.head(10)
        
        # NaN, inf 값을 None으로 변환하여 JSON 직렬화 가능하게 함
        top_10 = top_10.replace([float('inf'), float('-inf')], None)
        top_10 = top_10.where(pd.notna(top_10), None)
        
        # DataFrame을 딕셔너리 리스트로 변환
        projects_list = top_10.to_dict(orient='records')
        
        # 딕셔너리 내부의 모든 값도 확인하여 inf, nan, 빈 문자열 처리
        for project in projects_list:
            for key, value in project.items():
                # NaN, inf 값 처리
                if pd.isna(value) or (isinstance(value, float) and (value == float('inf') or value == float('-inf'))):
                    project[key] = None
                # 빈 문자열 처리
                elif isinstance(value, str) and value.strip() == '':
                    project[key] = None
                # #REF! 같은 특수 값 처리
                elif isinstance(value, str) and value.strip() == '#REF!':
                    project[key] = None
        
        if len(projects_list) == 0:
            raise HTTPException(
                status_code=400,
                detail="CSV 파일에 데이터가 없습니다."
            )
        
        return {
            "success": True,
            "count": len(projects_list),
            "data": projects_list
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


