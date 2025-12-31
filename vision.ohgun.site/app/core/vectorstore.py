"""pgvector operations and vector store management."""

from typing import List, Tuple

import psycopg2

from app.core.database import get_db_connection
from app.core.embeddings import generate_embeddings, get_embedding_dimension


def setup_pgvector() -> tuple[psycopg2.extensions.connection, int]:
    """Setup pgvector extension and create sample table.

    Returns:
        Tuple of (database connection object, embedding dimension).
    """
    # Get connection without registering vector (extension not installed yet)
    conn = get_db_connection(register_vector_extension=False)
    cur = conn.cursor()

    # Enable pgvector extension
    try:
        cur.execute("CREATE EXTENSION IF NOT EXISTS vector")
        conn.commit()
        print("✅ pgvector 확장 설치 완료!")
    except psycopg2.ProgrammingError as e:
        # Extension might already exist or permission issue
        if "already exists" not in str(e).lower():
            print(f"⚠️  pgvector 확장 설치 중 오류: {str(e)[:100]}")
            raise
        conn.commit()

    # Now register the vector extension
    from pgvector.psycopg2 import register_vector
    register_vector(conn)

    # Get embedding dimension
    embedding_dim = get_embedding_dimension()

    # Create sample table for embeddings (Neon pgvector 표준 구조)
    cur.execute("DROP TABLE IF EXISTS langchain_documents")
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS langchain_documents (
            id BIGSERIAL PRIMARY KEY,
            content TEXT NOT NULL,
            metadata JSONB,
            embedding VECTOR({embedding_dim}) NOT NULL
        )
    """)

    # Create HNSW index for vector similarity search (성능 향상)
    try:
        cur.execute("""
            CREATE INDEX IF NOT EXISTS langchain_documents_embedding_idx
            ON langchain_documents
            USING hnsw (embedding vector_cosine_ops)
        """)
        print("✅ HNSW 인덱스 생성 완료!")
    except psycopg2.ProgrammingError as e:
        # 인덱스 생성 실패 시 경고만 출력 (이미 존재하거나 권한 문제)
        if "already exists" not in str(e).lower():
            print(f"⚠️  HNSW 인덱스 생성 중 오류 (계속 진행): {str(e)[:100]}")
        else:
            print("✅ HNSW 인덱스 이미 존재함")

    conn.commit()
    print(f"✅ pgvector 확장 및 테이블 생성 완료! (임베딩 차원: {embedding_dim})")

    return conn, embedding_dim


def insert_sample_data(conn: psycopg2.extensions.connection, dimension: int) -> None:
    """Insert sample documents with embeddings.

    Args:
        conn: Database connection object.
        dimension: Expected embedding dimension.
    """
    cur = conn.cursor()

    # Sample documents
    sample_docs = [
        "LangChain is a framework for developing applications powered by language models. It provides tools for building AI applications with LLMs.",
        "pgvector is a PostgreSQL extension that enables vector similarity search. It allows you to store and query high-dimensional vectors efficiently.",
        "Vector databases store embeddings which are numerical representations of text, images, or other data. They enable semantic search and similarity matching.",
        "RAG (Retrieval Augmented Generation) combines information retrieval with language models to provide more accurate and context-aware responses.",
        "Embeddings are dense vector representations that capture semantic meaning. Similar concepts have similar embeddings in the vector space.",
        "LangChain supports multiple LLM providers including OpenAI, Anthropic, and open-source models. It provides a unified interface for working with different models.",
    ]

    # Generate embeddings
    embeddings = generate_embeddings(sample_docs, dimension)

    # Insert documents with embeddings
    for content, embedding in zip(sample_docs, embeddings):
        cur.execute(
            "INSERT INTO langchain_documents (content, embedding) VALUES (%s, %s::vector)",
            (content, embedding)
        )

    conn.commit()
    print(f"✅ {len(sample_docs)}개의 샘플 문서 삽입 완료!")


def query_similar_documents(
    conn: psycopg2.extensions.connection,
    query_embedding: List[float],
    limit: int = 3
) -> List[Tuple[int, str, float]]:
    """Query documents similar to the given embedding.

    Args:
        conn: Database connection object.
        query_embedding: Query vector for similarity search.
        limit: Maximum number of results to return.

    Returns:
        List of tuples (doc_id, content, distance).
    """
    # psycopg2 연결은 스레드 안전하지 않으므로 연결 상태 확인
    try:
        # 연결이 닫혔는지 확인
        if hasattr(conn, 'closed') and conn.closed:
            raise psycopg2.InterfaceError("Connection is closed")
        # 연결 테스트 (간단한 쿼리)
        test_cur = conn.cursor()
        test_cur.execute("SELECT 1")
        test_cur.close()
    except (psycopg2.InterfaceError, psycopg2.OperationalError, AttributeError):
        # 연결이 닫혔거나 문제가 있으면 새 연결 생성
        # (스레드에서 실행될 때 연결이 닫힐 수 있음)
        from app.core.database import get_db_connection
        conn = get_db_connection(register_vector_extension=True)

    cur = conn.cursor()

    # Find similar documents using cosine distance
    cur.execute(
        """
        SELECT id, content, embedding <=> %s::vector AS distance
        FROM langchain_documents
        ORDER BY distance
        LIMIT %s
        """,
        (query_embedding, limit)
    )

    results = cur.fetchall()
    return results

