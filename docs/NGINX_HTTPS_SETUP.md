# Nginx 리버스 프록시 및 HTTPS 설정 가이드

## Phase 1: Nginx 설치 및 기본 설정

### 1-1. 패키지 업데이트 및 Nginx 설치

```bash
sudo apt update
sudo apt install -y nginx
sudo systemctl enable nginx
sudo systemctl start nginx
```

**예상 오류 및 해결:**
- `E: Could not get lock /var/lib/dpkg/lock-frontend`
  - 해결: `sudo killall apt apt-get` 또는 잠시 대기 후 재시도
- `Unable to locate package nginx`
  - 해결: `sudo apt update` 재실행

### 1-2. Nginx 상태 확인

```bash
sudo systemctl status nginx
```

**정상 상태 확인:**
- `Active: active (running)` 표시되어야 함
- `enabled` 표시되어야 함 (부팅 시 자동 시작)

**오류 발생 시:**
```bash
# Nginx 재시작
sudo systemctl restart nginx

# 로그 확인
sudo tail -f /var/log/nginx/error.log
```

---

## Phase 2: 방화벽(UFW) 설정

### 2-1. 방화벽 상태 확인

```bash
sudo ufw status
```

**상태 확인:**
- `Status: inactive` → 방화벽 비활성화 상태 (설정 불필요)
- `Status: active` → 방화벽 활성화 상태 (포트 열기 필요)

### 2-2. 방화벽 활성화 시 포트 열기

```bash
sudo ufw allow 'Nginx Full'
sudo ufw allow 22/tcp  # SSH 포트 (이미 열려있을 수 있음)
sudo ufw status
```

**예상 오류:**
- `ufw: command not found`
  - 해결: `sudo apt install ufw -y`

---

## Phase 3: Nginx 리버스 프록시 설정 (HTTP)

### 3-1. 설정 파일 생성

```bash
sudo nano /etc/nginx/sites-available/api.ohgun.kr
```

**설정 파일 내용:**
```nginx
server {
    listen 80;
    server_name api.ohgun.kr;

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_http_version 1.1;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        proxy_read_timeout 60;
        proxy_connect_timeout 60;
    }
}
```

**저장 방법:**
- `Ctrl + O` → Enter (저장)
- `Ctrl + X` (종료)

### 3-2. 설정 파일 활성화

```bash
# 심볼릭 링크 생성
sudo ln -s /etc/nginx/sites-available/api.ohgun.kr /etc/nginx/sites-enabled/

# 기본 설정 파일 비활성화 (충돌 방지)
sudo rm /etc/nginx/sites-enabled/default
```

**예상 오류:**
- `File exists` → 이미 링크가 존재함 (무시하거나 `sudo rm` 후 재생성)

### 3-3. Nginx 문법 체크 및 재시작

```bash
# 문법 체크
sudo nginx -t
```

**정상 출력:**
```
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
```

**오류 발생 시:**
- 설정 파일 문법 오류 확인
- `sudo nano /etc/nginx/sites-available/api.ohgun.kr`로 재수정

```bash
# Nginx 재시작
sudo systemctl reload nginx
```

### 3-4. HTTP 테스트

**EC2에서 테스트:**
```bash
curl http://localhost
curl -H "Host: api.ohgun.kr" http://localhost
```

**브라우저에서 테스트:**
- `http://api.ohgun.kr` (포트 없이 접근)
- Swagger UI가 표시되어야 함

**오류 발생 시:**
```bash
# Nginx 로그 확인
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log

# Docker 컨테이너 확인
docker ps | grep ohgun-api
curl http://127.0.0.1:8080/swagger-ui/index.html
```

---

## Phase 4: Let's Encrypt SSL 인증서 발급

### 4-1. Certbot 설치

```bash
sudo apt install -y certbot python3-certbot-nginx
```

**예상 오류:**
- 패키지 찾을 수 없음
  - 해결: `sudo apt update` 재실행

### 4-2. SSL 인증서 발급

```bash
sudo certbot --nginx -d api.ohgun.kr
```

