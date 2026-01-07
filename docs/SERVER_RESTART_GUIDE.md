# 서버 재시작 가이드 (로컬 & EC2)

환경 변수 변경 후 서버를 재시작하는 방법을 단계별로 설명합니다.

---

## 📋 목차

1. [로컬 환경 재시작](#로컬-환경-재시작)
2. [EC2 환경 재시작](#ec2-환경-재시작)
3. [GitHub Secret 업데이트](#github-secret-업데이트)

---

## 🖥️ 로컬 환경 재시작

### 방법 1: Docker Compose 사용 (권장)

#### 1-1. 현재 실행 중인 컨테이너 확인

```bash
# 프로젝트 루트 디렉토리에서
cd C:\Users\hi\Documents\classs\class

# 실행 중인 컨테이너 확인
docker-compose ps
```

**예상 출력:**
```
NAME                IMAGE                    STATUS
ohgun-api           ohgun-api:latest         Up 5 minutes
redis               redis:7-alpine           Up 5 minutes
```

#### 1-2. 컨테이너 재시작

```bash
# 모든 서비스 재시작
docker-compose restart

# 또는 특정 서비스만 재시작 (백엔드만)
docker-compose restart api-service
```

#### 1-3. 로그 확인

```bash
# 실시간 로그 확인
docker-compose logs -f api-service

# 또는 특정 컨테이너 로그
docker logs -f ohgun-api
```

**정상 시작 확인:**
- `Started OhgunApplication in X.XXX seconds` 메시지 확인
- 에러 없이 애플리케이션이 시작되었는지 확인

---

### 방법 2: Docker Compose Down & Up (완전 재시작)

환경 변수 변경이 제대로 적용되지 않을 때 사용:

```bash
# 1. 모든 컨테이너 중지 및 제거
docker-compose down

# 2. 컨테이너 재생성 및 시작
docker-compose up -d

# 3. 로그 확인
docker-compose logs -f api-service
```

**장점:**
- 환경 변수 변경이 확실히 적용됨
- 깨끗한 상태에서 재시작

**단점:**
- 약간 더 오래 걸림 (10-20초)

---

### 방법 3: Spring Boot 직접 실행 (Docker 미사용 시)

```bash
# api.ohgun.site 디렉토리로 이동
cd api.ohgun.site

# Gradle로 실행
./gradlew bootRun

# 또는 빌드 후 실행
./gradlew build
java -jar build/libs/ohgun-api-*.jar
```

---

## ☁️ EC2 환경 재시작

### 방법 1: GitHub Secret 업데이트 후 자동 재배포 (권장) ⭐

#### 1-1. GitHub Secret 업데이트

1. **GitHub 저장소 접속**
   - `https://github.com/ohgun0325/ohgun-api` (또는 해당 저장소)
   - 또는 메인 저장소의 Settings

2. **Secrets 메뉴 이동**
   - 저장소 → **Settings** → **Secrets and variables** → **Actions**

3. **EC2_ENV_FILE Secret 찾기**
   - Secret 목록에서 `EC2_ENV_FILE` 찾기
   - **Update** 버튼 클릭

4. **새로운 .env 내용 입력**
   - 로컬의 `.env` 파일 전체 내용 복사
   - **개인 Neon DB 정보 포함**
   - **개인 Upstash Redis 정보 포함**
   - Secret 값에 붙여넣기

5. **저장**
   - **Update secret** 버튼 클릭

#### 1-2. 코드 변경사항 커밋 및 푸시

```bash
# 변경사항 확인
git status

# 변경된 파일 추가
git add docker-compose.yaml
git add api.ohgun.site/src/main/resources/application.yaml
git add application-production.yaml

# 커밋
git commit -m "chore: update to personal Neon DB and Upstash Redis"

# 푸시 (main 브랜치)
git push origin main
```

#### 1-3. GitHub Actions 자동 배포 확인

1. **GitHub Actions 페이지 이동**
   - 저장소 → **Actions** 탭
   - 최신 워크플로우 실행 확인

2. **빌드 및 배포 진행 상황 확인**
   - "Build and Push Docker Image" 단계 완료 대기
   - "Deploy to EC2" 단계 완료 대기
   - 모든 단계가 ✅ (초록색)이면 성공

3. **배포 완료 확인**
   - EC2에서 자동으로 새 이미지를 Pull
   - 컨테이너가 자동으로 재시작됨

**예상 시간:** 5-10분

---

### 방법 2: EC2에서 수동 재시작

GitHub Actions를 사용하지 않고 직접 EC2에서 재시작:

#### 2-1. EC2에 SSH 접속

```bash
# Windows PowerShell 또는 Git Bash에서
ssh -i "C:\Users\hi\Documents\ohgun-keypair.pem" ec2-user@13.125.xxx.xxx

# 또는
ssh -i "C:\Users\hi\Documents\ohgun-keypair.pem" ec2-user@ec2-xxx.ap-northeast-2.compute.amazonaws.com
```

**EC2 주소 확인:**
- AWS 콘솔 → EC2 → Instances → Public IPv4 address

#### 2-2. 컨테이너 재시작

```bash
# EC2에 접속 후

# 1. 현재 실행 중인 컨테이너 확인
docker ps | grep ohgun-api

# 2. 컨테이너 재시작
docker restart ohgun-api

# 3. 로그 확인
docker logs -f ohgun-api
```

#### 2-3. 새 이미지 Pull 후 재시작 (환경 변수 변경 시)

```bash
# 1. 새 이미지 다운로드
docker pull ohgun0325/ohgun-api:latest

# 2. 기존 컨테이너 중지 및 제거
docker stop ohgun-api
docker rm ohgun-api

# 3. 새 이미지로 컨테이너 실행
# (EC2의 .env 파일이 최신인지 확인 필요)
cd /opt/ohgun-api
docker-compose down
docker-compose up -d

# 또는 직접 실행
docker run -d \
  --name ohgun-api \
  -p 8080:8080 \
  --env-file /opt/ohgun-api/.env \
  --restart unless-stopped \
  ohgun0325/ohgun-api:latest
```

---

## 🔐 GitHub Secret 업데이트 상세 가이드

### EC2_ENV_FILE Secret 업데이트

#### 1. 로컬 .env 파일 내용 확인

```bash
# 프로젝트 루트에서
cat .env
```

**확인할 내용:**
- ✅ `NEON_DB_HOST=ep-dark-violet-a1dtvvt8-pooler.ap-southeast-1.aws.neon.tech`
- ✅ `NEON_DB_PASSWORD=npg_1yNpvxl5fRnK`
- ✅ `UPSTASH_REDIS_HOST=ample-puma-6304.upstash.io`
- ✅ `UPSTASH_REDIS_PASSWORD=ARigAAImcDFhNWZ1OTg4M2JjNmI0NTQ1YmRhYmFlMGRjZjkxNWM2YXAxNjMwNA`

#### 2. GitHub에서 Secret 업데이트

**단계별:**

1. **GitHub 저장소 접속**
   ```
   https://github.com/ohgun0325/ohgun-api
   ```

2. **Settings 이동**
   - 저장소 상단 메뉴 → **Settings**

3. **Secrets 메뉴**
   - 왼쪽 사이드바 → **Secrets and variables** → **Actions**

4. **EC2_ENV_FILE 찾기**
   - Secret 목록에서 `EC2_ENV_FILE` 찾기
   - 오른쪽의 **연필 아이콘 (Update)** 클릭

5. **새 값 입력**
   - 로컬 `.env` 파일의 **전체 내용** 복사
   - Secret 값 입력란에 붙여넣기
   - **Update secret** 버튼 클릭

#### 3. 확인

- Secret 목록에서 `EC2_ENV_FILE`이 "Updated X minutes ago"로 표시되는지 확인

---

## ✅ 재시작 후 확인 사항

### 로컬 환경 확인

```bash
# 1. 컨테이너 실행 상태 확인
docker-compose ps

# 2. 애플리케이션 로그 확인
docker-compose logs api-service | tail -50

# 3. 헬스 체크
curl http://localhost:8080/actuator/health

# 4. Neon DB 연결 확인 (로그에서)
docker-compose logs api-service | grep -i "neon\|postgres"
```

**정상 확인:**
- ✅ 컨테이너가 `Up` 상태
- ✅ 로그에 "Started OhgunApplication" 메시지
- ✅ 헬스 체크가 `200 OK` 반환
- ✅ Neon DB 연결 성공 메시지

---

### EC2 환경 확인

```bash
# EC2에 SSH 접속 후

# 1. 컨테이너 실행 상태 확인
docker ps | grep ohgun-api

# 2. 애플리케이션 로그 확인
docker logs ohgun-api --tail 50

# 3. 헬스 체크
curl http://localhost:8080/actuator/health

# 4. 외부 접근 테스트
curl https://api.ohgun.kr/oauth/naver/login-url
```

**정상 확인:**
- ✅ 컨테이너가 실행 중
- ✅ 로그에 에러 없음
- ✅ 헬스 체크 성공
- ✅ 외부 API 호출 성공

---

## 🚨 문제 해결

### 로컬에서 컨테이너가 재시작되지 않는 경우

```bash
# 1. 강제 중지 및 제거
docker-compose down

# 2. 포트 확인 (8080 포트가 사용 중인지)
netstat -ano | findstr :8080

# 3. 완전히 재시작
docker-compose up -d --force-recreate

# 4. 로그 확인
docker-compose logs -f api-service
```

### EC2에서 환경 변수가 적용되지 않는 경우

```bash
# 1. EC2의 .env 파일 확인
cat /opt/ohgun-api/.env | grep NEON_DB
cat /opt/ohgun-api/.env | grep UPSTASH_REDIS

# 2. GitHub Secret이 올바른지 확인
# (GitHub에서 EC2_ENV_FILE Secret 내용 확인)

# 3. 컨테이너 환경 변수 확인
docker exec ohgun-api printenv | grep NEON_DB
docker exec ohgun-api printenv | grep UPSTASH_REDIS

# 4. 컨테이너 재생성
docker-compose down
docker-compose up -d
```

### GitHub Actions 배포 실패 시

1. **Actions 탭에서 에러 확인**
   - 빨간색 ❌ 표시된 단계 클릭
   - 에러 메시지 확인

2. **일반적인 원인:**
   - GitHub Secret 값이 잘못됨
   - Docker Hub 인증 실패
   - EC2 SSH 연결 실패

3. **해결 방법:**
   - GitHub Secret 재확인 및 업데이트
   - 워크플로우 재실행 (Re-run jobs)

---

## 📝 요약

### 로컬 환경
```bash
# 가장 빠른 방법
docker-compose restart api-service

# 환경 변수 변경 시
docker-compose down
docker-compose up -d
```

### EC2 환경
```bash
# 방법 1: GitHub Secret 업데이트 + git push (권장)
# 1. GitHub에서 EC2_ENV_FILE Secret 업데이트
# 2. git push origin main
# 3. GitHub Actions 자동 배포 대기

# 방법 2: EC2에서 수동 재시작
ssh ec2-user@EC2_IP
docker restart ohgun-api
```

---

## 🔗 관련 문서

- [EC2 재시작 가이드](./EC2_RESTART_GUIDE.md)
- [GitHub Secrets 설정 가이드](./GITHUB_SECRETS_SETUP_GUIDE.md)
- [GitHub Actions 자동 배포 가이드](./GITHUB_ACTIONS_AUTOMATIC_DEPLOYMENT.md)

