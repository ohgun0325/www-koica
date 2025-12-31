from fastapi import FastAPI, APIRouter
import uvicorn

# 서브라우터 생성
crawler_router = APIRouter(tags=["crawler"])

@crawler_router.get("/")
async def crawler_root():
    return {"message": "Crawler Service", "status": "running"}

@crawler_router.get("/health")
async def health_check():
    return {"status": "healthy"}

app = FastAPI(
    title="Crawler Service API",
    description="Crawler 서비스 API 문서",
    version="1.0.0"
)

# 서브라우터를 앱에 포함
app.include_router(crawler_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9001)

