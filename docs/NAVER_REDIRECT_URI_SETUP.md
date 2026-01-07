# 네이버 로그인 리다이렉트 URI 설정 가이드

## 현재 상황 분석

### 문제점

`.env` 파일에서 같은 환경 변수 이름이 2번 정의되면:

```env
NAVER_REDIRECT_URI=https://www.ohgun.kr/api/oauth/naver/callback
NAVER_REDIRECT_URI=http://localhost:8080/oauth/naver/callback
```

**결과:** 마지막 값만 사용됩니다. 즉, `http://localhost:8080/oauth/naver/callback`만 사용됩니다.

### 코드 동작 방식

1. **application.yaml:**
```yaml
oauth:
  naver:
    redirect-uri: ${NAVER_REDIRECT_URI}  # 하나의 값만 사용
```

2. **NaverService.java:**
```java
@Value("${oauth.naver.redirect-uri}")
private String redirectUri;  // 하나의 변수만 존재
```

3. **사용 위치:**
```java
public String buildAuthorizeUrl(String state) {
    String url = UriComponentsBuilder.fromHttpUrl(authorizeUrl)
            .queryParam("redirect_uri", redirectUri)  // 하나의 값만 사용
            ...
}
```

## 해결 방법

### 방법 1: 환경별로 다른 .env 파일 사용 (권장) ⭐

#### 로컬 개발용 `.env.local`
```env
NAVER_REDIRECT_URI=http://localhost:8080/oauth/naver/callback
```

#### 프로덕션용 `.env.production`
```env
NAVER_REDIRECT_URI=https://www.ohgun.kr/api/oauth/naver/callback
```

#### 사용 방법

**로컬 개발:**
```bash
# .env.local 파일 사용
cp .env.local .env
# 또는
export $(cat .env.local | xargs)
```

**프로덕션:**
```bash
# .env.production 파일 사용
cp .env.production .env
```

### 방법 2: Spring Profile 사용

#### application.yaml 수정

```yaml
spring:
  profiles:
    active: ${SPRING_PROFILES_ACTIVE:local}

---
# 로컬 프로파일
spring:
  config:
    activate:
      on-profile: local
oauth:
  naver:
    redirect-uri: http://localhost:8080/oauth/naver/callback

---
# 프로덕션 프로파일
spring:
  config:
    activate:
      on-profile: production
oauth:
  naver:
    redirect-uri: https://www.ohgun.kr/api/oauth/naver/callback
```

#### 실행 방법

**로컬:**
```bash
java -jar app.jar --spring.profiles.active=local
# 또는
export SPRING_PROFILES_ACTIVE=local
java -jar app.jar
```

**프로덕션:**
```bash
java -jar app.jar --spring.profiles.active=production
# 또는
export SPRING_PROFILES_ACTIVE=production
java -jar app.jar
```

### 방법 3: 환경 변수 이름 분리 (간단한 방법)

#### .env 파일 수정

```env
# 로컬 개발용
NAVER_REDIRECT_URI_LOCAL=http://localhost:8080/oauth/naver/callback

# 프로덕션용
NAVER_REDIRECT_URI_PROD=https://www.ohgun.kr/api/oauth/naver/callback

# 기본값 (환경에 따라 선택)
NAVER_REDIRECT_URI=${NAVER_REDIRECT_URI_LOCAL}  # 로컬
# 또는
NAVER_REDIRECT_URI=${NAVER_REDIRECT_URI_PROD}   # 프로덕션
```

#### application.yaml 수정

```yaml
oauth:
  naver:
    redirect-uri: ${NAVER_REDIRECT_URI:http://localhost:8080/oauth/naver/callback}
```

### 방법 4: 네이버 개발자 센터에 두 URI 모두 등록 (필수)

어떤 방법을 사용하든, **네이버 개발자 센터에 두 URI를 모두 등록**해야 합니다.

