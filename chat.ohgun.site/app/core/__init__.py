"""Core business logic package."""

from app.core.database import get_db_connection, wait_for_db
from app.core.embeddings import generate_embeddings, get_embedding_dimension
from app.core.vectorstore import (
    insert_sample_data,
    query_similar_documents,
    setup_pgvector,
)
from app.core.chat_chain import chat_with_ai
from app.core.gemini import get_chat_model, test_gemini_api

__all__ = [
    "get_db_connection",
    "wait_for_db",
    "generate_embeddings",
    "get_embedding_dimension",
    "insert_sample_data",
    "query_similar_documents",
    "setup_pgvector",
    "chat_with_ai",
    "get_chat_model",
    "test_gemini_api",
]

