FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Python 경로 설정
ENV PYTHONPATH=/app

# 시스템 패키지 업데이트 및 필요한 패키지 설치
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# requirements.txt 먼저 복사하고 설치 (캐시 최적화)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# NLTK 미사용으로 다운로드 단계 제거 (의존성 문제 방지)

# 앱 코드 복사
COPY app ./app

# 포트 노출
EXPOSE 9004

# 서버 실행
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "9004"]

