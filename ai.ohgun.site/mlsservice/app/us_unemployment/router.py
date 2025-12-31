from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse

from .service import USUnemploymentMap

usa_router = APIRouter(prefix="/usa", tags=["usa"])


@usa_router.get("/", summary="USA 실업률 서비스 상태")
async def usa_root():
    return {
        "message": "USA Unemployment Map Service",
        "status": "running",
        "endpoints": ["/usa/map"],
    }


@usa_router.get("/map", response_class=HTMLResponse, summary="USA 실업률 Choropleth 지도")
async def get_usa_unemployment_map():
    """
    미국 주별 실업률 Choropleth 지도 HTML을 반환합니다.
    """
    try:
        service = USUnemploymentMap()
        # 파일 저장 (기본: app/us_unemployment/save/us_unemployment.html)
        saved_path = service.save_html()
        # 브라우저에서 바로 렌더링할 수 있도록 HTML 문자열 반환
        m = service.build_map()
        return HTMLResponse(content=m._repr_html_(), headers={"X-Saved-Path": saved_path})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"지도 생성 중 오류 발생: {e}")
