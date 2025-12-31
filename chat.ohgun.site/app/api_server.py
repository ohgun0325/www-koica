"""FastAPI server for LangChain chatbot with pgvector."""

import asyncio
from contextlib import asynccontextmanager
from typing import Optional, Union

import psycopg2
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from app.router import chat_router
from app.routes import health_router, search_router
from app.core import (
    insert_sample_data,
    setup_pgvector,
    wait_for_db,
)
from app.models.base import BaseLLMModel
from app.models.manager import ModelManager
from config import settings

try:
    from langchain_google_genai import ChatGoogleGenerativeAI
except ImportError:
    ChatGoogleGenerativeAI = None  # type: ignore


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database connection and chat model on startup."""
    print("🚀 FastAPI 서버 시작 중...")

    # Wait for database (동기 작업을 비동기로 실행)
    await asyncio.to_thread(wait_for_db)

    # Setup pgvector (동기 작업을 비동기로 실행)
    db_connection, embedding_dimension = await asyncio.to_thread(setup_pgvector)
    print(f"✅ 데이터베이스 연결 완료 (임베딩 차원: {embedding_dimension})")

    # Insert sample data if table is empty (동기 작업을 비동기로 실행)
    def check_and_insert_data():
        cur = db_connection.cursor()
        cur.execute("SELECT COUNT(*) FROM langchain_documents")
        count = cur.fetchone()[0]

        if count == 0:
            print("📚 샘플 데이터 삽입 중...")
            insert_sample_data(db_connection, embedding_dimension)
        else:
            print(f"✅ 기존 문서 {count}개 발견")

    await asyncio.to_thread(check_and_insert_data)

    # Initialize QLoRA chat service or fallback to original model
    qlora_service = None
    chat_model: Optional[Union[BaseLLMModel, ChatGoogleGenerativeAI]] = None

    if settings.use_qlora:
        # QLoRA 모델 사용
        try:
            from app.service.chat_service import QLoRAChatService

            print("📦 QLoRA 서비스 초기화 중... (시간이 걸릴 수 있습니다)")

            def init_qlora_service():
                service = QLoRAChatService(
                    model_name=settings.qlora_model_name,
                    output_dir=settings.qlora_output_dir,
                    use_4bit=settings.qlora_use_4bit,
                    bnb_4bit_compute_dtype=settings.qlora_bnb_4bit_compute_dtype,
                    bnb_4bit_quant_type=settings.qlora_bnb_4bit_quant_type,
                    bnb_4bit_use_double_quant=settings.qlora_bnb_4bit_use_double_quant,
                    device_map=settings.qlora_device_map,
                )
                service.load_model()
                return service

            # 타임아웃 설정 (5분)
            try:
                qlora_service = await asyncio.wait_for(
                    asyncio.to_thread(init_qlora_service),
                    timeout=300.0
                )
                print("✅ QLoRA 채팅 서비스 로드 완료!")
            except asyncio.TimeoutError:
                print("⚠️  QLoRA 서비스 로드 타임아웃 (5분 초과)")
                print("   Fallback: 기존 모델 로딩 시도...")
                settings.use_qlora = False
                qlora_service = None
        except KeyboardInterrupt:
            print("\n⚠️  사용자가 QLoRA 로딩을 중단했습니다.")
            print("   Fallback: 기존 모델 로딩 시도...")
            settings.use_qlora = False
            qlora_service = None
        except Exception as e:
            print(f"⚠️  QLoRA 서비스 로드 중 오류: {str(e)}")
            print("   Fallback: 기존 모델 로딩 시도...")
            settings.use_qlora = False
            qlora_service = None

    if not settings.use_qlora or qlora_service is None:
        # 기존 모델 로딩 (QLoRA가 비활성화되었거나 로드 실패한 경우)
        # Try to load Midm model first (동기 작업을 비동기로 실행)
        if settings.default_chat_model:
            try:
                def load_midm_model():
                    manager = ModelManager()
                    return manager.get_chat_model(settings.default_chat_model)

                chat_model = await asyncio.to_thread(load_midm_model)
                if chat_model:
                    print(f"✅ Midm 모델 '{settings.default_chat_model}' 로드 완료!")
                else:
                    print(f"⚠️  Midm 모델 '{settings.default_chat_model}' 로드 실패")
            except Exception as e2:
                print(f"⚠️  Midm 모델 로드 중 오류: {str(e2)[:100]}")

        # Fallback to Gemini API if Midm is not available
        print(f"🔍 Gemini API 로드 시도 - gemini_api_key 설정 여부: {settings.gemini_api_key is not None}")
        if chat_model is None and settings.gemini_api_key:
            print(f"🔑 Gemini API 키 길이: {len(settings.gemini_api_key)} (처음 10자: {settings.gemini_api_key[:10]}...)")
            try:
                def load_gemini_model():
                    from app.core import get_chat_model
                    return get_chat_model()

                gemini_model = await asyncio.to_thread(load_gemini_model)
                if gemini_model:
                    chat_model = gemini_model
                    print("✅ Gemini API 연결 확인 완료!")
                else:
                    print("⚠️  Gemini API를 사용할 수 없습니다. (get_chat_model()이 None 반환)")
            except Exception as e2:
                print(f"⚠️  Gemini API 로드 중 오류: {str(e2)[:200]}")
                import traceback
                traceback.print_exc()
        elif chat_model is None:
            print(f"⚠️  Gemini API 키가 설정되지 않았습니다. settings.gemini_api_key = {settings.gemini_api_key}")

        if chat_model is None:
            print("⚠️  사용 가능한 채팅 모델이 없습니다. 검색 기능만 사용 가능합니다.")

        app.state.chat_model = chat_model
    else:
        # QLoRA를 사용할 때는 chat_model을 None으로 설정 (GPU 메모리 절약)
        app.state.chat_model = None

    # Store in app state
    app.state.db_connection = db_connection
    app.state.embedding_dimension = embedding_dimension
    app.state.qlora_service = qlora_service

    print("✅ FastAPI 서버 준비 완료!")

    yield

    # Cleanup on shutdown (동기 작업을 비동기로 실행)
    qlora_service = getattr(app.state, "qlora_service", None)
    if qlora_service:
        await asyncio.to_thread(qlora_service.unload_model)
        print("👋 QLoRA 서비스 언로드 완료")

    if db_connection:
        await asyncio.to_thread(db_connection.close)
        print("👋 데이터베이스 연결 종료")


# Create FastAPI app
app = FastAPI(
    title=settings.app_title,
    description=settings.app_description,
    version=settings.app_version,
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
)

# Include routers
app.include_router(health_router)
app.include_router(chat_router)
app.include_router(search_router)


@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the main HTML page."""
    try:
        with open("static/index.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return """
        <html>
            <head><title>LangChain Chatbot</title></head>
            <body>
                <h1>LangChain Chatbot API</h1>
                <p>API 문서: <a href="/docs">/docs</a></p>
                <p>프론트엔드: <a href="http://localhost:3000">Next.js 프론트엔드</a></p>
            </body>
        </html>
        """


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.api_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )

