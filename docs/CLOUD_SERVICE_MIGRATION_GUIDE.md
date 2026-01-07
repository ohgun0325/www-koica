# 클라우드 서비스 구축 가이드 (Neon DB + Upstash Redis)

Spring Boot 애플리케이션을 로컬 Docker 컨테이너에서 클라우드 서비스(Neon DB, Upstash Redis)로 전환하는 과정을 정리한 문서입니다.

## 📋 목차

1. [개요](#개요)
2. [전환 전 구조 (로컬 컨테이너)](#전환-전-구조-로컬-컨테이너)
3. [전환 후 구조 (클라우드 서비스)](#전환-후-구조-클라우드-서비스)
4. [구축 과정](#구축-과정)
5. [환경 변수 설정](#환경-변수-설정)
6. [Docker Compose 설정](#docker-compose-설정)
7. [테스트 및 확인](#테스트-및-확인)
8. [Docker Hub 배포](#docker-hub-배포)
9. [GitHub Actions 연동](#github-actions-연동)
10. [문제 해결](#문제-해결)

---

## 개요

### 목표

로컬에서 실행되던 PostgreSQL과 Redis 컨테이너를 클라우드 관리형 서비스로 전환하여:
- **데이터베이스 관리 부담 감소**
- **백업 및 복구 자동화**
- **확장성 향상**
- **다른 서버에서도 동일한 데이터 접근 가능**

### 사용 서비스

- **Neon DB**: Serverless PostgreSQL (AWS Singapore)
- **Upstash Redis**: Serverless Redis with Global Edge Network

---

## 전환 전 구조 (로컬 컨테이너)

### Docker Compose 구조

```yaml
services:
  postgres:
    image: postgres:17-alpine
    container_name: ohgun-postgres
    environment:
      POSTGRES_DB: ohgun
      POSTGRES_USER: ohgun
      POSTGRES_PASSWORD: ohgun1234
    ports:
      - "5432:5432"
    volumes:
      - postgres-data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    container_name: ohgun-redis
    command: redis-server --appendonly yes --requirepass redis1234
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data

  api:
    image: ohgun0325/ohgun-api:latest
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    environment:
      SPRING_PROFILES_ACTIVE: local
      NEON_DB_HOST: postgres  # 로컬 컨테이너 이름
      UPSTASH_REDIS_HOST: redis  # 로컬 컨테이너 이름
```

### 특징

- ✅ 로컬에서 완전히 독립적으로 실행
- ✅ 인터넷 연결 불필요
- ❌ 데이터베이스 관리 필요
- ❌ 백업/복구 수동 처리
- ❌ 다른 서버에서 접근 불가

---

## 전환 후 구조 (클라우드 서비스)

### Docker Compose 구조

```yaml
services:
  api:
    image: ohgun0325/ohgun-api:latest
    container_name: ohgun-api
    ports:
      - "8080:8080"
    env_file:
      - ../.env
    environment:
      # Neon PostgreSQL Database Configuration
      NEON_DB_HOST: ${NEON_DB_HOST:-ep-calm-credit-alrnsip1-pooler.ap-southeast-1.aws.neon.tech}
      NEON_DB_NAME: ${NEON_DB_NAME:-neondb}
      NEON_DB_USER: ${NEON_DB_USER:-neondb_owner}
      NEON_DB_PASSWORD: ${NEON_DB_PASSWORD:-npg_kDZv9cRNij8A}
      
      # Upstash Redis Configuration
      UPSTASH_REDIS_HOST: ${UPSTASH_REDIS_HOST:-awaited-insect-5667.upstash.io}
      UPSTASH_REDIS_PORT: ${UPSTASH_REDIS_PORT:-6379}
      UPSTASH_REDIS_PASSWORD: ${UPSTASH_REDIS_PASSWORD:-ARYjAAImcDIyYTNkMDE3YjJlYjA0MDVjODRjYTE5NWRjZmRmMDZlNXAyNTY2Nw}
```

### 특징

- ✅ 데이터베이스 관리 불필요 (관리형 서비스)
- ✅ 자동 백업 및 복구
- ✅ 확장성 향상
- ✅ 다른 서버에서도 동일한 데이터 접근
- ❌ 인터넷 연결 필수
- ❌ 네트워크 지연 가능성
- ❌ 비용 발생 (무료 티어 제한)

---

## 구축 과정

### 1단계: Neon DB 설정 확인

#### Neon DB 정보 확인

1. [Neon Console](https://console.neon.tech) 접속
2. 프로젝트 선택
3. Connection Details에서 다음 정보 확인:
   - **Host**: `ep-calm-credit-alrnsip1-pooler.ap-southeast-1.aws.neon.tech`
   - **Database**: `neondb`
   - **User**: `neondb_owner`
   - **Password**: (Neon에서 제공한 비밀번호)

#### application.yaml 기본값 확인

```yaml:5:9:api.ohgun.site/src/main/resources/application.yaml
# Neon PostgreSQL Database Configuration
datasource:
  url: jdbc:postgresql://${NEON_DB_HOST:ep-calm-credit-alrnsip1-pooler.ap-southeast-1.aws.neon.tech}:5432/${NEON_DB_NAME:neondb}?sslmode=require
  username: ${NEON_DB_USER:neondb_owner}
  password: ${NEON_DB_PASSWORD:npg_kDZv9cRNij8A}
```

**중요**: `application.yaml`에 기본값이 설정되어 있어 환경 변수가 없어도 동작합니다.

### 2단계: Upstash Redis 설정 확인

#### Upstash Redis 정보 확인

1. [Upstash Console](https://console.upstash.com) 접속
2. Redis Database 선택
3. Details 탭에서 다음 정보 확인:
   - **REST API Endpoint**: `awaited-insect-5667.upstash.io`
   - **Port**: `6379`
   - **Password**: (Upstash에서 제공한 토큰)

#### application.yaml 설정 확인

```yaml:22:30:api.ohgun.site/src/main/resources/application.yaml
# Upstash Redis Configuration
data:
  redis:
    host: ${UPSTASH_REDIS_HOST}
    port: ${UPSTASH_REDIS_PORT}
    password: ${UPSTASH_REDIS_PASSWORD}
    ssl:
      enabled: true
    timeout: 2000ms
```

**중요**: Upstash Redis는 환경 변수가 필수입니다. 기본값이 없으므로 반드시 설정해야 합니다.

### 3단계: docker-compose.yaml 수정

#### 변경 사항

1. **postgres 서비스 제거**
2. **redis 서비스 제거**
3. **api 서비스만 유지**
4. **환경 변수 설정 추가**

#### 최종 docker-compose.yaml

```yaml:1:52:api.ohgun.site/docker-compose.yaml
services:
  # ========================================
  # Spring Boot Application
  # ========================================
  api:
    image: ${DOCKER_IMAGE_NAME:-ohgun0325/ohgun-api}:${DOCKER_TAG:-latest}
    build:
      context: .
      dockerfile: Dockerfile
    container_name: ohgun-api
    ports:
      - "${SERVER_PORT:-8080}:8080"
    env_file:
      - ../.env
    environment:
      # Spring Profile (기본값 사용, application.yaml의 기본 설정 적용)
      # SPRING_PROFILES_ACTIVE을 설정하지 않으면 application.yaml의 기본값 사용

      # Neon PostgreSQL Database Configuration
      # application.yaml의 기본값 사용:
      # - NEON_DB_HOST: ep-calm-credit-alrnsip1-pooler.ap-southeast-1.aws.neon.tech
      # - NEON_DB_NAME: neondb
      # - NEON_DB_USER: neondb_owner
      # - NEON_DB_PASSWORD: npg_kDZv9cRNij8A
      # 환경 변수로 오버라이드하려면 아래 주석을 해제하고 설정하세요:
      # NEON_DB_HOST: ${NEON_DB_HOST}
      # NEON_DB_NAME: ${NEON_DB_NAME}
      # NEON_DB_USER: ${NEON_DB_USER}
      # NEON_DB_PASSWORD: ${NEON_DB_PASSWORD}

      # Upstash Redis Configuration (필수 환경 변수)
      # .env 파일에서 읽어오거나, 아래 기본값 사용
      UPSTASH_REDIS_HOST: ${UPSTASH_REDIS_HOST:-awaited-insect-5667.upstash.io}
      UPSTASH_REDIS_PORT: ${UPSTASH_REDIS_PORT:-6379}
      UPSTASH_REDIS_PASSWORD: ${UPSTASH_REDIS_PASSWORD:-ARYjAAImcDIyYTNkMDE3YjJlYjA0MDVjODRjYTE5NWRjZmRmMDZlNXAyNTY2Nw}

      # JPA Configuration
      JPA_DDL_AUTO: ${JPA_DDL_AUTO:-validate}
      JPA_SHOW_SQL: ${JPA_SHOW_SQL:-false}

      # JWT Configuration
      JWT_SECRET: ${JWT_SECRET:-your-secret-key-change-in-production-min-256-bits}
      JWT_EXPIRATION: ${JWT_EXPIRATION:-86400}
      JWT_REFRESH_EXPIRATION: ${JWT_REFRESH_EXPIRATION:-2592000}

      # OAuth Naver Configuration
      NAVER_CLIENT_ID: ${NAVER_CLIENT_ID:-}
      NAVER_CLIENT_SECRET: ${NAVER_CLIENT_SECRET:-}
      NAVER_REDIRECT_URI: ${NAVER_REDIRECT_URI:-http://localhost:8080/oauth/naver/callback}
      OAUTH_FRONTEND_REDIRECT_URL: ${OAUTH_FRONTEND_REDIRECT_URL:-http://localhost:3000}
    restart: unless-stopped
```

### 4단계: Spring Profile 설정

#### application.yaml vs application-local.yaml

**application.yaml** (기본 설정 - 클라우드 서비스):
```yaml
spring:
  datasource:
    url: jdbc:postgresql://${NEON_DB_HOST:ep-calm-credit-alrnsip1-pooler.ap-southeast-1.aws.neon.tech}:5432/${NEON_DB_NAME:neondb}?sslmode=require
    username: ${NEON_DB_USER:neondb_owner}
    password: ${NEON_DB_PASSWORD:npg_kDZv9cRNij8A}
  
  data:
    redis:
      host: ${UPSTASH_REDIS_HOST}
      port: ${UPSTASH_REDIS_PORT}
      password: ${UPSTASH_REDIS_PASSWORD}
      ssl:
        enabled: true
```

**application-local.yaml** (로컬 개발용 - 사용 안 함):
```yaml
spring:
  datasource:
    url: jdbc:postgresql://${NEON_DB_HOST:localhost}:5432/${NEON_DB_NAME:ohgun}
    username: ${NEON_DB_USER:ohgun}
    password: ${NEON_DB_PASSWORD:ohgun1234}
  
  data:
    redis:
      host: ${UPSTASH_REDIS_HOST:localhost}
      port: ${UPSTASH_REDIS_PORT:6379}
      password: ${UPSTASH_REDIS_PASSWORD:redis1234}
      ssl:
        enabled: false
```

**현재 설정**: `SPRING_PROFILES_ACTIVE`를 설정하지 않으면 `application.yaml`의 기본값(클라우드 서비스)을 사용합니다.

---

## 환경 변수 설정

### 옵션 1: .env 파일 사용 (권장)

**위치**: 루트 디렉토리 `.env` 파일

```env
# Neon PostgreSQL Database
NEON_DB_HOST=ep-calm-credit-alrnsip1-pooler.ap-southeast-1.aws.neon.tech
NEON_DB_NAME=neondb
NEON_DB_USER=neondb_owner
NEON_DB_PASSWORD=npg_kDZv9cRNij8A

# Upstash Redis
UPSTASH_REDIS_HOST=awaited-insect-5667.upstash.io
UPSTASH_REDIS_PORT=6379
UPSTASH_REDIS_PASSWORD=ARYjAAImcDIyYTNkMDE3YjJlYjA0MDVjODRjYTE5NWRjZmRmMDZlNXAyNTY2Nw
```

**docker-compose.yaml에서 참조**:
```yaml
env_file:
  - ../.env
```

### 옵션 2: docker-compose.yaml에 기본값 설정

```yaml
environment:
  UPSTASH_REDIS_HOST: ${UPSTASH_REDIS_HOST:-awaited-insect-5667.upstash.io}
  UPSTASH_REDIS_PORT: ${UPSTASH_REDIS_PORT:-6379}
  UPSTASH_REDIS_PASSWORD: ${UPSTASH_REDIS_PASSWORD:-기본값}
```

### 환경 변수 우선순위

```
1순위: docker-compose.yaml의 environment 섹션
   ↓
2순위: .env 파일 (env_file)
   ↓
3순위: docker-compose.yaml의 ${변수명:-기본값}
   ↓
4순위: application.yaml의 기본값
```

---

## Docker Compose 설정

### 핵심 변경 사항

#### 제거된 항목
- ❌ `postgres` 서비스
- ❌ `redis` 서비스
- ❌ `depends_on` 의존성
- ❌ `networks` 섹션 (단일 컨테이너이므로 불필요)
- ❌ `volumes` 섹션 (로컬 데이터 저장 불필요)

#### 추가된 항목
- ✅ `env_file: - ../.env` (루트 .env 파일 참조)
- ✅ 클라우드 서비스 환경 변수 설정
- ✅ 기본값 제공 (즉시 실행 가능)

### 네트워크 구조 변화

**이전 (로컬 컨테이너)**:
```
┌─────────────────────────────────┐
│    Docker Network (로컬)        │
├─────────────────────────────────┤
│  postgres  →  api  ←  redis     │
│  컨테이너      컨테이너   컨테이너 │
└─────────────────────────────────┘
```

**현재 (클라우드 서비스)**:
```
┌──────────────────────┐
│   api 컨테이너만      │
│   (로컬 Docker)      │
└──────────────────────┘
        ↓         ↓
        ↓         ↓
  ┌─────┴───┐  ┌─┴──────────┐
  │ Neon DB │  │ Upstash    │
  │ (AWS)   │  │ Redis      │
  └─────────┘  └────────────┘
```

---

## 테스트 및 확인

### 1. 로컬 테스트

```powershell
# 1. 컨테이너 중지
cd api.ohgun.site
docker-compose down

# 2. Docker Hub에서 최신 이미지 pull
docker pull ohgun0325/ohgun-api:latest

# 3. 컨테이너 시작
docker-compose up -d

# 4. 로그 확인
docker-compose logs -f api
```

### 2. 연결 상태 확인

#### Neon DB 연결 확인

**로그에서 확인**:
```
HikariPool-1 - Start completed
Initialized JPA EntityManagerFactory
Database version: 17.7
```

**환경 변수 확인**:
```powershell
docker-compose exec api printenv | Select-String "NEON"
```

#### Upstash Redis 연결 확인

**로그에서 확인**:
```
Bootstrapping Spring Data Redis repositories
# Redis 연결 에러가 없어야 함
```

**환경 변수 확인**:
```powershell
docker-compose exec api printenv | Select-String "UPSTASH"
```

### 3. 애플리케이션 상태 확인

**성공 로그**:
```
Started MonolithicApplication in 8.37 seconds
Tomcat started on port 8080
```

**컨테이너 상태**:
```powershell
docker ps --filter "name=ohgun-api"
# STATUS: Up (정상 실행 중)
```

---

## Docker Hub 배포

### 1. 이미지 빌드 및 푸시

```powershell
# 로컬에서 빌드
cd api.ohgun.site
docker-compose build

# Docker Hub에 푸시
docker push ohgun0325/ohgun-api:latest
```

### 2. 다른 환경에서 Pull 테스트

```powershell
# 이미지 삭제
docker rmi ohgun0325/ohgun-api:latest

# Docker Hub에서 pull
docker pull ohgun0325/ohgun-api:latest

# 실행
docker-compose up -d
```

### 3. 이미지 확인

- **Docker Hub**: https://hub.docker.com/r/ohgun0325/ohgun-api
- **Tags**: `latest`, `{commit-sha}`

---

## GitHub Actions 연동

### 워크플로우 파일

**위치**: `api.ohgun.site/.github/workflows/ci-cd.yml`

```yaml:1:57:api.ohgun.site/.github/workflows/ci-cd.yml
name: CI/CD Pipeline - API

on:
  push:
    branches:
      - main
    paths:
      - "**"
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
          java-version: "21"
          distribution: "temurin"

      - name: Grant execute permission for gradlew
        run: chmod +x gradlew

      - name: Build with Gradle
        run: ./gradlew build --no-daemon -x test

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Build and push Docker image
        uses: docker/build-push-action@v5
        with:
          context: .
          file: ./Dockerfile
          push: true
          tags: |
            ${{ env.DOCKER_IMAGE_NAME }}:${{ env.DOCKER_TAG }}
            ${{ env.DOCKER_IMAGE_NAME }}:${{ github.sha }}
          cache-from: type=registry,ref=${{ env.DOCKER_IMAGE_NAME }}:buildcache
          cache-to: type=registry,ref=${{ env.DOCKER_IMAGE_NAME }}:buildcache,mode=max
```

### GitHub Secrets 설정

**필요한 Secrets**:
- `DOCKERHUB_USERNAME`: Docker Hub 사용자명
- `DOCKERHUB_TOKEN`: Docker Hub Personal Access Token

**설정 위치**: GitHub 저장소 → Settings → Secrets and variables → Actions

### 자동화 흐름

```
코드 수정 → git push origin main
    ↓
GitHub Actions 자동 실행
    ↓
Gradle 빌드
    ↓
Docker 이미지 빌드
    ↓
Docker Hub에 푸시
    ↓
다른 환경에서 pull 가능
```

---

## 문제 해결

### 1. Neon DB 연결 실패

**증상**:
```
Failed to obtain JDBC Connection
```

**해결 방법**:
1. Neon DB 호스트 주소 확인
2. SSL 모드 확인 (`sslmode=require`)
3. 비밀번호 확인
4. 네트워크 연결 확인 (인터넷 연결 필수)

### 2. Upstash Redis 연결 실패

**증상**:
```
Redis health check failed
Unable to connect to Redis
WRONGPASS invalid username-password pair
```

**해결 방법**:
1. Upstash Redis 비밀번호 확인 (URL에서 추출 가능)
2. 환경 변수 설정 확인
3. SSL 설정 확인 (`ssl.enabled: true`)

**비밀번호 확인**:
```powershell
# UPSTASH_REDIS_URL에서 비밀번호 추출
# rediss://default:PASSWORD@host:port
```

### 3. 인코딩 오류

**증상**:
```
error: unmappable character for encoding UTF-8
```

**해결 방법**:
1. `build.gradle`에 인코딩 설정 확인:
```gradle
tasks.withType(JavaCompile) {
    options.encoding = 'UTF-8'
}
```

2. `Dockerfile`에 인코딩 설정 확인:
```dockerfile
ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8
ENV JAVA_TOOL_OPTIONS=-Dfile.encoding=UTF-8
```

### 4. 환경 변수 미설정

**증상**:
```
The "UPSTASH_REDIS_HOST" variable is not set. Defaulting to a blank string.
```

**해결 방법**:
1. `.env` 파일 확인
2. `docker-compose.yaml`의 기본값 확인
3. 환경 변수 우선순위 확인

---

## 요약

### 전환 전후 비교

| 항목 | 로컬 컨테이너 | 클라우드 서비스 |
|------|--------------|----------------|
| **PostgreSQL** | Docker 컨테이너 | Neon DB (AWS) |
| **Redis** | Docker 컨테이너 | Upstash Redis |
| **관리** | 수동 관리 필요 | 자동 관리 |
| **백업** | 수동 처리 | 자동 백업 |
| **접근성** | 로컬만 가능 | 어디서나 접근 |
| **인터넷** | 불필요 | 필수 |
| **비용** | 무료 | 무료 티어 |

### 핵심 포인트

1. ✅ **Neon DB**: `application.yaml`에 기본값이 있어 환경 변수 선택적
2. ✅ **Upstash Redis**: 환경 변수 필수 (기본값 없음)
3. ✅ **docker-compose.yaml**: 단일 컨테이너 구조로 단순화
4. ✅ **환경 변수**: `.env` 파일 또는 기본값으로 관리
5. ✅ **GitHub Actions**: 자동 빌드 및 Docker Hub 푸시

### 다음 단계

- [ ] EC2 서버 설정
- [ ] EC2에 docker-compose.yaml 배포
- [ ] GitHub Actions에 EC2 배포 단계 추가
- [ ] 프로덕션 환경 테스트

---

## 참고 자료

- [Neon DB 공식 문서](https://neon.tech/docs)
- [Upstash Redis 공식 문서](https://docs.upstash.com/redis)
- [Docker Compose 환경 변수](https://docs.docker.com/compose/environment-variables/)
- [Spring Boot 외부 설정](https://docs.spring.io/spring-boot/docs/current/reference/html/features.html#features.external-config)

---

**작성일**: 2026-01-02  
**프로젝트**: api.ohgun.site  
**버전**: 1.0.0

