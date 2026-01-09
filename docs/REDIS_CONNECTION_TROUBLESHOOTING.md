# Redis 연결 오류 해결 가이드

## 현재 상황

- `application.yaml`에서 `spring.redis.*` 설정 완료
- 여전히 `Unable to connect to Redis` 에러 발생

---

## 확인해야 할 사항

### 1. 배포가 완료되었는지 확인

#### GitHub Actions 확인
1. GitHub 저장소 → **Actions** 탭
2. 최신 워크플로우가 ✅ 완료되었는지 확인
3. **빌드 시간** 확인 (최근 몇 분 내에 완료되었는지)

#### EC2에서 확인
```bash
# 컨테이너가 최근에 재시작되었는지 확인
docker ps | grep ohgun-api

# 이미지가 최근에 pull되었는지 확인
docker images | grep ohgun-api
```

---

### 2. 컨테이너 내부 설정 확인

```bash
# 컨테이너 내부에서 application.yaml 확인
docker exec ohgun-api cat /app/application.yaml | grep -A 10 redis

# 또는 JAR 파일 내부 확인
docker exec ohgun-api jar -tf /app/app.jar | grep application.yaml
```

**예상 출력:**
```yaml
redis:
  host: ${UPSTASH_REDIS_HOST}
  port: ${UPSTASH_REDIS_PORT}
  password: ${UPSTASH_REDIS_PASSWORD}
  ssl:
    enabled: true
```

---

### 3. 환경 변수 확인

```bash
# 컨테이너 내부 환경 변수 확인
docker exec ohgun-api printenv | grep UPSTASH

# 예상 출력:
# UPSTASH_REDIS_HOST=ample-puma-6304.upstash.io
# UPSTASH_REDIS_PORT=6379
# UPSTASH_REDIS_PASSWORD=ARigAAImcDFhNWZ1OTg4M2JjNmI0NTQ1YmRhYmFlMGRjZjkxNWM2YXAxNjMwNA
```

**문제 발견 시:**
- 환경 변수가 없으면 → EC2 `.env` 파일 확인
- 환경 변수가 있으면 → 다음 단계로

---

### 4. Redis 연결 테스트

#### 컨테이너 내부에서 직접 테스트
```bash
# 컨테이너 내부에서 Redis 연결 테스트
docker exec ohgun-api sh -c "
  apk add --no-cache redis 2>/dev/null || apt-get update && apt-get install -y redis-tools 2>/dev/null || true
  redis-cli -h \$UPSTASH_REDIS_HOST -p \$UPSTASH_REDIS_PORT -a \$UPSTASH_REDIS_PASSWORD --tls ping
"
```

**성공 시:**
```
PONG
```

**실패 시:**
- SSL/TLS 에러 → SSL 설정 문제
- Connection refused → 네트워크/방화벽 문제
- Authentication failed → 비밀번호 문제

---

### 5. Spring Boot 로그 확인

```bash
# Redis 관련 로그만 필터링
docker logs ohgun-api --tail 500 | grep -i redis

# 전체 로그 확인
docker logs ohgun-api --tail 500
```

**확인할 내용:**
- `LettuceConnectionFactory` 초기화 메시지
- Redis 연결 시도 로그
- 구체적인 에러 메시지

---

## 가능한 원인 및 해결

### 원인 1: 배포가 아직 완료되지 않음

**증상:**
- GitHub Actions가 아직 실행 중
- EC2 컨테이너가 오래된 이미지 사용

**해결:**
- GitHub Actions 완료 대기
- 또는 EC2에서 수동으로 새 이미지 pull 및 재시작

---

### 원인 2: SSL 설정 문제

**증상:**
- `SSLHandshakeException` 또는 `javax.net.ssl.SSLException`

**해결:**
`application.yaml`에서 SSL 설정 확인:
```yaml
spring:
  redis:
    ssl:
      enabled: true
```

---

### 원인 3: 네트워크/방화벽 문제

**증상:**
- `Connection timed out` 또는 `Connection refused`

**해결:**
- EC2 Security Group에서 **아웃바운드 규칙** 확인
- Upstash Redis 엔드포인트로의 **아웃바운드 트래픽 허용** 확인

---

### 원인 4: 비밀번호 문제

**증상:**
- `Authentication failed` 또는 `NOAUTH`

**해결:**
- `UPSTASH_REDIS_PASSWORD`가 **TCP 비밀번호**인지 확인 (REST TOKEN 아님)
- Upstash 콘솔에서 **Connection URL** 확인:
  ```
  rediss://:PASSWORD@HOST:6379
  ```
  여기서 `PASSWORD` 부분이 `UPSTASH_REDIS_PASSWORD` 값

---

## 빠른 해결 방법

### 방법 1: 컨테이너 강제 재시작

```bash
# EC2에서
cd /opt/ohgun-api

docker stop ohgun-api
docker rm ohgun-api

# 최신 이미지 pull
docker pull ohgun0325/ohgun-api:latest

# 새 컨테이너 실행
docker run -d \
  --name ohgun-api \
  -p 8080:8080 \
  --env-file /opt/ohgun-api/.env \
  --restart unless-stopped \
  ohgun0325/ohgun-api:latest

# 로그 확인
docker logs -f ohgun-api
```

---

### 방법 2: 로그 레벨 상향

`application.yaml`에 추가:
```yaml
logging:
  level:
    org.springframework.data.redis: DEBUG
    io.lettuce.core: DEBUG
```

이렇게 하면 Redis 연결 시도 과정을 상세히 볼 수 있습니다.

---

## 체크리스트

- [ ] GitHub Actions 배포 완료 확인
- [ ] EC2 컨테이너 재시작 확인
- [ ] 환경 변수 (`UPSTASH_REDIS_*`) 확인
- [ ] `application.yaml`의 `spring.redis.*` 설정 확인
- [ ] Redis 연결 테스트 (`redis-cli --tls ping`)
- [ ] Spring Boot 로그에서 구체적인 에러 메시지 확인
- [ ] EC2 Security Group 아웃바운드 규칙 확인

---

## 다음 단계

위 체크리스트를 모두 확인한 후에도 문제가 지속되면:

1. **전체 로그** (`docker logs ohgun-api --tail 500`) 공유
2. **환경 변수** (`docker exec ohgun-api printenv | grep UPSTASH`) 공유
3. **Redis 연결 테스트 결과** 공유

이 정보를 바탕으로 정확한 원인을 파악할 수 있습니다.

