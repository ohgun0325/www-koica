"""RAG chat chain implementation."""

from typing import Optional, Union

import psycopg2

from app.core.embeddings import generate_embeddings
from app.core.vectorstore import query_similar_documents
from app.models.base import BaseLLMModel

try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain_core.messages import HumanMessage, SystemMessage
except ImportError:
    ChatGoogleGenerativeAI = None  # type: ignore
    HumanMessage = None  # type: ignore
    SystemMessage = None  # type: ignore


def chat_with_ai(
    conn: psycopg2.extensions.connection,
    user_input: str,
    dimension: int,
    chat_model: Optional[Union[BaseLLMModel, ChatGoogleGenerativeAI]] = None
) -> str:
    """Chat with AI using RAG (Retrieval Augmented Generation).

    Args:
        conn: Database connection object.
        user_input: User's question or message.
        dimension: Expected embedding dimension.
        chat_model: Chat model instance (BaseLLMModel or ChatGoogleGenerativeAI).

    Returns:
        AI's response as a string.
    """
    # Generate embedding for user query
    print("🔍 관련 문서 검색 중...")
    query_embeddings = generate_embeddings([user_input], dimension)
    query_vector = query_embeddings[0]

    # Search for similar documents
    similar_docs = query_similar_documents(conn, query_vector, limit=3)

    # If chat model is not available, return search results only
    if chat_model is None:
        if similar_docs:
            context = "\n\n".join([content for _, content, _ in similar_docs])
            return f"""⚠️ 채팅 모델을 사용할 수 없습니다.

하지만 데이터베이스에서 관련 문서를 찾았습니다:

{context}

이 정보를 참고하시기 바랍니다."""
        else:
            return "⚠️ 채팅 모델을 사용할 수 없고, 관련 문서도 찾지 못했습니다."

    # Check if it's a BaseLLMModel (Midm) or Gemini model
    is_base_model = isinstance(chat_model, BaseLLMModel)

    # Prepare messages
    if is_base_model:
        # BaseLLMModel (Midm) - use list format with improved prompt
        # Format context more naturally (remove bullet points)
        formatted_context = "\n\n".join([content for _, content, _ in similar_docs])

        # Create a concise, natural system prompt for Midm
        system_content = f"""당신은 친절한 AI 어시스턴트입니다. 아래 정보를 바탕으로 사용자의 질문에 자연스럽고 대화하듯이 답변해주세요. 정보를 나열하지 말고 자신의 말로 쉽게 설명하세요.

참고 정보:
{formatted_context}"""

        messages = [
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_input}
        ]
    else:
        # Gemini model - use LangChain messages with improved prompt
        if SystemMessage is None or HumanMessage is None:
            return "❌ LangChain 메시지 클래스를 사용할 수 없습니다."

        # Format context more naturally (remove bullet points)
        formatted_context = "\n\n".join([content for _, content, _ in similar_docs])

        messages = [
            SystemMessage(content=f"""당신은 친절하고 도움이 되는 AI 어시스턴트입니다.

다음은 사용자의 질문과 관련된 참고 정보입니다:

{formatted_context}

**중요 지시사항:**
1. 위 정보를 바탕으로 사용자의 질문에 자연스럽고 대화하듯이 답변하세요.
2. 정보를 불릿 포인트나 번호로 나열하지 말고, 자신의 말로 쉽고 이해하기 쉽게 풀어서 설명하세요.
3. 친절하고 자연스러운 톤으로 대화하듯이 답변하세요.
4. 참고 정보에 없는 내용이 필요하면 일반적인 지식을 바탕으로 보완할 수 있습니다.
5. "참고 문서", "참고 정보" 같은 표현을 사용하지 말고, 자연스럽게 정보를 통합하여 답변하세요."""),
            HumanMessage(content=user_input)
        ]

    # Get AI response with error handling
    print("🤖 AI가 응답 생성 중...")
    try:
        response = chat_model.invoke(messages)

        # Handle different response formats
        if is_base_model:
            # BaseLLMModel returns string directly
            return str(response)
        else:
            # Gemini returns object with .content attribute
            return response.content if hasattr(response, 'content') else str(response)

    except Exception as e:
        error_msg = str(e)
        print(f"❌ 모델 응답 생성 오류: {error_msg[:200]}")

        # Fallback to search results
        if similar_docs:
            context = "\n\n".join([content for _, content, _ in similar_docs])
            return f"""⚠️ 모델 응답 생성 중 오류가 발생했습니다.

하지만 데이터베이스에서 관련 문서를 찾았습니다:

{context}

이 정보를 참고하시기 바랍니다."""
        else:
            return f"❌ 오류 발생: {error_msg[:200]}"