**진행 중 질문:**
1. **이메일 주소 입력** (인증서 만료 알림용)
2. **약관 동의** → `Y` 입력
3. **이메일 공유 동의** → `Y` 또는 `N` 선택
4. **HTTP → HTTPS 리다이렉트** → `2` 선택 권장

**예상 오류:**
- `Failed to obtain certificate`
  - 원인: DNS 설정이 아직 전파되지 않음
  - 해결: DNS 전파 대기 (최대 24시간)
- `Connection refused`
  - 원인: 포트 80이 막혀있음
  - 해결: 보안 그룹에서 포트 80 확인
- `Domain does not point to this server`
  - 원인: DNS가 다른 IP를 가리킴
  - 해결: `nslookup api.ohgun.kr`로 확인

**성공 시 출력:**
```
Successfully received certificate.
Certificate is saved at: /etc/letsencrypt/live/api.ohgun.kr/fullchain.pem
Key is saved at: /etc/letsencrypt/live/api.ohgun.kr/privkey.pem
```

### 4-3. 인증서 자동 갱신 테스트

```bash
sudo certbot renew --dry-run
```

**정상 출력:**
```
The following certificates are not due for renewal yet:
```

---

## Phase 5: HTTPS 테스트 및 검증

### 5-1. 브라우저 테스트

**접속 URL:**
- `https://api.ohgun.kr/swagger-ui/index.html`
- `http://api.ohgun.kr/swagger-ui/index.html` (자동으로 HTTPS로 리다이렉트)

**확인 사항:**
- ✅ 자물쇠 아이콘 표시
- ✅ "안전한 연결" 표시
- ✅ Swagger UI 정상 표시

### 5-2. SSL 인증서 정보 확인

```bash
# 인증서 만료일 확인
sudo certbot certificates

# SSL 테스트 (온라인 도구)
# https://www.ssllabs.com/ssltest/analyze.html?d=api.ohgun.kr
```

### 5-3. Nginx 최종 설정 확인

```bash
sudo cat /etc/nginx/sites-available/api.ohgun.kr
```

**예상 설정:**
```nginx
# HTTP → HTTPS 리다이렉트
server {
    listen 80;
    server_name api.ohgun.kr;
    return 301 https://$server_name$request_uri;
}

# HTTPS 설정
server {
    listen 443 ssl http2;
    server_name api.ohgun.kr;

    ssl_certificate /etc/letsencrypt/live/api.ohgun.kr/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.ohgun.kr/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_http_version 1.1;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        proxy_read_timeout 60;
        proxy_connect_timeout 60;
    }
}
```

---

## 문제 해결 가이드

### Nginx가 시작되지 않을 때

```bash
# 상태 확인
sudo systemctl status nginx

# 로그 확인
sudo tail -50 /var/log/nginx/error.log

# 설정 파일 문법 체크
sudo nginx -t

# 포트 충돌 확인
sudo lsof -i :80
sudo lsof -i :443
```

### SSL 인증서 발급 실패 시

```bash
# DNS 확인
nslookup api.ohgun.kr

# 포트 80 접근 확인
sudo netstat -tulpn | grep :80

# Certbot 로그 확인
sudo tail -f /var/log/letsencrypt/letsencrypt.log
```

### 리다이렉트 루프 발생 시

```bash
# 설정 파일 확인
sudo nginx -t

# X-Forwarded-Proto 헤더 확인
# proxy_set_header X-Forwarded-Proto $scheme; 가 있는지 확인
```

---

## 완료 체크리스트

- [ ] Nginx 설치 및 실행 확인
- [ ] HTTP 접속 테스트 (`http://api.ohgun.kr`)
- [ ] SSL 인증서 발급 완료
- [ ] HTTPS 접속 테스트 (`https://api.ohgun.kr`)
- [ ] HTTP → HTTPS 자동 리다이렉트 확인
- [ ] Swagger UI 정상 작동 확인

---

## 참고사항

- SSL 인증서는 90일마다 자동 갱신됨
- Certbot은 cron job으로 자동 갱신 설정됨
- 인증서 갱신 실패 시 이메일 알림 발송
- Docker 컨테이너는 계속 8080 포트로 실행 (변경 불필요)

