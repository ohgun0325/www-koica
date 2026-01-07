# EC2 환경 변수 업데이트 가이드

EC2에서 팀 DB/Redis를 개인 DB/Redis로 변경하는 방법입니다.

---

## 🔍 현재 상황 확인

EC2에서 확인한 환경 변수:
- ❌ `NEON_DB_HOST=ep-calm-credit-alrnsip1-pooler...` (팀 DB)
- ❌ `UPSTASH_REDIS_HOST=awaited-insect-5667.upstash.io` (팀 Redis)

변경해야 할 값:
- ✅ `NEON_DB_HOST=ep-dark-violet-a1dtvvt8-pooler.ap-southeast-1.aws.neon.tech` (개인 DB)
- ✅ `UPSTASH_REDIS_HOST=ample-puma-6304.upstash.io` (개인 Redis)

---

## 방법 1: GitHub Secret 업데이트 후 자동 재배포 (권장) ⭐

### 1단계: GitHub Secret 업데이트

1. **GitHub 저장소 접속**
   ```
   https://github.com/ohgun0325/ohgun-api
   ```
   (또는 해당 백엔드 저장소)

2. **Settings → Secrets 이동**
   - 저장소 상단 메뉴 → **Settings**
   - 왼쪽 사이드바 → **Secrets and variables** → **Actions**

3. **EC2_ENV_FILE Secret 찾기**
   - Secret 목록에서 `EC2_ENV_FILE` 찾기
   - 오른쪽의 **연필 아이콘 (Update)** 클릭

4. **로컬 .env 파일 내용 복사**
   - 로컬 프로젝트의 `.env` 파일 열기
   - **전체 내용** 복사 (Ctrl+A → Ctrl+C)
   - 다음 정보가 포함되어 있는지 확인:
     ```
     NEON_DB_HOST=ep-dark-violet-a1dtvvt8-pooler.ap-southeast-1.aws.neon.tech
     NEON_DB_PASSWORD=npg_1yNpvxl5fRnK
     UPSTASH_REDIS_HOST=ample-puma-6304.upstash.io
     UPSTASH_REDIS_PASSWORD=ARigAAImcDFhNWZ1OTg4M2JjNmI0NTQ1YmRhYmFlMGRjZjkxNWM2YXAxNjMwNA
     ```

5. **Secret 값 업데이트**
   - 기존 내용 삭제
   - 복사한 `.env` 전체 내용 붙여넣기
   - **Update secret** 버튼 클릭

### 2단계: GitHub Actions 트리거

#### 옵션 A: 코드 푸시로 트리거 (권장)

```bash
# 로컬에서
cd C:\Users\hi\Documents\classs\class

# 변경사항 확인
git status

# 변경된 파일 추가 (이미 커밋했다면 스킵)
git add docker-compose.yaml
git add api.ohgun.site/src/main/resources/application.yaml
git add application-production.yaml

# 더미 커밋 생성 (환경 변수 변경 트리거용)
git commit --allow-empty -m "chore: trigger EC2 deployment with updated env vars"

# 푸시
git push origin main
```

#### 옵션 B: GitHub Actions 수동 실행

1. GitHub 저장소 → **Actions** 탭
2. 최신 워크플로우 선택
3. **Run workflow** 버튼 클릭
4. **Run workflow** 확인

### 3단계: 배포 완료 대기

1. **GitHub Actions 페이지에서 확인**
   - 저장소 → **Actions** 탭
   - 최신 워크플로우 실행 확인
   - 모든 단계가 ✅ (초록색)이면 성공

2. **예상 시간:** 5-10분

### 4단계: EC2에서 확인

```bash
# EC2에 SSH 접속 후

# 1. 환경 변수 확인
docker exec ohgun-api printenv | grep NEON_DB
docker exec ohgun-api printenv | grep UPSTASH_REDIS

# 예상 출력:
# NEON_DB_HOST=ep-dark-violet-a1dtvvt8-pooler.ap-southeast-1.aws.neon.tech
# UPSTASH_REDIS_HOST=ample-puma-6304.upstash.io
```

---

## 방법 2: EC2에서 직접 수동 업데이트 (빠른 방법)

GitHub Actions를 기다리지 않고 즉시 변경하려면:

### 1단계: EC2에 SSH 접속

```bash
ssh -i "C:\Users\hi\Documents\ohgun-keypair.pem" ec2-user@EC2_IP주소
```

### 2단계: .env 파일 확인 및 업데이트

```bash
# EC2에 접속 후

# 1. 현재 .env 파일 확인
cd /opt/ohgun-api
cat .env | grep NEON_DB
cat .env | grep UPSTASH_REDIS

# 2. .env 파일 백업
cp .env .env.backup

# 3. .env 파일 편집
nano .env
# 또는
vi .env
```

