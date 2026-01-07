# GitHub Actions 자동 배포 완성 가이드

GitHub Actions를 통해 코드 푸시만으로 EC2에 자동 배포하는 전체 과정을 정리한 문서입니다.

## 📋 목차

1. [개요](#개요)
2. [자동 배포 아키텍처](#자동-배포-아키텍처)
3. [GitHub Actions 워크플로우 설정](#github-actions-워크플로우-설정)
4. [GitHub Secrets 설정](#github-secrets-설정)
5. [자동 배포 프로세스](#자동-배포-프로세스)
6. [배포 확인 및 문제 해결](#배포-확인-및-문제-해결)
7. [자주 묻는 질문](#자주-묻는-질문)
8. [전체 흐름 요약](#전체-흐름-요약)

---

## 개요

### 목표

**코드 푸시만으로 자동 배포**

- 로컬 Docker Desktop 실행 불필요
- 수동 배포 작업 불필요
- `git push`만으로 EC2에 자동 배포

### 완성된 자동 배포 파이프라인

```
코드 수정 (로컬)
    ↓
git push origin main
    ↓
GitHub Actions 자동 실행
    ↓
Docker 이미지 빌드 및 Docker Hub 푸시
    ↓
EC2에 SSH 접속
    ↓
최신 이미지 pull 및 컨테이너 재시작
    ↓
애플리케이션 자동 업데이트 완료 ✅
```

---

## 자동 배포 아키텍처

### 전체 구조

```
┌─────────────────┐
│  로컬 개발 환경   │
│  (코드 수정)     │
└────────┬────────┘
         │ git push
         ↓
┌─────────────────┐
│  GitHub 저장소   │
│  (ohgun-api)    │
└────────┬────────┘
         │ 트리거
         ↓
┌─────────────────┐
│ GitHub Actions  │
│  (CI/CD 서버)   │
│                 │
│ 1. Gradle 빌드  │
│ 2. Docker 빌드  │
│ 3. Docker Hub 푸시│
│ 4. EC2 배포     │
└────────┬────────┘
         │
         ├──────────────┐
         ↓              ↓
┌─────────────┐  ┌─────────────┐
│ Docker Hub  │  │  AWS EC2     │
│ (이미지 저장)│  │ (프로덕션 서버)│
└─────────────┘  └──────┬───────┘
                        │
                        ↓
              ┌─────────────────┐
              │  컨테이너 실행    │
              │  (ohgun-api)     │
              └────────┬────────┘
                        │
         ┌──────────────┼──────────────┐
         ↓              ↓              ↓
    ┌─────────┐  ┌─────────┐  ┌─────────┐
    │ Neon DB │  │ Upstash │  │ 외부 접속│
    │(PostgreSQL)│ │ (Redis) │  │  (8080) │
    └─────────┘  └─────────┘  └─────────┘
```

### 주요 컴포넌트

1. **GitHub Actions**: 자동화된 CI/CD 파이프라인
2. **Docker Hub**: Docker 이미지 저장소
3. **AWS EC2**: 프로덕션 서버
4. **Neon DB**: 클라우드 PostgreSQL 데이터베이스
5. **Upstash Redis**: 클라우드 Redis 캐시

---

## GitHub Actions 워크플로우 설정

### 워크플로우 파일 위치

```
api.ohgun.site/.github/workflows/ci-cd.yml
```

### 워크플로우 구조

#### 1. 트리거 설정

```yaml
on:
  push:
    branches:
      - main
    paths:
      - "**"
  pull_request:
    branches:
      - main
  workflow_dispatch:  # 수동 실행 가능
```

- **자동 실행**: `main` 브랜치에 push 시
- **수동 실행**: GitHub Actions UI에서 "Run workflow" 버튼 클릭

#### 2. Job 1: build-and-push

```yaml
build-and-push:
  runs-on: ubuntu-latest
  
  steps:
    - Checkout code
    - Set up JDK 21
    - Build with Gradle
    - Build and push Docker image to Docker Hub
```

**기능**:
- Spring Boot 애플리케이션 빌드
- Docker 이미지 생성
- Docker Hub에 푸시 (`ohgun0325/ohgun-api:latest`)

#### 3. Job 2: deploy

```yaml
deploy:
  needs: build-and-push
  runs-on: ubuntu-latest
  if: github.ref == 'refs/heads/main' && github.event_name == 'push'
  
  steps:
    - Deploy to EC2
```

**기능**:
- `build-and-push` 성공 후 실행
- `main` 브랜치 push 시에만 실행
- EC2에 SSH 접속하여 자동 배포

### 배포 스크립트 상세

```yaml
script: |
  # 1. 작업 디렉토리 생성
  sudo mkdir -p /opt/ohgun-api
  sudo chown $USER:$USER /opt/ohgun-api
  cd /opt/ohgun-api
  
  # 2. .env 파일 생성/업데이트
  if [ -n "${{ secrets.EC2_ENV_FILE }}" ]; then
    echo "${{ secrets.EC2_ENV_FILE }}" > .env
    chmod 600 .env
  fi
  
  # 3. 기존 컨테이너 중지 및 제거
  docker stop ohgun-api || true
  docker rm ohgun-api || true
  
  # 4. 최신 이미지 pull
  docker pull ohgun0325/ohgun-api:latest
  
  # 5. 새 컨테이너 실행
  docker run -d \
    --name ohgun-api \
    -p 8080:8080 \
    --env-file .env \
    --restart unless-stopped \
    ohgun0325/ohgun-api:latest
  
  # 6. 불필요한 이미지 정리
  docker image prune -f
  
  # 7. 컨테이너 상태 및 로그 확인
  docker ps -a | grep ohgun-api
  docker logs --tail 20 ohgun-api
```

---

## GitHub Secrets 설정

### 필요한 Secrets

GitHub 저장소 → Settings → Secrets and variables → Actions에서 다음 Secrets를 설정해야 합니다:

#### 1. Docker Hub 인증

- **`DOCKERHUB_USERNAME`**: Docker Hub 사용자명
- **`DOCKERHUB_TOKEN`**: Docker Hub Personal Access Token

#### 2. EC2 접속 정보

- **`EC2_HOST`**: EC2 Public IP 또는 도메인
  - 예: `3.35.26.129`
  - 참고: Public IP는 재시작 시 변경될 수 있으므로 Elastic IP 사용 권장

- **`EC2_USERNAME`**: EC2 사용자명
  - Ubuntu: `ubuntu`
  - Amazon Linux: `ec2-user`

- **`EC2_SSH_KEY`**: EC2 SSH Private Key
  - `-----BEGIN RSA PRIVATE KEY-----`부터 `-----END RSA PRIVATE KEY-----`까지 전체 복사

#### 3. 환경 변수 파일

- **`EC2_ENV_FILE`**: `.env` 파일 전체 내용
  - Neon DB 설정
  - Upstash Redis 설정
  - JWT 설정
  - OAuth 설정
  - JPA 설정

### .env 파일 예시

```env
# Neon PostgreSQL Database Configuration
NEON_DB_HOST=ep-calm-credit-a1rnsip1-pooler.ap-southeast-1.aws.neon.tech
NEON_DB_NAME=neondb
NEON_DB_USER=neondb_owner
NEON_DB_PASSWORD=npg_kDZv9cRNij8A

# Upstash Redis Configuration
UPSTASH_REDIS_HOST=awaited-insect-5667.upstash.io
UPSTASH_REDIS_PORT=6379
UPSTASH_REDIS_PASSWORD=ARYjAAImcDIyYTNkMDE3YjJlYjA0MDVjODRjYTE5NWRjZmRmMDZlNXAyNTY2Nw

# JWT Configuration
JWT_SECRET=your-secret-key-change-in-production-min-256-bits
JWT_EXPIRATION=86400
JWT_REFRESH_EXPIRATION=2592000

# JPA Configuration
JPA_DDL_AUTO=validate
JPA_SHOW_SQL=false

# OAuth Naver Configuration
NAVER_CLIENT_ID=your-naver-client-id
NAVER_CLIENT_SECRET=your-naver-client-secret
NAVER_REDIRECT_URI=http://localhost:8080/oauth/naver/callback
OAUTH_FRONTEND_REDIRECT_URL=http://localhost:3000
```

### Secrets 설정 방법

1. GitHub 저장소 → **Settings**
2. 왼쪽 메뉴 → **Secrets and variables** → **Actions**
3. **New repository secret** 클릭
4. Name과 Value 입력 후 **Add secret** 클릭

---

## 자동 배포 프로세스

### 1. 코드 수정 및 푸시

```bash
# 로컬에서 코드 수정
cd api.ohgun.site
vim src/main/java/...

# 변경사항 커밋 및 푸시
git add .
git commit -m "기능 추가"
git push origin main
```

### 2. GitHub Actions 자동 실행

1. GitHub 저장소 → **Actions** 탭
2. "CI/CD Pipeline - API" 워크플로우 확인
3. 실행 상태 모니터링:
   - ✅ 초록색: 성공
   - ❌ 빨간색: 실패
   - 🟡 노란색: 진행 중

### 3. 배포 단계별 확인

#### Step 1: build-and-push
- ✅ 코드 체크아웃
- ✅ JDK 21 설정
- ✅ Gradle 빌드
- ✅ Docker 이미지 빌드
- ✅ Docker Hub 푸시

#### Step 2: deploy
- ✅ EC2 SSH 접속
- ✅ 디렉토리 생성
- ✅ .env 파일 생성/업데이트
- ✅ 컨테이너 중지 및 제거
- ✅ 최신 이미지 pull
- ✅ 새 컨테이너 실행
- ✅ 상태 확인

### 4. 배포 완료 확인

배포가 성공하면 GitHub Actions 로그에 다음이 표시됩니다:

```
=== 컨테이너 상태 ===
CONTAINER ID   IMAGE                          STATUS    PORTS
abc123def456   ohgun0325/ohgun-api:latest     Up        0.0.0.0:8080->8080/tcp

=== 최근 로그 ===
Started MonolithicApplication in 9.297 seconds
Tomcat started on port 8080
```

---

## 배포 확인 및 문제 해결

### EC2에서 배포 상태 확인

#### 1. SSH 접속

```bash
# AWS Console → EC2 → Connect → EC2 Instance Connect 사용
# 또는 SSH 키 파일로 접속
ssh -i your-key.pem ubuntu@3.35.26.129
```

#### 2. 컨테이너 상태 확인

```bash
# 실행 중인 컨테이너 확인
docker ps | grep ohgun-api

# 모든 컨테이너 확인
docker ps -a | grep ohgun-api
```

#### 3. 컨테이너 로그 확인

```bash
# 최근 로그 확인
docker logs ohgun-api --tail 50

# 실시간 로그 보기
docker logs -f ohgun-api

# 에러만 확인
docker logs ohgun-api 2>&1 | grep -i error
```

#### 4. 헬스 체크

```bash
# 로컬에서 헬스 체크
curl http://localhost:8080/actuator/health

# 또는 상세 정보
curl http://localhost:8080/actuator/health | jq
```

**예상 출력**:
```json
{
  "status": "UP",
  "components": {
    "db": {
      "status": "UP",
      "details": {
        "database": "PostgreSQL",
        "validationQuery": "isValid()"
      }
    },
    "redis": {
      "status": "UP"
    }
  }
}
```

#### 5. .env 파일 확인

```bash
cd /opt/ohgun-api
cat .env | sed 's/PASSWORD=.*/PASSWORD=***/g'
```

### 일반적인 문제 해결

#### 문제 1: 배포 실패 - 디렉토리 없음

**증상**:
```
cd: /opt/ohgun-api: No such file or directory
```

**해결**: 워크플로우에서 자동 생성하도록 설정됨 (이미 해결됨)

#### 문제 2: 배포 실패 - .env 파일 없음

**증상**:
```
docker: open .env: no such file or directory
```

**해결**:
1. GitHub Secret `EC2_ENV_FILE` 확인
2. 또는 EC2에 SSH 접속하여 수동으로 `.env` 파일 생성

#### 문제 3: 애플리케이션 시작 실패 - 환경 변수 누락

**증상**:
```
UnsatisfiedDependencyException: Error creating bean 'naverService'
```

**해결**: `.env` 파일에 OAuth 설정 추가:
```env
NAVER_CLIENT_ID=your-client-id
NAVER_CLIENT_SECRET=your-client-secret
NAVER_REDIRECT_URI=http://localhost:8080/oauth/naver/callback
```

#### 문제 4: 데이터베이스 연결 실패

**증상**:
```
CannotGetJdbcConnectionException: Failed to obtain JDBC Connection
```

**해결**:
1. `.env` 파일의 `NEON_DB_HOST` 확인
2. Neon DB 비밀번호 확인
3. 네트워크 연결 확인: `nc -zv NEON_DB_HOST 5432`

#### 문제 5: Redis 연결 실패

**증상**:
```
Redis connection failed
```

**해결**:
1. `.env` 파일의 `UPSTASH_REDIS_HOST`, `UPSTASH_REDIS_PASSWORD` 확인
2. SSL 설정 확인 (`ssl.enabled: true`)

### 빠른 진단 스크립트

EC2에 SSH 접속 후 다음 스크립트 실행:

```bash
#!/bin/bash
echo "=== 컨테이너 상태 ==="
docker ps -a | grep ohgun-api

echo ""
echo "=== .env 파일 확인 ==="
if [ -f /opt/ohgun-api/.env ]; then
    echo "✓ .env 파일 존재"
    echo "환경 변수 목록:"
    cat /opt/ohgun-api/.env | sed 's/PASSWORD=.*/PASSWORD=***/g'
else
    echo "✗ .env 파일이 없습니다!"
fi

echo ""
echo "=== 최근 로그 (50줄) ==="
docker logs ohgun-api --tail 50

echo ""
echo "=== 헬스 체크 ==="
curl -s http://localhost:8080/actuator/health | jq . || curl -s http://localhost:8080/actuator/health

echo ""
echo "=== 에러 로그 ==="
docker logs ohgun-api 2>&1 | grep -i error | tail -10
```

---

## 자주 묻는 질문

### Q1: 로컬 Docker Desktop을 실행해야 하나요?

**A**: 아니요. 프로덕션 배포에는 필요 없습니다.

- **자동 배포**: GitHub Actions가 클라우드에서 빌드하고 EC2에 배포
- **로컬 테스트**: 로컬에서 테스트하고 싶을 때만 Docker Desktop 사용

### Q2: 배포는 언제 자동으로 실행되나요?

**A**: `main` 브랜치에 `git push`할 때마다 자동 실행됩니다.

### Q3: 수동으로 배포를 실행할 수 있나요?

**A**: 네, 가능합니다.

1. GitHub 저장소 → **Actions** 탭
2. "CI/CD Pipeline - API" 워크플로우 선택
3. 오른쪽 상단 **"Run workflow"** 버튼 클릭
4. 브랜치 선택 후 **"Run workflow"** 클릭

### Q4: 배포 중에 서비스가 중단되나요?

**A**: 짧은 시간 동안 중단됩니다.

- 기존 컨테이너 중지 → 새 컨테이너 시작
- 일반적으로 10-30초 정도 소요
- Zero-downtime 배포가 필요하면 Blue-Green 배포 전략 고려

### Q5: 배포 실패 시 어떻게 되나요?

**A**: 기존 컨테이너는 그대로 유지됩니다.

- 배포 실패 시 기존 컨테이너는 계속 실행
- GitHub Actions 로그에서 실패 원인 확인
- 문제 해결 후 다시 배포

### Q6: 여러 환경(dev, staging, prod)에 배포할 수 있나요?

**A**: 네, 가능합니다.

- 워크플로우에 환경별 job 추가
- GitHub Environments 사용
- 브랜치별로 다른 EC2 인스턴스에 배포

### Q7: 배포 속도를 높일 수 있나요?

**A**: 다음 방법을 고려할 수 있습니다:

1. **Docker 레이어 캐싱**: 이미 설정됨
2. **병렬 실행**: 여러 job을 병렬로 실행
3. **조건부 실행**: 변경된 파일만 빌드

### Q8: EC2 Public IP가 변경되면 어떻게 하나요?

**A**: GitHub Secret `EC2_HOST`를 업데이트하세요.

- Elastic IP 사용 권장 (IP 고정)
- 또는 도메인 사용 (Route 53 등)

---

## 전체 흐름 요약

### 개발자 관점

```bash
# 1. 코드 수정
vim src/main/java/...

# 2. 커밋 및 푸시
git add .
git commit -m "기능 추가"
git push origin main

# 3. 끝! (자동 배포됨)
```

### 시스템 관점

```
1. GitHub 저장소에 코드 푸시
   ↓
2. GitHub Actions 워크플로우 트리거
   ↓
3. build-and-push job 실행
   - Gradle 빌드
   - Docker 이미지 빌드
   - Docker Hub 푸시
   ↓
4. deploy job 실행 (build-and-push 성공 후)
   - EC2에 SSH 접속
   - 디렉토리 및 .env 파일 생성
   - 기존 컨테이너 중지 및 제거
   - 최신 이미지 pull
   - 새 컨테이너 실행
   - 상태 확인
   ↓
5. 배포 완료 ✅
```

### 시간 소요

- **빌드 및 푸시**: 약 2-3분
- **배포**: 약 1-2분
- **총 소요 시간**: 약 3-5분

---

## 완성된 기능 체크리스트

- [x] GitHub Actions CI/CD 파이프라인 설정
- [x] Docker Hub 자동 푸시
- [x] EC2 자동 배포
- [x] .env 파일 자동 생성
- [x] 수동 실행 가능 (workflow_dispatch)
- [x] 배포 상태 확인
- [x] 에러 로그 확인
- [x] 헬스 체크 확인

---

## 다음 단계 (선택사항)

### 1. 알림 설정

- Slack 알림 추가
- 이메일 알림 설정
- 배포 성공/실패 알림

### 2. 배포 전략 개선

- Blue-Green 배포
- Canary 배포
- 롤백 자동화

### 3. 모니터링 강화

- CloudWatch 연동
- 로그 집계 (CloudWatch Logs)
- 메트릭 수집

### 4. 보안 강화

- Secrets 관리 개선 (AWS Secrets Manager)
- SSH 키 로테이션
- 네트워크 보안 강화

---

## 참고 문서

- [EC2 배포 가이드](./EC2_DEPLOYMENT_GUIDE.md)
- [클라우드 서비스 마이그레이션 가이드](./CLOUD_SERVICE_MIGRATION_GUIDE.md)
- [Docker Hub 로그인 가이드](./DOCKER_HUB_LOGIN_GUIDE.md)
- [GitHub Secrets 설정 가이드](./GITHUB_SECRETS_SETUP_GUIDE.md)

---

## 결론

이제 **코드 푸시만으로 자동 배포**가 완성되었습니다!

- ✅ 로컬 Docker Desktop 불필요
- ✅ 수동 배포 작업 불필요
- ✅ `git push`만으로 자동 배포
- ✅ 일관된 배포 환경
- ✅ 빠른 배포 속도

**행복한 배포 되세요! 🚀**

