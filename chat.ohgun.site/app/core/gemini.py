"""Google Gemini API integration."""

from typing import Optional

from config import settings

try:
    from langchain_google_genai import (
        ChatGoogleGenerativeAI,
        GoogleGenerativeAIEmbeddings,
    )
    from langchain_core.messages import HumanMessage
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    ChatGoogleGenerativeAI = None  # type: ignore
    GoogleGenerativeAIEmbeddings = None  # type: ignore


def test_gemini_api() -> int:
    """Test if Gemini API is available and return embedding dimension.

    Returns:
        Embedding dimension if API is available and working, otherwise 0.
    """
    if not GEMINI_AVAILABLE:
        return 0

    if not settings.gemini_api_key:
        return 0

    try:
        embeddings_model = GoogleGenerativeAIEmbeddings(
            model=settings.gemini_embedding_model,
            google_api_key=settings.gemini_api_key,
        )
        # Test with a single word to check if API works and get dimension
        test_embedding = embeddings_model.embed_query("test")
        return len(test_embedding)
    except Exception:
        return 0


def get_chat_model() -> Optional[ChatGoogleGenerativeAI]:
    """Get initialized Gemini chat model.

    Returns:
        ChatGoogleGenerativeAI instance if available, None otherwise.
    """
    if not GEMINI_AVAILABLE:
        print("⚠️  langchain_google_genai 모듈을 사용할 수 없습니다.")
        return None

    if not settings.gemini_api_key:
        print("⚠️  settings.gemini_api_key가 None이거나 빈 문자열입니다.")
        return None

    # 환경 변수와 설정값 디버깅
    import os
    env_gemini_model = os.getenv('GEMINI_MODEL', 'not set in env')
    print(f"🔍 환경 변수 GEMINI_MODEL: {env_gemini_model}")
    print(f"🔍 settings.gemini_model: {settings.gemini_model}")
    print(f"🔑 Gemini API 키 확인: 길이={len(settings.gemini_api_key)}, 모델={settings.gemini_model}")

    try:
        chat_model = ChatGoogleGenerativeAI(
            model=settings.gemini_model,
            google_api_key=settings.gemini_api_key,
            temperature=settings.gemini_temperature,
        )

        print(f"✅ ChatGoogleGenerativeAI 인스턴스 생성 완료 (모델: {settings.gemini_model})")

        # Test if it works
        print("🧪 Gemini API 테스트 호출 중...")
        test_response = chat_model.invoke([HumanMessage(content="test")])
        print(f"✅ Gemini API 테스트 호출 성공! 응답 타입: {type(test_response)}")
        return chat_model
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Gemini API 오류 발생:")
        print(f"   에러 타입: {type(e).__name__}")
        print(f"   에러 메시지 (전체): {error_msg}")

        # 더 자세한 에러 정보 출력
        if hasattr(e, 'response'):
            print(f"   응답 객체: {e.response}")
        if hasattr(e, 'status_code'):
            print(f"   상태 코드: {e.status_code}")
        if hasattr(e, 'details'):
            print(f"   상세 정보: {e.details}")

        if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
            print("⚠️  Gemini API 할당량 초과. 검색 기능만 사용 가능합니다.")
        elif "401" in error_msg or "UNAUTHENTICATED" in error_msg or "API key" in error_msg.lower():
            print("⚠️  Gemini API 키 인증 실패. API 키를 확인하세요.")
        elif "INVALID_ARGUMENT" in error_msg or "400" in error_msg:
            print(f"⚠️  Gemini API 잘못된 요청. 모델명({settings.gemini_model})을 확인하세요.")
        else:
            print(f"⚠️  Gemini API 알 수 없는 오류: {error_msg[:200]}")

        import traceback
        traceback.print_exc()
        return None


def get_embeddings_model() -> Optional[GoogleGenerativeAIEmbeddings]:
    """Get initialized Gemini embeddings model.

    Returns:
        GoogleGenerativeAIEmbeddings instance if available, None otherwise.
    """
    if not GEMINI_AVAILABLE or not settings.gemini_api_key:
        return None

    try:
        return GoogleGenerativeAIEmbeddings(
            model=settings.gemini_embedding_model,
            google_api_key=settings.gemini_api_key,
        )
    except Exception:
        return None

