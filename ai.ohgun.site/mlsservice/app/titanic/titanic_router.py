"""
Titanic Router
타이타닉 데이터 관련 API 라우터
"""

from fastapi import APIRouter, HTTPException
from typing import List, Optional, Dict, Any
import pandas as pd
import os
import sys
import io
from contextlib import redirect_stdout, redirect_stderr
from pathlib import Path
from .titanic_service import TitanicService


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
titanic_router = APIRouter(prefix="/titanic", tags=["titanic"])

# 서비스 인스턴스 생성
_service_instance: Optional[TitanicService] = None

def get_service() -> TitanicService:
    """서비스 싱글톤 인스턴스 반환"""
    global _service_instance
    if _service_instance is None:
        _service_instance = TitanicService()
    return _service_instance


@titanic_router.get("/")
async def titanic_root():
    """타이타닉 서비스 상태 확인"""
    service = get_service()
    return {
        "message": "타이타닉 머신러닝 서비스",
        "status": "running",
        "description": "타이타닉 데이터셋을 활용한 머신러닝 서비스"
    }


@titanic_router.post("/preprocess")
async def preprocess():
    """데이터 전처리 실행"""
    import traceback
    try:
        service = get_service()
        # 로그를 캡처하기 위한 StringIO 버퍼
        log_buffer = io.StringIO()
        
        # stdout과 stderr를 캡처
        with redirect_stdout(log_buffer), redirect_stderr(log_buffer):
            try:
                service.preprogress()
            except Exception as inner_e:
                # 내부 에러도 로그에 포함
                traceback.print_exc(file=log_buffer)
                raise inner_e
        
        # 캡처된 로그 가져오기
        logs = log_buffer.getvalue()
        
        # 로그를 리스트로 변환 (빈 줄 제거)
        log_lines = [line for line in logs.split('\n') if line.strip()]
        
        return {
            "message": "전처리 완료",
            "status": "success",
            "logs": log_lines
        }
    except Exception as e:
        error_trace = traceback.format_exc()
        return {
            "message": "전처리 중 오류 발생",
            "status": "error",
            "error": str(e),
            "error_trace": error_trace.split('\n'),
            "logs": []
        }


@titanic_router.post("/modeling")
async def modeling():
    """모델링 실행"""
    try:
        service = get_service()
        log_buffer = io.StringIO()
        
        with redirect_stdout(log_buffer), redirect_stderr(log_buffer):
            service.modeling()
        
        logs = log_buffer.getvalue()
        
        return {
            "message": "모델링 완료",
            "status": "success",
            "logs": logs.split('\n') if logs else []
        }
    except Exception as e:
        return {
            "message": "모델링 중 오류 발생",
            "status": "error",
            "error": str(e),
            "logs": []
        }


@titanic_router.post("/learning")
async def learning():
    """학습 실행"""
    try:
        service = get_service()
        log_buffer = io.StringIO()
        
        with redirect_stdout(log_buffer), redirect_stderr(log_buffer):
            service.learning()
        
        logs = log_buffer.getvalue()
        
        return {
            "message": "학습 완료",
            "status": "success",
            "logs": logs.split('\n') if logs else []
        }
    except Exception as e:
        return {
            "message": "학습 중 오류 발생",
            "status": "error",
            "error": str(e),
            "logs": []
        }


@titanic_router.post("/evaluating")
async def evaluating():
    """평가 실행"""
    try:
        service = get_service()
        log_buffer = io.StringIO()
        
        with redirect_stdout(log_buffer), redirect_stderr(log_buffer):
            service.evaluating()
        
        logs = log_buffer.getvalue()
        
        return {
            "message": "평가 완료",
            "status": "success",
            "logs": logs.split('\n') if logs else []
        }
    except Exception as e:
        return {
            "message": "평가 중 오류 발생",
            "status": "error",
            "error": str(e),
            "logs": []
        }


# GET 메서드도 지원 (Postman에서 GET 호출 시 405 방지)
@titanic_router.get("/evaluating")
async def evaluating_get():
    return await evaluating()


@titanic_router.post("/submit")
async def submit():
    """제출 실행"""
    try:
        service = get_service()
        log_buffer = io.StringIO()
        
        with redirect_stdout(log_buffer), redirect_stderr(log_buffer):
            service.submit()
        
        logs = log_buffer.getvalue()
        
        return {
            "message": "제출 완료",
            "status": "success",
            "logs": logs.split('\n') if logs else []
        }
    except Exception as e:
        return {
            "message": "제출 중 오류 발생",
            "status": "error",
            "error": str(e),
            "logs": []
        }


