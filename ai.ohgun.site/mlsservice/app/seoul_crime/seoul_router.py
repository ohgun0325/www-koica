"""
Seoul Crime Router
서울 범죄 데이터 관련 API 라우터
"""

from fastapi import APIRouter, HTTPException
from typing import List, Optional, Dict, Any
import pandas as pd
import os
import sys
import io
import traceback
from contextlib import redirect_stdout, redirect_stderr
from pathlib import Path
from .seoul_service import SeoulService


class TeeOutput:
    """
    출력을 버퍼와 실제 stdout/stderr 둘 다에 전달하는 클래스
    ic() 등 모든 출력이 터미널에도 표시되도록 함
    """
    def __init__(self, buffer, original_stream):
        self.buffer = buffer
        self.original_stream = original_stream
        # 원본 스트림의 속성들을 복사
        self.mode = getattr(original_stream, 'mode', None)
        self.name = getattr(original_stream, 'name', None)
        self.encoding = getattr(original_stream, 'encoding', None)
        self.errors = getattr(original_stream, 'errors', None)
        self.closed = getattr(original_stream, 'closed', False)
    
    def write(self, text):
        # 버퍼에 저장 (API 응답용)
        if text:
            self.buffer.write(text)
            # 실제 stdout/stderr에도 출력 (터미널 로그용 - Docker 컨테이너 로그)
            self.original_stream.write(text)
            self.original_stream.flush()
    
    def flush(self):
        self.buffer.flush()
        if hasattr(self.original_stream, 'flush'):
            self.original_stream.flush()
    
    def writable(self):
        return True
    
    def readable(self):
        return False
    
    def seekable(self):
        return False
    
    def __getattr__(self, name):
        """
        다른 속성/메서드는 원본 스트림에서 가져옴
        (ic() 등이 사용할 수 있는 모든 메서드 지원)
        """
        return getattr(self.original_stream, name)

# APIRouter 생성 (prefix와 tags 설정)
seoul_router = APIRouter(prefix="/seoul", tags=["seoul"])

# 서비스 인스턴스 생성
_service_instance: Optional[SeoulService] = None

def get_service() -> SeoulService:
    """서비스 싱글톤 인스턴스 반환"""
    global _service_instance
    if _service_instance is None:
        _service_instance = SeoulService()
    return _service_instance


@seoul_router.get("/")
async def seoul_root():
    """서울 범죄 서비스 상태 확인"""
    service = get_service()
    return {
        "message": "서울 범죄 데이터 서비스",
        "status": "running",
        "description": "서울시 범죄, CCTV, 인구 데이터를 활용한 데이터 분석 서비스"
    }


@seoul_router.post("/preview")
@seoul_router.get("/preview")
async def preview_data():
    """
    3개 데이터(CCTV, Crime, Population)의 상위 5개 목록을 화면에 출력
    
    Returns:
        각 데이터의 상위 5개 행과 기본 정보
    """
    try:
        service = get_service()
        log_buffer = io.StringIO()
        
        # stdout과 stderr를 캡처
        with redirect_stdout(log_buffer), redirect_stderr(log_buffer):
            try:
                result = service.show_data_preview()
            except Exception as inner_e:
                # 내부 에러도 로그에 포함
                traceback.print_exc(file=log_buffer)
                raise inner_e
        
        # 캡처된 로그 가져오기
        logs = log_buffer.getvalue()
        
        # 로그를 리스트로 변환 (빈 줄 제거)
        log_lines = [line for line in logs.split('\n') if line.strip()]
        
        return {
            "message": "데이터 미리보기 완료",
            "status": "success",
            "result": result,
            "logs": log_lines
        }
    except Exception as e:
        error_trace = traceback.format_exc()
        return {
            "message": "데이터 미리보기 중 오류 발생",
            "status": "error",
            "error": str(e),
            "error_trace": error_trace.split('\n'),
            "logs": []
        }


@seoul_router.get("/data/cctv")
async def get_cctv_data():
    """
    CCTV 데이터 조회 (상위 5개)
    
    Returns:
        CCTV 데이터의 상위 5개 행
    """
    try:
        service = get_service()
        df_cctv = service.method.load_cctv()
        
        # NaN, inf 값을 None으로 변환하여 JSON 직렬화 가능하게 함
        df_cctv = df_cctv.replace([float('inf'), float('-inf')], None)
        df_cctv = df_cctv.where(pd.notna(df_cctv), None)
        
        # 상위 5개 선택
        top_5 = df_cctv.head(5)
        
        # DataFrame을 딕셔너리 리스트로 변환
        cctv_list = top_5.to_dict(orient='records')
        
        # 딕셔너리 내부의 모든 값도 확인하여 inf, nan 처리
        for record in cctv_list:
            for key, value in record.items():
                if pd.isna(value) or (isinstance(value, float) and (value == float('inf') or value == float('-inf'))):
                    record[key] = None
        
        return {
            "success": True,
            "count": len(cctv_list),
            "total_rows": len(df_cctv),
            "data": cctv_list
        }
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"CCTV 데이터 조회 중 오류 발생: {str(e)}"
        )


