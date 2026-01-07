# CI/CD 파이프라인 구축 가이드

GitHub Actions + Docker Hub를 사용한 CI/CD 파이프라인 구축 가이드입니다.

## 📋 목차

1. [CI/CD 구조 개요](#cicd-구조-개요)
2. [서브모듈별 GitHub Actions 설정](#서브모듈별-github-actions-설정)
3. [Docker Hub 설정](#docker-hub-설정)
4. [EC2 배포 설정](#ec2-배포-설정)
5. [S3 리소스 배포](#s3-리소스-배포)
6. [전체 워크플로우 예시](#전체-워크플로우-예시)

---

## CI/CD 구조 개요

### 프로젝트 구조

```
www-koica (메인 저장소)
├── admin.ohgun.site → Vercel 배포
├── www.ohgun.site → Vercel 배포
├── api.ohgun.site (서브모듈) → Spring Boot → EC2 배포
├── chat.ohgun.site (서브모듈) → FastAPI → EC2 배포
└── vision.ohgun.site (서브모듈) → FastAPI → EC2 배포
```

### CI/CD 흐름

```
각 서브모듈 저장소
    ↓
GitHub Actions 트리거 (push to main)
    ↓
Docker 이미지 빌드
    ↓
Docker Hub에 푸시
    ↓
EC2에서 이미지 Pull & 배포
    ↓
S3에서 리소스(모델, 이미지) 다운로드
```

### 핵심 포인트

**✅ 각 서브모듈별로 독립적인 GitHub Actions 워크플로우 필요**

- `ohgun-api` 저장소 → `.github/workflows/ci-cd.yml`
- `ohgun-chat` 저장소 → `.github/workflows/ci-cd.yml`
- `ohgun-vision` 저장소 → `.github/workflows/ci-cd.yml`

각 서브모듈은 독립적인 Git 저장소이므로, 각각의 워크플로우가 필요합니다.

---

## 서브모듈별 GitHub Actions 설정

### 1. API 서브모듈 (Spring Boot)

**위치:** `api.ohgun.site/.github/workflows/ci-cd.yml`

```yaml
name: CI/CD Pipeline - API

on:
  push:
    branches:
      - main
    paths:
      - '**'
  pull_request:
    branches:
      - main

env:
  DOCKER_IMAGE_NAME: ohgun0325/ohgun-api
  DOCKER_TAG: latest

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up JDK 21
        uses: actions/setup-java@v4
        with:
          java-version: '21'
          distribution: 'temurin'

      - name: Grant execute permission for gradlew
        run: chmod +x gradlew

      - name: Build with Gradle
        run: ./gradlew build --no-daemon -x test

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}

      - name: Build and push Docker image
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: |
            ${{ env.DOCKER_IMAGE_NAME }}:${{ env.DOCKER_TAG }}
            ${{ env.DOCKER_IMAGE_NAME }}:${{ github.sha }}
          cache-from: type=registry,ref=${{ env.DOCKER_IMAGE_NAME }}:buildcache
          cache-to: type=registry,ref=${{ env.DOCKER_IMAGE_NAME }}:buildcache,mode=max

      - name: Deploy to EC2
        uses: appleboy/ssh-action@v1.0.0
        with:
          host: ${{ secrets.EC2_HOST }}
          username: ${{ secrets.EC2_USERNAME }}
          key: ${{ secrets.EC2_SSH_KEY }}
          script: |
            cd /opt/ohgun-api
            docker-compose pull
            docker-compose up -d --no-deps api
            docker system prune -f
```

### 2. Chat 서브모듈 (FastAPI)

**위치:** `chat.ohgun.site/.github/workflows/ci-cd.yml`

먼저 Dockerfile이 필요합니다. `chat.ohgun.site/Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# 시스템 의존성 설치
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Python 의존성 설치
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY app/ .

# 포트 노출
EXPOSE 8000

# 애플리케이션 실행
CMD ["uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8000"]
```

**워크플로우:** `chat.ohgun.site/.github/workflows/ci-cd.yml`

```yaml
name: CI/CD Pipeline - Chat

on:
  push:
    branches:
      - main
    paths:
      - '**'
  pull_request:
    branches:
      - main

env:
  DOCKER_IMAGE_NAME: ohgun0325/ohgun-chat
  DOCKER_TAG: latest

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r app/requirements.txt

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}

      - name: Build and push Docker image
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: |
            ${{ env.DOCKER_IMAGE_NAME }}:${{ env.DOCKER_TAG }}
            ${{ env.DOCKER_IMAGE_NAME }}:${{ github.sha }}
          cache-from: type=registry,ref=${{ env.DOCKER_IMAGE_NAME }}:buildcache
          cache-to: type=registry,ref=${{ env.DOCKER_IMAGE_NAME }}:buildcache,mode=max

      - name: Deploy to EC2
        uses: appleboy/ssh-action@v1.0.0
        with:
          host: ${{ secrets.EC2_HOST }}
          username: ${{ secrets.EC2_USERNAME }}
          key: ${{ secrets.EC2_SSH_KEY }}
          script: |
            cd /opt/ohgun-chat
            docker-compose pull
            docker-compose up -d --no-deps chat
            docker system prune -f
```

### 3. Vision 서브모듈 (FastAPI)

**위치:** `vision.ohgun.site/.github/workflows/ci-cd.yml`

먼저 Dockerfile이 필요합니다. `vision.ohgun.site/Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# 시스템 의존성 설치
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Python 의존성 설치
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY app/ .

# 포트 노출
EXPOSE 8000

# 애플리케이션 실행
CMD ["uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8000"]
```

**워크플로우:** `vision.ohgun.site/.github/workflows/ci-cd.yml`

```yaml
name: CI/CD Pipeline - Vision

on:
  push:
    branches:
      - main
    paths:
      - '**'
  pull_request:
    branches:
      - main

env:
  DOCKER_IMAGE_NAME: ohgun0325/ohgun-vision
  DOCKER_TAG: latest

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r app/requirements.txt

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}

      - name: Build and push Docker image
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: |
            ${{ env.DOCKER_IMAGE_NAME }}:${{ env.DOCKER_TAG }}
            ${{ env.DOCKER_IMAGE_NAME }}:${{ github.sha }}
          cache-from: type=registry,ref=${{ env.DOCKER_IMAGE_NAME }}:buildcache
          cache-to: type=registry,ref=${{ env.DOCKER_IMAGE_NAME }}:buildcache,mode=max

      - name: Deploy to EC2
        uses: appleboy/ssh-action@v1.0.0
        with:
          host: ${{ secrets.EC2_HOST }}
          username: ${{ secrets.EC2_USERNAME }}
          key: ${{ secrets.EC2_SSH_KEY }}
          script: |
            cd /opt/ohgun-vision
            docker-compose pull
            docker-compose up -d --no-deps vision
            docker system prune -f
```

---

## Docker Hub 설정

### 1. Docker Hub 계정 생성

1. [Docker Hub](https://hub.docker.com/)에 가입
2. 리포지토리 생성:
   - `ohgun-api`
   - `ohgun-chat`
   - `ohgun-vision`

### 2. GitHub Secrets 설정

각 서브모듈 저장소의 Settings → Secrets and variables → Actions에서 다음을 추가:

```
DOCKER_USERNAME: your-dockerhub-username
DOCKER_PASSWORD: your-dockerhub-password
EC2_HOST: your-ec2-ip-or-domain
EC2_USERNAME: ec2-user (또는 ubuntu)
EC2_SSH_KEY: EC2 SSH 개인키
```

---

## EC2 배포 설정

### 1. EC2에 Docker 설치

```bash
# EC2에 SSH 접속 후
sudo yum update -y
sudo yum install docker -y
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker ec2-user

# Docker Compose 설치
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### 2. EC2에 docker-compose.yml 생성

**API 서비스:** `/opt/ohgun-api/docker-compose.yml`

```yaml
version: '3.8'

services:
  api:
    image: ohgun0325/ohgun-api:latest
    container_name: ohgun-api
    ports:
      - "8080:8080"
    environment:
      - SPRING_PROFILES_ACTIVE=production
      - NEON_DB_HOST=${NEON_DB_HOST}
      - NEON_DB_NAME=${NEON_DB_NAME}
      - NEON_DB_USER=${NEON_DB_USER}
      - NEON_DB_PASSWORD=${NEON_DB_PASSWORD}
    restart: unless-stopped
    networks:
      - ohgun-network

networks:
  ohgun-network:
    external: true
```

**Chat 서비스:** `/opt/ohgun-chat/docker-compose.yml`

```yaml
version: '3.8'

services:
  chat:
    image: ohgun0325/ohgun-chat:latest
    container_name: ohgun-chat
    ports:
      - "8001:8000"
    environment:
      - AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
      - AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
      - AWS_S3_BUCKET=${AWS_S3_BUCKET}
      - NEON_DB_HOST=${NEON_DB_HOST}
    restart: unless-stopped
    networks:
      - ohgun-network

networks:
  ohgun-network:
    external: true
```

**Vision 서비스:** `/opt/ohgun-vision/docker-compose.yml`

```yaml
version: '3.8'

services:
  vision:
    image: ohgun0325/ohgun-vision:latest
    container_name: ohgun-vision
    ports:
      - "8002:8000"
    environment:
      - AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
      - AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
      - AWS_S3_BUCKET=${AWS_S3_BUCKET}
      - NEON_DB_HOST=${NEON_DB_HOST}
    restart: unless-stopped
    networks:
      - ohgun-network

networks:
  ohgun-network:
    external: true
```

### 3. EC2에서 네트워크 생성

```bash
docker network create ohgun-network
```

---

## S3 리소스 배포

### 1. S3 버킷 구조

```
s3://ohgun-resources/
├── models/
│   ├── chat/
│   │   └── *.bin, *.pt, *.safetensors
│   └── vision/
│       └── *.bin, *.pt, *.safetensors
├── images/
│   └── ...
└── data/
    └── ...
```

### 2. 애플리케이션에서 S3 접근

**FastAPI (Chat/Vision) 예시:**

```python
import boto3
from botocore.exceptions import ClientError

s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name='ap-northeast-2'
)

def download_model_from_s3(bucket_name, s3_key, local_path):
    try:
        s3_client.download_file(bucket_name, s3_key, local_path)
        return True
    except ClientError as e:
        print(f"Error downloading from S3: {e}")
        return False

# 사용 예시
download_model_from_s3(
    'ohgun-resources',
    'models/chat/model.bin',
    '/app/models/model.bin'
)
```

### 3. Dockerfile에서 S3 리소스 다운로드

**옵션 1: 런타임에 다운로드 (권장)**

```dockerfile
# requirements.txt에 boto3 추가
# app/requirements.txt
boto3>=1.28.0

# Dockerfile은 그대로 유지
# 애플리케이션 시작 시 S3에서 모델 다운로드
```

**옵션 2: 빌드 시 다운로드**

```dockerfile
FROM python:3.11-slim

# AWS CLI 설치
RUN apt-get update && apt-get install -y \
    awscli \
    && rm -rf /var/lib/apt/lists/*

# 환경 변수 설정 (빌드 시)
ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ARG AWS_S3_BUCKET

# S3에서 모델 다운로드
RUN mkdir -p /app/models && \
    aws s3 sync s3://${AWS_S3_BUCKET}/models/chat/ /app/models/ \
    --no-sign-request || true

# 나머지 설정...
```

---

## 전체 워크플로우 예시

### 통합 워크플로우 (선택사항)

메인 저장소(`www-koica`)에서도 전체 통합 테스트를 할 수 있습니다:

**위치:** `.github/workflows/integration-test.yml`

```yaml
name: Integration Test

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main

jobs:
  test-all:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout main repository
        uses: actions/checkout@v4
        with:
          submodules: recursive

      - name: Test API
        run: |
          cd api.ohgun.site
          ./gradlew test

      - name: Test Chat
        run: |
          cd chat.ohgun.site
          pip install -r app/requirements.txt
          pytest app/tests/

      - name: Test Vision
        run: |
          cd vision.ohgun.site
          pip install -r app/requirements.txt
          pytest app/tests/
```

---

## 설정 체크리스트

### 각 서브모듈 저장소에 설정

- [ ] `.github/workflows/ci-cd.yml` 파일 생성
- [ ] `Dockerfile` 생성 (FastAPI의 경우)
- [ ] GitHub Secrets 설정:
  - [ ] `DOCKER_USERNAME`
  - [ ] `DOCKER_PASSWORD`
  - [ ] `EC2_HOST`
  - [ ] `EC2_USERNAME`
  - [ ] `EC2_SSH_KEY`

### Docker Hub

- [ ] Docker Hub 계정 생성
- [ ] 리포지토리 생성:
  - [ ] `ohgun-api`
  - [ ] `ohgun-chat`
  - [ ] `ohgun-vision`

### EC2

- [ ] Docker 설치
- [ ] Docker Compose 설치
- [ ] 네트워크 생성 (`ohgun-network`)
- [ ] 각 서비스 디렉토리 생성:
  - [ ] `/opt/ohgun-api/`
  - [ ] `/opt/ohgun-chat/`
  - [ ] `/opt/ohgun-vision/`
- [ ] `docker-compose.yml` 파일 생성
- [ ] `.env` 파일 생성 (환경 변수)

### S3

- [ ] S3 버킷 생성 (`ohgun-resources`)
- [ ] 모델 파일 업로드
- [ ] IAM 사용자 생성 및 권한 설정
- [ ] AWS Access Key 생성

---

## 배포 흐름

### 1. 개발자가 코드 푸시

```bash
# API 서브모듈에서
cd api.ohgun.site
git add .
git commit -m "feat: 새로운 기능 추가"
git push origin main
```

### 2. GitHub Actions 자동 실행

- 코드 체크아웃
- 빌드 (Gradle 또는 pip)
- Docker 이미지 빌드
- Docker Hub에 푸시
- EC2에 SSH 접속
- Docker Compose로 배포

### 3. EC2에서 자동 배포

```bash
# GitHub Actions가 자동으로 실행
cd /opt/ohgun-api
docker-compose pull
docker-compose up -d --no-deps api
```

### 4. 애플리케이션 시작 시 S3에서 리소스 다운로드

애플리케이션이 시작되면 S3에서 필요한 모델/이미지를 다운로드합니다.

---

## 문제 해결

### 문제 1: Docker Hub 로그인 실패

**해결:** GitHub Secrets에 `DOCKER_USERNAME`과 `DOCKER_PASSWORD`가 올바르게 설정되었는지 확인

### 문제 2: EC2 SSH 접속 실패

**해결:** 
- EC2 Security Group에서 SSH 포트(22) 허용 확인
- SSH 키가 올바른지 확인
- `EC2_SSH_KEY` Secret이 개인키 전체 내용을 포함하는지 확인

### 문제 3: S3 접근 실패

**해결:**
- IAM 사용자 권한 확인
- AWS Access Key가 올바른지 확인
- S3 버킷 정책 확인

---

## 요약

### 핵심 답변

**Q: 각 서브모듈별로 GitHub Actions를 실행해야 하는가?**

**A: 네, 맞습니다!** 각 서브모듈은 독립적인 Git 저장소이므로:

1. **각 서브모듈 저장소에 `.github/workflows/ci-cd.yml` 파일 생성**
2. **각 서브모듈이 독립적으로 CI/CD 파이프라인 실행**
3. **각 서브모듈이 독립적으로 Docker Hub에 이미지 푸시**
4. **각 서브모듈이 독립적으로 EC2에 배포**

### 구조

```
ohgun-api (저장소)
  └── .github/workflows/ci-cd.yml → Docker Hub → EC2

ohgun-chat (저장소)
  └── .github/workflows/ci-cd.yml → Docker Hub → EC2

ohgun-vision (저장소)
  └── .github/workflows/ci-cd.yml → Docker Hub → EC2
```

각 서브모듈이 독립적으로 배포되므로, 하나의 서브모듈만 수정해도 해당 서브모듈만 재배포됩니다.

---

## 작성일

- 작성일: 2025-01-XX
- 프로젝트: www-koica
- 서브모듈: ohgun-api, ohgun-chat, ohgun-vision

