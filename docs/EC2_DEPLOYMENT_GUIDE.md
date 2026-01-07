# EC2 배포 가이드 (Docker Hub + 클라우드 서비스)

Docker Hub에서 이미지를 pull하여 EC2에 배포하고, Neon DB와 Upstash Redis 클라우드 서비스에 연결하는 전체 과정을 정리한 문서입니다.

## 📋 목차

1. [개요](#개요)
2. [사전 준비 사항](#사전-준비-사항)
3. [Docker Hub 연결](#docker-hub-연결)
4. [EC2 서버 설정](#ec2-서버-설정)
5. [클라우드 서비스 연결](#클라우드-서비스-연결)
6. [EC2 배포 과정](#ec2-배포-과정)
7. [테스트 및 확인](#테스트-및-확인)
8. [문제 해결](#문제-해결)
9. [전체 흐름 요약](#전체-흐름-요약)

---

## 개요

### 목표

1. **Docker Hub에서 이미지 pull**
2. **EC2 서버에 Docker 및 Docker Compose 설치**
3. **클라우드 서비스(Neon DB, Upstash Redis) 연결**
4. **EC2에서 애플리케이션 실행 및 외부 접속 확인**

### 전체 아키텍처

```
로컬 개발 환경
    ↓ (코드 수정)
GitHub 저장소
    ↓ (git push)
GitHub Actions
    ↓ (자동 빌드)
Docker Hub
    ↓ (docker pull)
EC2 서버
    ↓ (환경 변수 설정)
클라우드 서비스
    ├─ Neon DB (PostgreSQL)
    └─ Upstash Redis
```

---

## 사전 준비 사항

### 1. Docker Hub 계정 및 이미지

- **Docker Hub 계정**: `ohgun0325`
- **이미지 이름**: `ohgun0325/ohgun-api:latest`
- **이미지 상태**: GitHub Actions를 통해 자동 빌드 및 푸시 완료

### 2. EC2 인스턴스

- **인스턴스 이름**: `ohgunapi`
- **인스턴스 ID**: `i-04725bfdaf515a9ee`
- **Public IP**: `3.35.26.129 -> 로그인 할 때 마다 바뀜`
- **인스턴스 타입**: `t3.small`
- **OS**: Ubuntu (Amazon Linux 2도 가능)
- **가용 영역**: `ap-northeast-2c` (서울)

### 3. 클라우드 서비스 정보

#### Neon DB (PostgreSQL)

- **호스트**: `ep-calm-credit-a1rnsip1-pooler.ap-southeast-1.aws.neon.tech`
- **데이터베이스**: `neondb`
- **사용자**: `neondb_owner`
- **비밀번호**: `npg_kDZv9cRNij8A`
- **포트**: `5432`
- **SSL**: 필수 (`sslmode=require`)

#### Upstash Redis

- **호스트**: `awaited-insect-5667.upstash.io`
- **포트**: `6379`
- **비밀번호**: `ARYjAAImcDIyYTNkMDE3YjJlYjA0MDVjODRjYTE5NWRjZmRmMDZlNXAyNTY2Nw`
- **SSL**: 필수 (`ssl.enabled: true`)

### 4. GitHub Secrets (이미 설정됨)

- `DOCKERHUB_USERNAME`: Docker Hub 사용자명
- `DOCKERHUB_TOKEN`: Docker Hub Personal Access Token
- `EC2_HOST`: EC2 Public IP 또는 도메인
- `EC2_USERNAME`: EC2 사용자명 (예: `ubuntu`, `ec2-user`)
- `EC2_SSH_KEY`: EC2 SSH 개인키

---

## Docker Hub 연결

### 1. Docker Hub 이미지 확인

**이미지 정보**:

- **저장소**: `ohgun0325/ohgun-api`
- **태그**: `latest`
- **상태**: GitHub Actions를 통해 자동 빌드 및 푸시 완료

**확인 방법**:

1. [Docker Hub](https://hub.docker.com/r/ohgun0325/ohgun-api) 접속
2. Tags 탭에서 `latest` 태그 확인
3. 최근 업데이트 시간 확인

### 2. GitHub Actions 자동화

**워크플로우 파일**: `api.ohgun.site/.github/workflows/ci-cd.yml`

**자동화 흐름**:

```
코드 수정 → git push origin main
    ↓
GitHub Actions 자동 실행
    ↓
Gradle 빌드 (Spring Boot)
    ↓
Docker 이미지 빌드
    ↓
Docker Hub에 푸시 (ohgun0325/ohgun-api:latest)
```

**실행 조건**:

- `main` 브랜치에 push
- 코드 변경 감지

**결과 확인**:

- GitHub Actions 페이지에서 실행 상태 확인
- Docker Hub에서 이미지 업데이트 확인

---

## EC2 서버 설정

### 1단계: EC2 인스턴스 접속

#### AWS 콘솔에서 접속

1. AWS 콘솔 → EC2 → Instances
2. `ohgunapi` 인스턴스 선택
3. "Connect" 버튼 클릭
4. SSH 클라이언트 또는 EC2 Instance Connect 사용

#### SSH로 접속 (로컬에서)

```bash
ssh -i your-key.pem ubuntu@3.35.26.129
```

### 2단계: Docker 설치

#### Ubuntu 환경

```bash
# 1. 시스템 업데이트
sudo apt update && sudo apt upgrade -y

# 2. Docker 설치 (공식 스크립트 사용)
curl -fsSL https://get.docker.com | sudo sh

# 3. Docker 서비스 시작 및 자동 시작 설정
sudo systemctl start docker
sudo systemctl enable docker

# 4. 현재 사용자를 docker 그룹에 추가
sudo usermod -aG docker $USER

# 5. 그룹 권한 적용 (재로그인 또는 newgrp 사용)
newgrp docker

# 6. Docker 버전 확인
docker --version
```

**예상 출력**:

```
Docker version 29.1.3, build f52814d
```

### 3단계: Docker Compose 설치

```bash
# 최신 버전의 docker-compose 설치
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# 실행 권한 부여
sudo chmod +x /usr/local/bin/docker-compose

# 버전 확인
docker-compose --version
```

**예상 출력**:

```
Docker Compose version v2.x.x
```

### 4단계: 작업 디렉토리 생성

```bash
# 작업 디렉토리 생성
sudo mkdir -p /opt/ohgun-api
sudo chown $USER:$USER /opt/ohgun-api
cd /opt/ohgun-api
```

---

## 클라우드 서비스 연결

### 1. Neon DB 연결 설정

#### 연결 정보 확인

Neon Console에서 확인:

- **호스트**: `ep-calm-credit-a1rnsip1-pooler.ap-southeast-1.aws.neon.tech`
- **데이터베이스**: `neondb`
- **사용자**: `neondb_owner`
- **비밀번호**: `npg_kDZv9cRNij8A`

#### 네트워크 연결 테스트

```bash
# Neon DB 호스트에 연결 테스트
telnet ep-calm-credit-a1rnsip1-pooler.ap-southeast-1.aws.neon.tech 5432

# 또는 nc (netcat) 사용
nc -zv ep-calm-credit-a1rnsip1-pooler.ap-southeast-1.aws.neon.tech 5432
```

**성공 시**:

```
Connected to ep-calm-credit-a1rnsip1-pooler.ap-southeast-1.aws.neon.tech
```

### 2. Upstash Redis 연결 설정

#### 연결 정보 확인

Upstash Console에서 확인:

- **호스트**: `awaited-insect-5667.upstash.io`
- **포트**: `6379`
- **비밀번호**: `ARYjAAImcDIyYTNkMDE3YjJlYjA0MDVjODRjYTE5NWRjZmRmMDZlNXAyNTY2Nw`

#### 중요 사항

- **SSL 필수**: `ssl.enabled: true`
- **비밀번호**: Upstash Redis URL에서 추출 가능
- **환경 변수 필수**: `application.yaml`에 기본값이 없으므로 반드시 설정 필요

---

## EC2 배포 과정

### 1단계: .env 파일 생성

EC2에서 `.env` 파일 생성:

```bash
cd /opt/ohgun-api
vim .env
```

**.env 파일 내용**:

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
```

**Vim 사용법**:

- `i`: 편집 모드 시작
- 내용 입력
- `Esc`: 일반 모드로 돌아가기
- `:wq`: 저장하고 나가기
- `:q!`: 저장하지 않고 나가기

### 2단계: Docker 이미지 Pull

```bash
# Docker Hub에서 이미지 pull
docker pull ohgun0325/ohgun-api:latest
```

**예상 출력**:

```
latest: Pulling from ohgun0325/ohgun-api
...
Status: Downloaded newer image for ohgun0325/ohgun-api:latest
docker.io/ohgun0325/ohgun-api:latest
```

### 3단계: 컨테이너 실행

#### 방법 1: docker run 명령어 사용 (권장)

```bash
docker run -d \
  --name ohgun-api \
  -p 8080:8080 \
  --env-file .env \
  --restart unless-stopped \
  ohgun0325/ohgun-api:latest
```

#### 방법 2: docker-compose.yaml 사용

**docker-compose.yaml 파일 생성**:

```bash
cat > docker-compose.yaml << 'EOF'
services:
  api:
    image: ohgun0325/ohgun-api:latest
    container_name: ohgun-api
    ports:
      - "8080:8080"
    env_file:
      - .env
    restart: unless-stopped
EOF
```

**실행**:

```bash
docker-compose up -d
```

### 4단계: 로그 확인

```bash
# 실시간 로그 확인
docker logs -f ohgun-api

# 최근 50줄 확인
docker logs ohgun-api --tail 50

# 특정 키워드 필터링
docker logs ohgun-api 2>&1 | grep -i "started\|error\|exception"
```

**정상 시작 시 예상 로그**:

```
Started MonolithicApplication in X.XX seconds
Tomcat started on port 8080
HikariPool-1 - Start completed
Initialized JPA EntityManagerFactory
```

---

## 테스트 및 확인

### 1. EC2 내부에서 테스트

```bash
# 헬스 체크
curl http://localhost:8080/actuator/health

# 예상 응답
{
  "status": "UP",
  "components": {
    "db": {
      "status": "UP",
      "details": {
        "database": "PostgreSQL"
      }
    },
    "redis": {
      "status": "UP",
      "details": {
        "version": "8.2.0"
      }
    }
  }
}
```

### 2. 로컬에서 EC2 접속 테스트

#### Security Group 설정

1. AWS 콘솔 → EC2 → Security Groups
2. 인스턴스에 연결된 Security Group 선택
3. Inbound rules → Edit inbound rules
4. Rule 추가:
   - **Type**: Custom TCP
   - **Port**: 8080
   - **Source**: 0.0.0.0/0 (또는 특정 IP)

#### PowerShell에서 테스트

```powershell
# 방법 1: Invoke-WebRequest (권장)
$response = Invoke-WebRequest -Uri http://3.35.26.129:8080/actuator/health -UseBasicParsing
$response.Content.ToString()

# 방법 2: JSON으로 파싱하여 보기 좋게
$response.Content | ConvertFrom-Json | ConvertTo-Json -Depth 10

# 방법 3: 간단하게
(Invoke-WebRequest -Uri http://3.35.26.129:8080/actuator/health -UseBasicParsing).Content.ToString()
```

**성공 시**:

- StatusCode: 200
- JSON 응답: `{"status":"UP",...}`

### 3. 연결 상태 확인

#### 데이터베이스 연결 확인

```bash
# 컨테이너 로그에서 데이터베이스 연결 확인
docker logs ohgun-api 2>&1 | grep -i "hikari\|postgres\|database"

# 환경 변수 확인
docker exec ohgun-api printenv | grep NEON
```

**정상 연결 시**:

```
HikariPool-1 - Start completed
Initialized JPA EntityManagerFactory
Database version: 17.7 (또는 12.0)
```

#### Redis 연결 확인

```bash
# Redis 관련 로그 확인
docker logs ohgun-api 2>&1 | grep -i "redis"

# 환경 변수 확인
docker exec ohgun-api printenv | grep UPSTASH
```

**정상 연결 시**:

```
Bootstrapping Spring Data Redis repositories
# Redis 연결 오류 없음
```

### 4. 컨테이너 상태 확인

```bash
# 실행 중인 컨테이너 확인
docker ps | grep ohgun-api

# 상세 정보 확인
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

**정상 상태**:

```
NAMES       STATUS              PORTS
ohgun-api   Up X minutes        0.0.0.0:8080->8080/tcp
```

---

## 문제 해결

### 1. Docker 설치 문제

#### 문제: `docker: command not found`

**해결**:

```bash
# Docker 재설치
curl -fsSL https://get.docker.com | sudo sh
sudo systemctl start docker
newgrp docker
```

#### 문제: `permission denied` 오류

**해결**:

```bash
# 사용자를 docker 그룹에 추가
sudo usermod -aG docker $USER
newgrp docker

# 또는 SSH 재접속
exit
# 다시 SSH 접속
```

### 2. Docker 이미지 Pull 실패

#### 문제: `unauthorized: authentication required`

**해결**:

```bash
# Docker Hub 로그인 (필요한 경우)
docker login -u ohgun0325
# Personal Access Token 입력
```

#### 문제: `pull access denied`

**해결**:

- 이미지가 공개(Public)인지 확인
- Docker Hub에서 이미지 공개 설정 확인

### 3. 데이터베이스 연결 실패

#### 문제: `password authentication failed`

**증상**:

```
ERROR: password authentication failed for user 'neondb_owner'
```

**해결**:

1. Neon Console에서 비밀번호 확인
2. `.env` 파일의 `NEON_DB_PASSWORD` 확인
3. 호스트 주소 확인 (`a1rnsip1` vs `alrnsip1`)

#### 문제: `CannotGetJdbcConnectionException`

**증상**:

```
Failed to obtain JDBC Connection
```

**해결**:

1. 네트워크 연결 확인:

   ```bash
   telnet ep-calm-credit-a1rnsip1-pooler.ap-southeast-1.aws.neon.tech 5432
   ```
2. 환경 변수 확인:

   ```bash
   docker exec ohgun-api printenv | grep NEON
   ```
3. SSL 설정 확인:

   - JDBC URL에 `sslmode=require` 포함 확인
   - `channel_binding=require` 파라미터 추가 시도

### 4. Redis 연결 실패

#### 문제: `Redis health check failed`

**증상**:

```
Unable to connect to Redis
WRONGPASS invalid username-password pair
```

**해결**:

1. Upstash Redis 비밀번호 확인
2. `.env` 파일의 `UPSTASH_REDIS_PASSWORD` 확인
3. SSL 설정 확인 (`ssl.enabled: true`)

### 5. 포트 연결 실패

#### 문제: `Connection refused` (로컬에서 EC2 접속 시)

**해결**:

1. Security Group에서 포트 8080 열기
2. 컨테이너 포트 매핑 확인:

   ```bash
   docker ps | grep ohgun-api
   # 8080:8080이어야 함
   ```
3. 컨테이너 재시작:

   ```bash
   docker stop ohgun-api
   docker rm ohgun-api
   docker run -d --name ohgun-api -p 8080:8080 --env-file .env --restart unless-stopped ohgun0325/ohgun-api:latest
   ```

### 6. 애플리케이션 시작 실패

#### 문제: JWT 환경 변수 오류

**증상**:

```
Failed to bind properties under 'jwt.access-token-validity-in-seconds' to long
```

**해결**:
`.env` 파일에 JWT 환경 변수 추가:

```env
JWT_SECRET=your-secret-key-change-in-production-min-256-bits
JWT_EXPIRATION=86400
JWT_REFRESH_EXPIRATION=2592000
```

#### 문제: 컨테이너가 계속 재시작됨

**해결**:

```bash
# 로그 확인
docker logs ohgun-api --tail 100

# 오류 메시지 확인 후 해결
```

---

## 전체 흐름 요약

### 1. 개발 환경 → GitHub

```
로컬 개발
    ↓
코드 수정
    ↓
git add .
    ↓
git commit -m "메시지"
    ↓
git push origin main
```

### 2. GitHub → Docker Hub

```
GitHub 저장소 (ohgun-api)
    ↓
GitHub Actions 자동 실행
    ↓
Gradle 빌드
    ↓
Docker 이미지 빌드
    ↓
Docker Hub에 푸시
    (ohgun0325/ohgun-api:latest)
```

### 3. Docker Hub → EC2

```
EC2 서버 접속
    ↓
Docker 설치
    ↓
docker pull ohgun0325/ohgun-api:latest
    ↓
.env 파일 생성 (환경 변수)
    ↓
docker run (컨테이너 실행)
```

### 4. EC2 → 클라우드 서비스

```
애플리케이션 시작
    ↓
환경 변수 읽기 (.env)
    ↓
Neon DB 연결 (PostgreSQL)
    ↓
Upstash Redis 연결
    ↓
애플리케이션 실행 완료
```

### 5. 외부 접속 확인

```
로컬 컴퓨터
    ↓
http://3.35.26.129:8080/actuator/health
    ↓
EC2 Security Group (포트 8080)
    ↓
EC2 인스턴스
    ↓
Docker 컨테이너 (ohgun-api)
    ↓
Spring Boot 애플리케이션
```

---

## 핵심 포인트 정리

### Docker Hub 연결

- ✅ GitHub Actions로 자동 빌드 및 푸시
- ✅ 이미지: `ohgun0325/ohgun-api:latest`
- ✅ EC2에서 `docker pull`로 다운로드 가능

### EC2 서버 설정

- ✅ Docker 설치 (공식 스크립트 사용)
- ✅ Docker Compose 설치
- ✅ 작업 디렉토리: `/opt/ohgun-api`

### 클라우드 서비스 연결

- ✅ Neon DB: SSL 필수, 호스트 주소 정확히 확인
- ✅ Upstash Redis: SSL 필수, 환경 변수 필수
- ✅ 네트워크 연결 테스트 (telnet/nc)

### 배포 과정

- ✅ `.env` 파일로 환경 변수 관리
- ✅ `docker run` 또는 `docker-compose` 사용
- ✅ 포트 매핑: `8080:8080` (중요!)

### 테스트 및 확인

- ✅ EC2 내부: `curl http://localhost:8080/actuator/health`
- ✅ 로컬에서: `Invoke-WebRequest http://3.35.26.129:8080/actuator/health`
- ✅ Security Group: 포트 8080 열기

---

## 체크리스트

### 사전 준비

- [ ] Docker Hub 계정 및 이미지 확인
- [ ] EC2 인스턴스 생성 및 접속 가능
- [ ] Neon DB 연결 정보 확인
- [ ] Upstash Redis 연결 정보 확인
- [ ] EC2 Security Group 확인

### EC2 서버 설정

- [ ] Docker 설치 완료
- [ ] Docker Compose 설치 완료
- [ ] 작업 디렉토리 생성 (`/opt/ohgun-api`)
- [ ] docker 그룹 권한 적용

### 클라우드 서비스 연결

- [ ] Neon DB 네트워크 연결 테스트 성공
- [ ] `.env` 파일 생성 및 설정 완료
- [ ] 환경 변수 확인

### 배포 및 테스트

- [ ] Docker 이미지 pull 성공
- [ ] 컨테이너 실행 성공
- [ ] 애플리케이션 시작 완료
- [ ] EC2 내부 헬스 체크 성공
- [ ] Security Group 포트 8080 열기
- [ ] 로컬에서 EC2 접속 테스트 성공

---

## 다음 단계

현재까지 완료:

- ✅ Docker Hub 연결
- ✅ EC2 서버 설정
- ✅ 클라우드 서비스 연결
- ✅ 수동 배포 성공

다음 단계:

- [ ] GitHub Actions에 EC2 자동 배포 단계 추가
- [ ] 코드 푸시만으로 자동 배포 테스트

---

## 참고 자료

- [Docker 공식 문서](https://docs.docker.com/)
- [Docker Compose 문서](https://docs.docker.com/compose/)
- [Neon DB 문서](https://neon.tech/docs)
- [Upstash Redis 문서](https://docs.upstash.com/redis)
- [AWS EC2 문서](https://docs.aws.amazon.com/ec2/)
- [Spring Boot Actuator](https://docs.spring.io/spring-boot/docs/current/reference/html/actuator.html)

---

**작성일**: 2026-01-02
**프로젝트**: api.ohgun.site
**버전**: 1.0.0
