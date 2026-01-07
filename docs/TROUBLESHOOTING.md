# 네이버 로그인 오류 해결 가이드

## 현재 문제 상황

### 에러 메시지
- `ERR_CONNECTION_TIMED_OUT`
- `Failed to fetch` - `https://api.ohgun.kr/oauth/naver/login-url`

### 원인 분석

1. **HTTP 메서드 불일치** ✅ 해결됨
   - 프론트엔드: GET 요청
   - NaverController: GET 매핑 (`@GetMapping("/login-url")`)
   - AuthController: POST 매핑 제거됨

2. **연결 타임아웃** ⚠️ 확인 필요
   - 백엔드 서버가 응답하지 않음
   - 가능한 원인:
     - EC2 서버가 실행되지 않음
     - Gateway가 실행되지 않음
     - 방화벽/보안 그룹 설정 문제
     - 네트워크 연결 문제

## 해결 방법

### 1. EC2 서버 상태 확인

```bash
# EC2에 SSH 접속 후
sudo systemctl status docker
docker ps  # 실행 중인 컨테이너 확인
```

### 2. Gateway 실행 확인

```bash
# Gateway 컨테이너가 실행 중인지 확인
docker ps | grep gateway

# Gateway 로그 확인
docker logs gateway-container-name
```

### 3. 방화벽/보안 그룹 확인

EC2 보안 그룹에서 다음 포트가 열려있는지 확인:
- **8080**: Gateway 포트 (외부 접근 가능해야 함)
- **HTTPS (443)**: API 도메인 (`api.ohgun.kr`)

### 4. 네트워크 연결 테스트

```bash
# EC2에서 외부 연결 테스트
curl https://api.ohgun.kr/oauth/naver/login-url

# 또는 로컬에서 테스트
curl https://api.ohgun.kr/health
```

### 5. Gateway 라우팅 확인

Gateway의 `application.yaml`에서:
- `/oauth/**` 경로가 `http://oauth:8080`으로 라우팅됨
- 모놀리식 애플리케이션이 `oauth` 서비스로 실행되어야 함

### 6. 모놀리식 애플리케이션 실행 확인

```bash
# 모놀리식 애플리케이션이 실행 중인지 확인
docker ps | grep api

# 또는
curl http://localhost:8080/oauth/naver/login-url
```

## 현재 구조

### 프론트엔드 (Vercel)
- URL: `https://ohgun.kr`
- 요청: `GET https://api.ohgun.kr/oauth/naver/login-url`

### 백엔드 (EC2)
- Gateway: 포트 8080
- 모놀리식 애플리케이션: 포트 8080 (내부)
- NaverController: `/oauth/naver/login-url` (GET)

## 체크리스트

- [ ] EC2 서버가 실행 중인가?
- [ ] Docker 컨테이너들이 실행 중인가?
- [ ] Gateway가 포트 8080에서 실행 중인가?
- [ ] 모놀리식 애플리케이션이 실행 중인가?
- [ ] 보안 그룹에서 포트 8080이 열려있는가?
- [ ] `api.ohgun.kr` 도메인이 EC2를 가리키고 있는가?
- [ ] Nginx/로드밸런서가 올바르게 설정되어 있는가?

## 빠른 테스트

브라우저에서 직접 접속:
```
https://api.ohgun.kr/oauth/naver/login-url
```

응답이 오면 정상, 타임아웃이면 서버 문제입니다.