async def _execute_preprocess():
    """
    전처리 실행 공통 로직
    터미널과 API 응답 둘 다에 로그 출력
    """
    import traceback
    try:
        service = get_service()
        log_buffer = io.StringIO()
        
        # Docker 컨테이너의 실제 stdout/stderr 가져오기
        # Docker에서는 sys.stdout이 이미 컨테이너의 stdout과 연결되어 있음
        # 하지만 버퍼링을 피하기 위해 sys.stderr도 사용
        original_stdout = sys.stdout
        original_stderr = sys.stderr
        
        # TeeOutput으로 버퍼와 실제 stdout/stderr 둘 다에 출력
        # Docker 컨테이너의 stdout/stderr는 자동으로 docker logs에 표시됨
        tee_stdout = TeeOutput(log_buffer, original_stdout)
        tee_stderr = TeeOutput(log_buffer, original_stderr)
        
        # stdout과 stderr를 TeeOutput으로 리다이렉트
        sys.stdout = tee_stdout
        sys.stderr = tee_stderr
        
        # Python의 출력 버퍼링 비활성화 (즉시 출력 보장)
        import os
        os.environ['PYTHONUNBUFFERED'] = '1'
        
        try:
            service.preprogress()
            # 모든 출력이 flush되도록 보장
            sys.stdout.flush()
            sys.stderr.flush()
        except Exception as inner_e:
            # 내부 에러도 로그에 포함
            traceback.print_exc(file=tee_stderr)
            sys.stderr.flush()
            raise inner_e
        finally:
            # 모든 출력 flush
            sys.stdout.flush()
            sys.stderr.flush()
            # 원본 stdout/stderr 복원
            sys.stdout = original_stdout
            sys.stderr = original_stderr
        
        # 캡처된 로그 가져오기
        logs = log_buffer.getvalue()
        
        # 로그를 리스트로 변환 (빈 줄 제거)
        log_lines = [line for line in logs.split('\n') if line.strip()]
        
        return {
            "message": "전처리 완료",
            "status": "success",
            "logs": log_lines
        }
    except Exception as e:
        error_trace = traceback.format_exc()
        # 에러도 터미널에 출력
        print(f"❌ 전처리 중 오류 발생: {e}", file=sys.stderr)
        print(error_trace, file=sys.stderr)
        return {
            "message": "전처리 중 오류 발생",
            "status": "error",
            "error": str(e),
            "error_trace": error_trace.split('\n'),
            "logs": []
        }


@titanic_router.get("/preprocess/run")
async def preprocess_run_get():
    """
    TitanicService.preprogress 실행 (GET 방식)
    브라우저나 화면에서 직접 접근 가능
    """
    return await _execute_preprocess()


@titanic_router.post("/preprocess/run")
async def preprocess_run_post():
    """
    TitanicService.preprogress 실행 (POST 방식)
    API 클라이언트에서 호출 가능
    """
    return await _execute_preprocess()


@titanic_router.get("/passengers/top10")
async def get_top_10_passengers():
    """
    train.csv 파일에서 상위 10명의 승객 목록을 조회합니다.
    
    Returns:
        상위 10명의 승객 정보 리스트
    """
    try:
        # CSV 파일 경로 설정
        current_dir = Path(__file__).parent
        csv_path = current_dir / "train.csv"
        
        # 파일 존재 확인
        if not csv_path.exists():
            raise HTTPException(
                status_code=404, 
                detail=f"train.csv 파일을 찾을 수 없습니다: {csv_path}"
            )
        
        # CSV 파일 읽기
        df = pd.read_csv(csv_path)
        
        # 상위 10명 선택 (PassengerId 기준)
        top_10 = df.head(10)
        
        # NaN, inf 값을 None으로 변환하여 JSON 직렬화 가능하게 함
        top_10 = top_10.replace([float('inf'), float('-inf')], None)
        top_10 = top_10.where(pd.notna(top_10), None)
        
        # DataFrame을 딕셔너리 리스트로 변환
        passengers_list = top_10.to_dict(orient='records')
        
        # 딕셔너리 내부의 모든 값도 확인하여 inf, nan 처리
        for passenger in passengers_list:
            for key, value in passenger.items():
                if pd.isna(value) or (isinstance(value, float) and (value == float('inf') or value == float('-inf'))):
                    passenger[key] = None
        
        return {
            "success": True,
            "count": len(passengers_list),
            "data": passengers_list
        }
        
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"데이터 조회 중 오류 발생: {str(e)}"
        )


@titanic_router.post("/submit")
@titanic_router.get("/submit")
async def submit_prediction():
    """
    RandomForest 모델로 test.csv 예측 후 Kaggle 제출용 CSV 생성
    
    Returns:
        제출 파일 생성 결과 및 상위 10개 예측 결과
    """
    try:
        service = TitanicService()
        
        # TeeOutput을 사용하여 터미널 로그도 출력
        stdout_buffer = io.StringIO()
        stderr_buffer = io.StringIO()
        
        tee_stdout = TeeOutput(stdout_buffer, sys.__stdout__)
        tee_stderr = TeeOutput(stderr_buffer, sys.__stderr__)
        
        result = None
        with redirect_stdout(tee_stdout), redirect_stderr(tee_stderr):
            result = service.submit()
        
        # 버퍼에서 출력 로그 가져오기
        captured_logs = stdout_buffer.getvalue() + stderr_buffer.getvalue()
        
        # ANSI 색상 코드 제거
        import re
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        clean_logs = ansi_escape.sub('', captured_logs)
        
        return {
            "status": "success",
            "message": "Kaggle 제출 파일이 생성되었습니다",
            "result": result,
            "logs": clean_logs
        }
        
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        raise HTTPException(
            status_code=500,
            detail=f"제출 파일 생성 중 오류 발생: {str(e)}\n{error_detail}"
        )

