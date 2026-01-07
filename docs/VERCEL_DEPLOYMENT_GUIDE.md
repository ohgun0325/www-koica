# Vercel 프론트엔드 배포 가이드

## Phase 1: 환경 변수 설정

### 로컬 개발용 환경 변수

프로젝트 루트(`www.ohgun.site/`)에 `.env.local` 파일을 생성하세요:

```bash
# www.ohgun.site/.env.local
NEXT_PUBLIC_OAUTH_BASE_URL=http://localhost:8080
NEXT_PUBLIC_OAUTH_REDIRECT_URL=http://localhost:3000/oauth/callback
```

### 프로덕션 환경 변수 (Vercel)

Vercel 대시보드에서 설정하거나, 아래 내용을 참고하세요:

```bash
# Vercel Environment Variables
NEXT_PUBLIC_OAUTH_BASE_URL=https://api.ohgun.kr
NEXT_PUBLIC_OAUTH_REDIRECT_URL=https://www.ohgun.kr/oauth/callback
```

---

## Phase 2: 백엔드 CORS 설정 수정

백엔드에서 Vercel 도메인을 허용하도록 CORS 설정을 수정해야 합니다.

**파일**: `api.ohgun.site/src/main/java/site/ohgun/api/oauth/config/SecurityConfig.java`

**수정 내용**:
```java
configuration.setAllowedOrigins(List.of(
        "http://localhost:3000",
        "http://localhost:3002",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3002",
        "https://www.ohgun.kr",        // Vercel 프로덕션 도메인
        "https://admin.ohgun.kr",      // Admin 사이트 (필요시)
        "https://*.vercel.app"         // Vercel 프리뷰 도메인 (선택사항)
));
```

---

## Phase 3: Vercel 프로젝트 생성

### 3-1. Vercel 계정 생성

1. https://vercel.com 접속
2. "Sign Up" → GitHub 계정으로 가입
3. GitHub 계정 연동 승인

### 3-2. 프로젝트 Import

1. Vercel 대시보드 → "Add New..." → "Project"
2. GitHub 저장소 선택
   - `ohgun0325/class` 저장소 선택
3. Framework Preset
   - Next.js 자동 감지됨
4. Root Directory 설정
   - `www.ohgun.site` 선택

### 3-3. 빌드 설정

- **Framework Preset**: Next.js
- **Root Directory**: `www.ohgun.site`
- **Build Command**: `pnpm build` (또는 자동 감지)
- **Output Directory**: `.next` (자동 감지)
- **Install Command**: `pnpm install` (자동 감지)

---

## Phase 4: Vercel 환경 변수 설정

### 4-1. 환경 변수 추가

Vercel 대시보드에서:
1. Project Settings → Environment Variables
2. 다음 환경변수 추가:

| Name | Value | Environment |
|------|-------|-------------|
| `NEXT_PUBLIC_OAUTH_BASE_URL` | `https://api.ohgun.kr` | Production, Preview, Development |
| `NEXT_PUBLIC_OAUTH_REDIRECT_URL` | `https://www.ohgun.kr/oauth/callback` | Production |
| `NEXT_PUBLIC_OAUTH_REDIRECT_URL` | `https://your-project.vercel.app/oauth/callback` | Preview, Development |

### 4-2. 환경별 설정

- **Production**: `main` 브랜치 배포 시 사용
- **Preview**: PR 또는 다른 브랜치 배포 시 사용
- **Development**: 로컬 개발 시 사용 (선택사항)

---

## Phase 5: 도메인 연결

### 5-1. Vercel 자동 도메인

배포 후 자동으로 생성됨:
- `your-project.vercel.app`

### 5-2. 커스텀 도메인 연결

1. Vercel 대시보드 → Project Settings → Domains
2. "Add Domain" 클릭
3. 도메인 입력: `www.ohgun.kr`
4. Vercel이 제공하는 DNS 설정 확인:

```
Type: CNAME
Name: www
Value: cname.vercel-dns.com
TTL: 600
```

### 5-3. 가비아 DNS 설정

1. 가비아 DNS 관리 페이지 접속
2. 기존 `www` CNAME 레코드 확인/수정:
   - 호스트: `www`
   - 타입: `CNAME`
   - 값: `cname.vercel-dns.com`
   - TTL: `600`

### 5-4. DNS 전파 확인

```bash
# DNS 확인
nslookup www.ohgun.kr

# 예상 결과: cname.vercel-dns.com 또는 Vercel IP
```

---

## Phase 6: 배포 및 테스트

### 6-1. 자동 배포

코드를 푸시하면 자동으로 배포됩니다:

```bash
git add .
git commit -m "feat: prepare for Vercel deployment"
git push origin main
```

### 6-2. 배포 확인

1. Vercel 대시보드 → Deployments 탭
2. 배포 상태 확인 (약 1-2분 소요)
3. 배포 완료 후 URL 확인

### 6-3. 기능 테스트

1. **메인 페이지 접속**
   - `https://www.ohgun.kr` 접속
   - 페이지 정상 로드 확인

2. **API 연동 테스트**
   - 로그인 버튼 클릭
   - OAuth 로그인 URL 요청 확인
   - 네이버 로그인 페이지로 리다이렉트 확인

3. **OAuth 콜백 테스트**
   - 네이버 로그인 완료 후
   - `https://www.ohgun.kr/oauth/callback`로 리다이렉트 확인
   - 토큰 저장 및 메인 페이지 이동 확인

---

## Phase 7: 문제 해결

### CORS 에러 발생 시

**증상**: 브라우저 콘솔에 CORS 에러 표시

**해결**:
1. 백엔드 CORS 설정 확인
2. Vercel 도메인이 `allowedOrigins`에 포함되어 있는지 확인
3. 백엔드 재배포

### 환경 변수 미적용 시

**증상**: API 호출이 `localhost:8080`으로 가는 경우

**해결**:
1. Vercel 대시보드에서 환경 변수 확인
2. 환경 변수 이름이 `NEXT_PUBLIC_`로 시작하는지 확인
3. 배포 재실행

### 빌드 실패 시

**증상**: Vercel 빌드 로그에 에러 표시

**해결**:
1. 로컬에서 빌드 테스트: `pnpm build`
2. 빌드 로그 확인
3. 의존성 문제 확인: `pnpm install`

---

## 완료 체크리스트

- [ ] 로컬 환경 변수 설정 (`.env.local`)
- [ ] 백엔드 CORS 설정 수정 (Vercel 도메인 추가)
- [ ] 백엔드 재배포
- [ ] Vercel 계정 생성 및 프로젝트 생성
- [ ] Vercel 환경 변수 설정
- [ ] 도메인 연결 (www.ohgun.kr)
- [ ] 배포 테스트
- [ ] OAuth 로그인 테스트

---

## 참고사항

- Vercel은 무료 플랜에서도 충분히 사용 가능
- 자동 HTTPS 설정 (Let's Encrypt)
- 자동 CI/CD (Git push 시 자동 배포)
- 프리뷰 배포 (PR마다 자동 생성)

