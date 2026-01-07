# CORS 에러 해결 가이드

## 현재 상황

- `SecurityConfig.java`에 `https://www.ohgun.kr`가 이미 허용되어 있음
- Gateway CORS 설정도 수정 완료
- 하지만 여전히 CORS 에러 발생

---

## 가능한 원인

### 1. 배포가 완료되지 않음
- GitHub Actions가 아직 실행 중일 수 있음
- EC2에서 컨테이너가 재시작되지 않았을 수 있음

### 2. Nginx가 CORS 헤더를 덮어쓰고 있음
- Nginx 설정에서 CORS 헤더를 추가해야 할 수 있음

### 3. 브라우저 캐시 문제
- 브라우저가 이전 응답을 캐시하고 있을 수 있음

---

## 해결 방법

### 1단계: 배포 상태 확인

#### GitHub Actions 확인
1. GitHub 저장소 → **Actions** 탭
2. 최신 워크플로우 실행 확인
3. 모든 단계가 ✅ (초록색)인지 확인

#### EC2에서 확인
```bash
# EC2에 SSH 접속 후

# 1. 컨테이너 상태 확인
docker ps | grep ohgun-api

# 2. 최근 로그 확인 (CORS 관련)
docker logs ohgun-api --tail 100 | grep -i cors

# 3. 애플리케이션 시작 시간 확인
docker logs ohgun-api | grep "Started MonolithicApplication"
```

---

### 2단계: CORS 헤더 직접 확인

#### curl로 테스트
```bash
# OPTIONS 요청 (Preflight)
curl -X OPTIONS \
  -H "Origin: https://www.ohgun.kr" \
  -H "Access-Control-Request-Method: GET" \
  -H "Access-Control-Request-Headers: Content-Type" \
  -v https://api.ohgun.kr/oauth/naver/login-url

# 실제 GET 요청
curl -X GET \
  -H "Origin: https://www.ohgun.kr" \
  -v https://api.ohgun.kr/oauth/naver/login-url
```

**예상 응답 헤더:**
```
Access-Control-Allow-Origin: https://www.ohgun.kr
Access-Control-Allow-Credentials: true
Access-Control-Allow-Methods: GET, POST, PUT, DELETE, PATCH, OPTIONS
```

---

### 3단계: Nginx 설정 확인 (필요시)

EC2에서 Nginx 설정 확인:
```bash
# Nginx 설정 파일 확인
sudo cat /etc/nginx/sites-available/default
# 또는
sudo cat /etc/nginx/nginx.conf
```

**Nginx에서 CORS 헤더 추가 (필요시):**
```nginx
location / {
    proxy_pass http://localhost:8080;
    
    # CORS 헤더 추가
    add_header 'Access-Control-Allow-Origin' 'https://www.ohgun.kr' always;
    add_header 'Access-Control-Allow-Credentials' 'true' always;
    add_header 'Access-Control-Allow-Methods' 'GET, POST, PUT, DELETE, PATCH, OPTIONS' always;
    add_header 'Access-Control-Allow-Headers' '*' always;
    
    # OPTIONS 요청 처리
    if ($request_method = 'OPTIONS') {
        add_header 'Access-Control-Allow-Origin' 'https://www.ohgun.kr' always;
        add_header 'Access-Control-Allow-Credentials' 'true' always;
        add_header 'Access-Control-Allow-Methods' 'GET, POST, PUT, DELETE, PATCH, OPTIONS' always;
        add_header 'Access-Control-Allow-Headers' '*' always;
        add_header 'Access-Control-Max-Age' '3600' always;
        add_header 'Content-Type' 'text/plain; charset=utf-8' always;
        add_header 'Content-Length' '0' always;
        return 204;
    }
}
```

**Nginx 재시작:**
```bash
sudo nginx -t  # 설정 파일 검증
sudo systemctl reload nginx  # 재시작
```

---

### 4단계: 브라우저 캐시 클리어

1. **Chrome DevTools 열기** (F12)
2. **Network 탭** 선택
3. **Disable cache** 체크
4. **페이지 새로고침** (Ctrl + Shift + R)

---

### 5단계: 애플리케이션 강제 재시작

```bash
# EC2에서
docker restart ohgun-api

# 로그 확인
docker logs -f ohgun-api
```

---

## 빠른 확인 체크리스트

- [ ] GitHub Actions 배포 완료 확인
- [ ] EC2 컨테이너 재시작 확인
- [ ] curl로 CORS 헤더 확인
- [ ] 브라우저 캐시 클리어
- [ ] Nginx 설정 확인 (필요시)

---

## 추가 디버깅

### Spring Boot 로그 레벨 변경

`application.yaml`에 추가:
```yaml
logging:
  level:
    org.springframework.web.cors: DEBUG
    org.springframework.security: DEBUG
```

이렇게 하면 CORS 관련 상세 로그를 확인할 수 있습니다.

---

## 참고사항

- **CORS Preflight 요청**: 브라우저는 실제 요청 전에 OPTIONS 요청을 보냅니다.
- **allow-credentials: true**: 이 설정이 있으면 `allowed-origins`에 `*`를 사용할 수 없습니다.
- **Nginx 프록시**: Nginx가 중간에 있으면 Nginx에서도 CORS 헤더를 추가해야 할 수 있습니다.