1. [네이버 개발자 센터](https://developers.naver.com/apps/#/list) 접속
2. 애플리케이션 선택
3. **API 설정** → **로그인 오픈 API 서비스 환경** → **서비스 URL**
4. **Callback URL**에 두 URI 모두 추가:
   - `http://localhost:8080/oauth/naver/callback`
   - `https://www.ohgun.kr/api/oauth/naver/callback`

## 추천 방법: 방법 1 (환경별 .env 파일)

가장 간단하고 명확한 방법입니다.

### 설정 예시

#### `.env.local` (로컬 개발용)
```env
NAVER_CLIENT_ID=BgiMQ7PADA36w8xu5Zy0
NAVER_CLIENT_SECRET=bmFQVH_Eef
NAVER_REDIRECT_URI=http://localhost:8080/oauth/naver/callback
```

#### `.env.production` (프로덕션용)
```env
NAVER_CLIENT_ID=BgiMQ7PADA36w8xu5Zy0
NAVER_CLIENT_SECRET=bmFQVH_Eef
NAVER_REDIRECT_URI=https://www.ohgun.kr/api/oauth/naver/callback
```

#### 사용 방법

**로컬 개발:**
```bash
# Windows PowerShell
Copy-Item .env.local .env

# 또는 직접 환경 변수 설정
$env:NAVER_REDIRECT_URI="http://localhost:8080/oauth/naver/callback"
```

**프로덕션:**
```bash
# EC2 또는 배포 환경에서
cp .env.production .env
# 또는
export NAVER_REDIRECT_URI=https://www.ohgun.kr/api/oauth/naver/callback
```

## Docker Compose 사용 시

### docker-compose.yaml 수정

```yaml
services:
  api-service:
    environment:
      - NAVER_REDIRECT_URI=${NAVER_REDIRECT_URI:-http://localhost:8080/oauth/naver/callback}
```

### 사용 방법

**로컬:**
```bash
# .env.local 파일 사용
export $(cat .env.local | xargs)
docker-compose up
```

**프로덕션:**
```bash
# .env.production 파일 사용
export $(cat .env.production | xargs)
docker-compose up
```

## 확인 방법

### 1. 애플리케이션 시작 시 로그 확인

애플리케이션 시작 시 다음 로그가 출력됩니다:

```
========================================
네이버 OAuth 인증 URL 생성:
Client ID: BgiMQ7PADA36w8xu5Zy0
Redirect URI: http://localhost:8080/oauth/naver/callback  # 또는 프로덕션 URI
State: xxxxx
Generated URL: https://nid.naver.com/oauth2.0/authorize?...
========================================
```

### 2. 네이버 개발자 센터 확인

네이버 개발자 센터에서 등록된 Callback URL 목록을 확인하세요.

## 주의사항

### ✅ 해야 할 것

1. **네이버 개발자 센터에 두 URI 모두 등록** (필수)
2. 환경별로 다른 `.env` 파일 사용
3. 실행 환경에 맞는 환경 변수 설정

### ❌ 하지 말아야 할 것

1. 같은 환경 변수 이름을 2번 정의 (마지막 값만 사용됨)
2. 네이버 개발자 센터에 URI를 등록하지 않음 (인증 실패)
3. 프로덕션에서 로컬 URI 사용 (보안 문제)

## 요약

### 현재 문제

```env
NAVER_REDIRECT_URI=https://www.ohgun.kr/api/oauth/naver/callback
NAVER_REDIRECT_URI=http://localhost:8080/oauth/naver/callback
```

→ **마지막 값만 사용됨** (`http://localhost:8080/oauth/naver/callback`)

### 해결 방법

1. **환경별 .env 파일 분리** (`.env.local`, `.env.production`)
2. **네이버 개발자 센터에 두 URI 모두 등록**
3. 실행 환경에 맞는 환경 변수 사용

### 권장 구조

```
.env.local          # 로컬 개발용
.env.production     # 프로덕션용
.env                # 현재 사용 중인 파일 (환경에 따라 복사)
```

---

## 빠른 수정 가이드

### 1단계: .env 파일 수정

`.env` 파일에서 중복된 `NAVER_REDIRECT_URI`를 제거하고 하나만 남기세요:

```env
# 로컬 개발 시
NAVER_REDIRECT_URI=http://localhost:8080/oauth/naver/callback

# 프로덕션 배포 시
NAVER_REDIRECT_URI=https://www.ohgun.kr/api/oauth/naver/callback
```

### 2단계: 네이버 개발자 센터에 두 URI 등록

네이버 개발자 센터에서 두 URI를 모두 등록하세요.

### 3단계: 환경에 맞게 사용

로컬 개발 시와 프로덕션 배포 시 각각 적절한 URI를 사용하세요.