@seoul_router.get("/data/crime")
async def get_crime_data():
    """
    범죄 데이터 조회 (상위 5개)
    
    Returns:
        범죄 데이터의 상위 5개 행
    """
    try:
        service = get_service()
        df_crime = service.method.load_crime()
        
        # NaN, inf 값을 None으로 변환하여 JSON 직렬화 가능하게 함
        df_crime = df_crime.replace([float('inf'), float('-inf')], None)
        df_crime = df_crime.where(pd.notna(df_crime), None)
        
        # 상위 5개 선택
        top_5 = df_crime.head(5)
        
        # DataFrame을 딕셔너리 리스트로 변환
        crime_list = top_5.to_dict(orient='records')
        
        # 딕셔너리 내부의 모든 값도 확인하여 inf, nan 처리
        for record in crime_list:
            for key, value in record.items():
                if pd.isna(value) or (isinstance(value, float) and (value == float('inf') or value == float('-inf'))):
                    record[key] = None
        
        return {
            "success": True,
            "count": len(crime_list),
            "total_rows": len(df_crime),
            "data": crime_list
        }
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"범죄 데이터 조회 중 오류 발생: {str(e)}"
        )


@seoul_router.get("/data/population")
async def get_population_data():
    """
    인구 데이터 조회 (상위 5개)
    
    Returns:
        인구 데이터의 상위 5개 행
    """
    try:
        service = get_service()
        df_population = service.method.load_population()
        
        # NaN, inf 값을 None으로 변환하여 JSON 직렬화 가능하게 함
        df_population = df_population.replace([float('inf'), float('-inf')], None)
        df_population = df_population.where(pd.notna(df_population), None)
        
        # 상위 5개 선택
        top_5 = df_population.head(5)
        
        # DataFrame을 딕셔너리 리스트로 변환
        population_list = top_5.to_dict(orient='records')
        
        # 딕셔너리 내부의 모든 값도 확인하여 inf, nan 처리
        for record in population_list:
            for key, value in record.items():
                if pd.isna(value) or (isinstance(value, float) and (value == float('inf') or value == float('-inf'))):
                    record[key] = None
        
        return {
            "success": True,
            "count": len(population_list),
            "total_rows": len(df_population),
            "data": population_list
        }
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"인구 데이터 조회 중 오류 발생: {str(e)}"
        )


@seoul_router.get("/data/merged")
async def get_merged_data():
    """
    CCTV와 인구 데이터 머지 결과 조회 (상위 5개)
    
    Returns:
        머지된 데이터의 상위 5개 행
    """
    try:
        service = get_service()
        df_merged = service.method.merge_cctv_pop()
        
        # NaN, inf 값을 None으로 변환하여 JSON 직렬화 가능하게 함
        df_merged = df_merged.replace([float('inf'), float('-inf')], None)
        df_merged = df_merged.where(pd.notna(df_merged), None)
        
        # 상위 5개 선택
        top_5 = df_merged.head(5)
        
        # DataFrame을 딕셔너리 리스트로 변환
        merged_list = top_5.to_dict(orient='records')
        
        # 딕셔너리 내부의 모든 값도 확인하여 inf, nan 처리
        for record in merged_list:
            for key, value in record.items():
                if pd.isna(value) or (isinstance(value, float) and (value == float('inf') or value == float('-inf'))):
                    record[key] = None
        
        return {
            "success": True,
            "count": len(merged_list),
            "total_rows": len(df_merged),
            "columns": df_merged.columns.tolist(),
            "data": merged_list
        }
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"머지 데이터 조회 중 오류 발생: {str(e)}"
        )


@seoul_router.get("/data/crime-cctv")
async def get_crime_cctv_merged_data():
    """
    범죄와 CCTV 데이터 머지 결과 조회 (상위 5개)
    
    Returns:
        머지된 데이터의 상위 5개 행 (관서명, 기관명, CCTV_소계, 범죄 데이터...)
    """
    try:
        service = get_service()
        df_merged = service.method.merge_crime_cctv()
        
        # NaN, inf 값을 None으로 변환하여 JSON 직렬화 가능하게 함
        df_merged = df_merged.replace([float('inf'), float('-inf')], None)
        df_merged = df_merged.where(pd.notna(df_merged), None)
        
        # 상위 5개 선택
        top_5 = df_merged.head(5)
        
        # DataFrame을 딕셔너리 리스트로 변환
        merged_list = top_5.to_dict(orient='records')
        
        # 딕셔너리 내부의 모든 값도 확인하여 inf, nan 처리
        for record in merged_list:
            for key, value in record.items():
                if pd.isna(value) or (isinstance(value, float) and (value == float('inf') or value == float('-inf'))):
                    record[key] = None
        
        return {
            "success": True,
            "count": len(merged_list),
            "total_rows": len(df_merged),
            "columns": df_merged.columns.tolist(),
            "data": merged_list
        }
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"범죄-CCTV 머지 데이터 조회 중 오류 발생: {str(e)}"
        )


@seoul_router.get("/police-stations/geocoding")
async def get_police_stations_geocoding():
    """
    경찰서 지오코딩 정보 조회
    
    카카오 로컬 API를 사용하여 서울시 경찰서들의 좌표 정보를 가져옵니다.
    
    Returns:
        경찰서 개수와 지오코딩 결과
    """
    try:
        service = get_service()
        result = service.get_police_stations_with_geocoding()
        
        return {
            "success": True,
            "total_count": result["total_count"],
            "success_count": result["success_count"],
            "fail_count": result["fail_count"],
            "police_stations": result["police_stations"],
            "geocoding_results": result["geocoding_results"]
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"경찰서 지오코딩 중 오류 발생: {str(e)}"
        )