**수정할 내용:**
```bash
# 기존 (팀 DB/Redis)
NEON_DB_HOST=ep-calm-credit-alrnsip1-pooler.ap-southeast-1.aws.neon.tech
NEON_DB_PASSWORD=npg_kDZv9cRNij8A
UPSTASH_REDIS_HOST=awaited-insect-5667.upstash.io
UPSTASH_REDIS_PASSWORD=ARYjAAImcDIyYTNkMDE3YjJlYjA0MDVjODRjYTE5NWRjZmRmMDZ1NXAYNTY2Nw

# 변경 후 (개인 DB/Redis)
NEON_DB_HOST=ep-dark-violet-a1dtvvt8-pooler.ap-southeast-1.aws.neon.tech
NEON_DB_PASSWORD=npg_1yNpvxl5fRnK
UPSTASH_REDIS_HOST=ample-puma-6304.upstash.io
UPSTASH_REDIS_PASSWORD=ARigAAImcDFhNWZ1OTg4M2JjNmI0NTQ1YmRhYmFlMGRjZjkxNWM2YXAxNjMwNA
```

**nano 편집기 사용법:**
- `Ctrl + W`: 검색
- `Ctrl + O`: 저장
- `Ctrl + X`: 종료

### 3단계: 컨테이너 재시작

```bash
# 1. 기존 컨테이너 중지 및 제거
docker stop ohgun-api
docker rm ohgun-api

# 2. 새 환경 변수로 컨테이너 실행
docker run -d \
  --name ohgun-api \
  -p 8080:8080 \
  --env-file /opt/ohgun-api/.env \
  --restart unless-stopped \
  ohgun0325/ohgun-api:latest

# 3. 로그 확인
docker logs -f ohgun-api
```

### 4단계: 환경 변수 확인

```bash
# 환경 변수 확인
docker exec ohgun-api printenv | grep NEON_DB
docker exec ohgun-api printenv | grep UPSTASH_REDIS

# Health check 확인
curl http://localhost:8080/actuator/health
```

---

## 방법 3: Docker Compose 사용 (EC2에 docker-compose.yaml이 있는 경우)

```bash
# EC2에 접속 후

cd /opt/ohgun-api

# 1. .env 파일 업데이트 (위의 방법 2 참고)

# 2. 컨테이너 재시작
docker-compose down
docker-compose up -d

# 3. 로그 확인
docker-compose logs -f api-service
```

---

## ✅ 최종 확인

### 환경 변수 확인

```bash
# EC2에서
docker exec ohgun-api printenv | grep NEON_DB
docker exec ohgun-api printenv | grep UPSTASH_REDIS
```

**정상 확인:**
```
NEON_DB_HOST=ep-dark-violet-a1dtvvt8-pooler.ap-southeast-1.aws.neon.tech
NEON_DB_PASSWORD=npg_1yNpvxl5fRnK
UPSTASH_REDIS_HOST=ample-puma-6304.upstash.io
UPSTASH_REDIS_PASSWORD=ARigAAImcDFhNWZ1OTg4M2JjNmI0NTQ1YmRhYmFlMGRjZjkxNWM2YXAxNjMwNA
```

### Health Check 확인

```bash
curl http://localhost:8080/actuator/health
```

**정상 확인:**
- `"db":{"status":"UP"}` - 개인 Neon DB 연결 성공
- `"redis":{"status":"UP"}` - 개인 Upstash Redis 연결 성공

### API 테스트

```bash
# 외부에서 테스트
curl https://api.ohgun.kr/oauth/naver/login-url

# 또는 EC2 내부에서
curl http://localhost:8080/oauth/naver/login-url
```

---

## 🚨 문제 해결

### 환경 변수가 변경되지 않는 경우

```bash
# 1. .env 파일이 올바른지 확인
cat /opt/ohgun-api/.env | grep -E "NEON_DB|UPSTASH_REDIS"

# 2. 컨테이너가 .env 파일을 읽는지 확인
docker inspect ohgun-api | grep -A 10 "Env"

# 3. 컨테이너 완전히 재생성
docker stop ohgun-api
docker rm ohgun-api
docker run -d \
  --name ohgun-api \
  -p 8080:8080 \
  --env-file /opt/ohgun-api/.env \
  --restart unless-stopped \
  ohgun0325/ohgun-api:latest
```

### GitHub Actions 배포가 실패하는 경우

1. **GitHub Secret 확인**
   - `EC2_ENV_FILE` Secret이 올바른지 확인
   - `.env` 파일 전체 내용이 포함되어 있는지 확인

2. **워크플로우 로그 확인**
   - GitHub → Actions → 실패한 워크플로우 클릭
   - 에러 메시지 확인

3. **수동으로 재시도**
   - 방법 2 (EC2에서 직접 수동 업데이트) 사용

---

## 📝 요약

| 방법 | 속도 | 권장 상황 |
|------|------|----------|
| 방법 1: GitHub Secret + 자동 배포 | 5-10분 | 정기적인 배포, 자동화 선호 |
| 방법 2: EC2 직접 수정 | 즉시 | 빠른 변경 필요, 테스트 |
| 방법 3: Docker Compose | 즉시 | docker-compose.yaml 사용 시 |

**권장:** 방법 1 (GitHub Secret 업데이트)을 사용하여 자동화된 배포를 유지하세요.

