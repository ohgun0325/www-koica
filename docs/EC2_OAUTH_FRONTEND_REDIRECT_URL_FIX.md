# EC2 OAUTH_FRONTEND_REDIRECT_URL 설정 가이드

## 문제 상황

백엔드가 `http://localhost:3000`으로 리다이렉트하려고 시도하여 연결이 거부됨.

**원인:**
- EC2 환경 변수 `OAUTH_FRONTEND_REDIRECT_URL`이 설정되지 않음
- 기본값 `http://localhost:3000`이 사용됨

---

## 해결 방법

### 방법 1: EC2에서 직접 수정 (빠른 방법)

```bash
# EC2에 SSH 접속 후
cd /opt/ohgun-api

# .env 파일 편집
nano .env
```

**추가할 내용:**
```bash
OAUTH_FRONTEND_REDIRECT_URL=https://www.ohgun.kr
```

**저장 및 나가기:**
- `Ctrl + O` → `Enter` (저장)
- `Ctrl + X` (나가기)

**컨테이너 재시작:**
```bash
docker restart ohgun-api

# 환경 변수 확인
docker exec ohgun-api printenv | grep OAUTH_FRONTEND_REDIRECT_URL
```

**예상 출력:**
```
OAUTH_FRONTEND_REDIRECT_URL=https://www.ohgun.kr
```

---

### 방법 2: GitHub Secret 업데이트 후 재배포 (권장)

#### 1단계: 로컬 .env 파일 확인

로컬 `.env` 파일에 다음이 포함되어 있는지 확인:
```bash
OAUTH_FRONTEND_REDIRECT_URL=https://www.ohgun.kr
```

#### 2단계: GitHub Secret 업데이트

1. GitHub 저장소 → **Settings** → **Secrets and variables** → **Actions**
2. `EC2_ENV_FILE` Secret 찾기 → **Update** 클릭
3. 로컬 `.env` 파일 전체 내용 복사 후 붙여넣기
4. **Update secret** 클릭

#### 3단계: 재배포 트리거

```bash
# 로컬에서
git commit --allow-empty -m "chore: update OAUTH_FRONTEND_REDIRECT_URL"
git push origin main
```

#### 4단계: 배포 완료 대기

- GitHub Actions에서 빌드 및 배포 완료 대기 (5-10분)
- EC2에서 자동으로 새 이미지 Pull 및 재시작

---

## 확인 방법

### 1. 환경 변수 확인

```bash
# EC2에서
docker exec ohgun-api printenv | grep OAUTH_FRONTEND_REDIRECT_URL
```

**정상 확인:**
```
OAUTH_FRONTEND_REDIRECT_URL=https://www.ohgun.kr
```

### 2. 애플리케이션 로그 확인

```bash
docker logs ohgun-api --tail 50
```

**정상 확인:**
- `Started MonolithicApplication` 메시지
- 에러 없이 시작됨

### 3. 네이버 로그인 테스트

1. `https://www.ohgun.kr`에서 네이버 로그인 클릭
2. 로그인 성공 후 `https://www.ohgun.kr/oauth/callback?accessToken=...`로 리다이렉트되는지 확인
3. `localhost:3000`으로 리다이렉트되지 않는지 확인

---

## 환경 변수 값

### 프로덕션 (EC2)
```bash
OAUTH_FRONTEND_REDIRECT_URL=https://www.ohgun.kr
```

### 로컬 개발
```bash
OAUTH_FRONTEND_REDIRECT_URL=http://localhost:3000
```

---

## 요약

| 상황 | 필요한 작업 | 시간 |
|------|------------|------|
| EC2에서 `.env` 직접 수정 | 컨테이너 재시작 | 10초 |
| GitHub Secret 업데이트 | 재배포 | 5-10분 |

**권장:** 방법 1 (EC2 직접 수정)으로 빠르게 해결하고, 이후 방법 2 (GitHub Secret)로 자동화 설정

