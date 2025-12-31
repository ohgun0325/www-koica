"""
NLP Router
자연어 처리 관련 API 라우터
"""

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse, FileResponse
from typing import Optional, List
from pydantic import BaseModel
import base64
import io
import os
from pathlib import Path
from datetime import datetime
from PIL import Image
import matplotlib
matplotlib.use('Agg')  # GUI 백엔드 사용 안 함 (서버 환경)
import matplotlib.pyplot as plt

from .emma.emma_wordcloud import EmmaWordCloud

# APIRouter 생성 (prefix와 tags 설정)
nlp_router = APIRouter(prefix="/nlp", tags=["nlp"])

# 서비스 인스턴스 생성
_emma_instance: Optional[EmmaWordCloud] = None

def get_emma_instance() -> EmmaWordCloud:
    """EmmaWordCloud 싱글톤 인스턴스 반환"""
    global _emma_instance
    if _emma_instance is None:
        _emma_instance = EmmaWordCloud()
    return _emma_instance


class WordCloudRequest(BaseModel):
    """워드클라우드 생성 요청 모델"""
    width: Optional[int] = 1000
    height: Optional[int] = 600
    background_color: Optional[str] = "white"
    random_state: Optional[int] = 0


@nlp_router.get("/")
async def nlp_root():
    """NLP 서비스 상태 확인"""
    return {
        "message": "NLP 자연어 처리 서비스",
        "status": "running",
        "description": "자연어 처리 및 워드클라우드 생성 서비스"
    }


def _create_wordcloud_response(request: WordCloudRequest) -> dict:
    """
    워드클라우드 생성 공통 로직
    
    Args:
        request: WordCloudRequest 객체
    
    Returns:
        응답 딕셔너리
    """
    # EmmaWordCloud 인스턴스 가져오기
    emma = get_emma_instance()
    
    # 워드클라우드 생성 (show=False로 설정하여 화면에 표시하지 않음)
    wc = emma.generate_wordcloud(
        width=request.width,
        height=request.height,
        background_color=request.background_color,
        random_state=request.random_state,
        show=False
    )
    
    # WordCloud 객체를 이미지로 변환
    img = wc.to_image()
    
    # PIL Image를 bytes로 변환
    img_buffer = io.BytesIO()
    img.save(img_buffer, format='PNG')
    img_bytes = img_buffer.getvalue()
    
    # base64로 인코딩
    img_base64 = base64.b64encode(img_bytes).decode('utf-8')
    
    # save 폴더에 이미지 저장
    save_dir = Path(__file__).resolve().parent / "save"
    save_dir.mkdir(exist_ok=True)  # 폴더가 없으면 생성
    
    # 파일명 생성 (타임스탬프 기반)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"emma_wordcloud_{timestamp}.png"
    filepath = save_dir / filename
    # 보기 좋은 상대 경로도 함께 반환 (프로젝트 루트 기준)
    saved_path_relative = str(Path("app") / "nlp" / "save" / filename)
    
    # 이미지 저장
    try:
        img.save(filepath, format='PNG')
        # 저장 확인
        if not filepath.exists():
            raise Exception(f"파일 저장 실패: {filepath}")
    except Exception as e:
        # 저장 실패 시 에러 로깅
        import sys
        print(f"이미지 저장 오류: {e}", file=sys.stderr)
        print(f"저장 시도 경로: {filepath}", file=sys.stderr)
        print(f"저장 디렉토리 존재 여부: {save_dir.exists()}", file=sys.stderr)
        print(f"저장 디렉토리 경로: {save_dir}", file=sys.stderr)
        raise
    
    # matplotlib figure 정리
    plt.close('all')
    
    return {
        "success": True,
        "message": "워드클라우드가 성공적으로 생성되었습니다.",
        "image_base64": img_base64,
        "format": "PNG",
        "width": request.width,
        "height": request.height,
        "background_color": request.background_color,
        "saved_path": str(filepath),
        "saved_path_relative": saved_path_relative,
        "filename": filename
    }


@nlp_router.get("/emma")
async def generate_emma_wordcloud(
    width: Optional[int] = Query(1000, description="워드클라우드 너비 (기본값: 1000)"),
    height: Optional[int] = Query(600, description="워드클라우드 높이 (기본값: 600)"),
    background_color: Optional[str] = Query("white", description="배경색 (기본값: white)"),
    random_state: Optional[int] = Query(0, description="랜덤 시드 (기본값: 0)")
):
    """
    Emma 소설 워드클라우드 생성
    
    GET 요청으로 쿼리 파라미터를 사용하여 워드클라우드를 생성합니다.
    
    Args:
        width: 워드클라우드 너비 (기본값: 1000)
        height: 워드클라우드 높이 (기본값: 600)
        background_color: 배경색 (기본값: "white")
        random_state: 랜덤 시드 (기본값: 0)
    
    Returns:
        {
            "success": bool,
            "message": str,
            "image_base64": str - base64 인코딩된 이미지 데이터,
            "saved_path": str - 저장된 파일 경로,
            "filename": str - 저장된 파일명
        }
    """
    try:
        request = WordCloudRequest(
            width=width,
            height=height,
            background_color=background_color,
            random_state=random_state
        )
        result = _create_wordcloud_response(request)
        return JSONResponse(status_code=200, content=result)
    except Exception as e:
        plt.close('all')
        raise HTTPException(
            status_code=500,
            detail=f"워드클라우드 생성 중 오류 발생: {str(e)}"
        )


@nlp_router.get("/emma/saved")
async def get_saved_wordclouds():
    """
    저장된 워드클라우드 이미지 목록 조회
    
    Returns:
        {
            "success": bool,
            "count": int,
            "images": List[Dict] - 저장된 이미지 정보 리스트
        }
    """
    try:
        save_dir = Path(__file__).resolve().parent / "save"
        save_dir.mkdir(exist_ok=True)
        
        # PNG 파일만 필터링
        image_files = sorted(
            [f for f in save_dir.glob("*.png")],
            key=lambda x: x.stat().st_mtime,
            reverse=True  # 최신 파일 먼저
        )
        
        images = []
        for img_file in image_files:
            stat = img_file.stat()
            images.append({
                "filename": img_file.name,
                "path": str(img_file),
                "path_relative": str(Path("app") / "nlp" / "save" / img_file.name),
                "size": stat.st_size,
                "created_at": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                "download_url": f"/api/ml/nlp/emma/saved/{img_file.name}"
            })
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "count": len(images),
                "images": images
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"저장된 이미지 목록 조회 중 오류 발생: {str(e)}"
        )


@nlp_router.get("/emma/saved/{filename}")
async def download_wordcloud_image(filename: str):
    """
    저장된 워드클라우드 이미지 다운로드
    
    Args:
        filename: 다운로드할 이미지 파일명
    
    Returns:
        이미지 파일 (PNG)
    """
    try:
        save_dir = Path(__file__).resolve().parent / "save"
        filepath = save_dir / filename
        
        # 보안: 상위 디렉토리 접근 방지
        if not filepath.resolve().is_relative_to(save_dir.resolve()):
            raise HTTPException(status_code=400, detail="Invalid file path")
        
        # 파일 존재 확인
        if not filepath.exists():
            raise HTTPException(status_code=404, detail=f"파일을 찾을 수 없습니다: {filename}")
        
        # PNG 파일만 허용
        if not filename.lower().endswith('.png'):
            raise HTTPException(status_code=400, detail="PNG 파일만 다운로드할 수 있습니다.")
        
        return FileResponse(
            path=str(filepath),
            filename=filename,
            media_type="image/png"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"이미지 다운로드 중 오류 발생: {str(e)}"
        )


