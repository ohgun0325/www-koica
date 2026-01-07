# EC2 서버 재시작 가이드

## ⚠️ 중요: 인스턴스 중지/시작은 필요 없습니다!

**인스턴스를 중지(Stop)했다가 시작(Start)하면:**
- Elastic IP가 설정되지 않은 경우 **Public IP 주소가 변경**됩니다
- 도메인 설정이 깨질 수 있습니다
- 불필요한 다운타임이 발생합니다

**권장 방법**: Docker 컨테이너만 재시작하거나 EC2 인스턴스를 재시작(Reboot)하세요.

---

## 방법 1: Docker 컨테이너만 재시작 (가장 빠름) ⭐ 권장

### 1-1. 단일 컨테이너 재시작

```bash
# EC2에 SSH 접속 후

# 컨테이너 재시작
docker restart ohgun-api

# 또는
docker stop ohgun-api
docker start ohgun-api
```

**장점**:
- 가장 빠름 (수초 내 완료)
- IP 주소 변경 없음
- 다른 서비스에 영향 없음

**단점**:
- 설정 파일 변경 시 새 이미지 필요

### 1-2. Docker Compose로 재시작

```bash
cd /opt/ohgun-api

# 컨테이너 재시작
docker-compose restart

# 또는 특정 서비스만 재시작
docker-compose restart api
```

---

## 방법 2: 새 이미지 Pull 후 재시작 (설정 변경 시)

### 2-1. 새 이미지 Pull

```bash
cd /opt/ohgun-api

# 최신 이미지 다운로드
docker pull ohgun0325/ohgun-api:latest
```

### 2-2. 컨테이너 재생성

```bash
# 기존 컨테이너 중지 및 제거
docker-compose down

# 새 이미지로 컨테이너 재생성 및 시작
docker-compose up -d
```

**또는 단일 명령어로:**

```bash
# 기존 컨테이너 중지 및 제거
docker stop ohgun-api
docker rm ohgun-api

# 새 이미지로 컨테이너 실행
docker run -d \
  --name ohgun-api \
  -p 8080:8080 \
  --env-file .env \
  --restart unless-stopped \
  ohgun0325/ohgun-api:latest
```

---

## 방법 3: EC2 인스턴스 재시작 (Reboot) ✅ 안전

### 3-1. AWS 콘솔에서 재시작

1. AWS 콘솔 → EC2 → Instances
2. `ohgunapi` 인스턴스 선택
3. "Instance state" → "Reboot instance" 클릭
4. 확인

**장점**:
- IP 주소 유지 (Elastic IP 사용 시)
- Docker 서비스 자동 재시작 (`restart: unless-stopped` 설정 시)
- 시스템 레벨 재시작

**단점**:
- 약 1-2분 소요
- 모든 서비스 재시작

### 3-2. SSH에서 재시작

```bash
# EC2에 SSH 접속 후

# 재시작
sudo reboot

# 또는
sudo shutdown -r now
```

**주의**: SSH 연결이 끊어집니다. 1-2분 후 다시 접속하세요.

---

## 방법 4: EC2 인스턴스 중지/시작 ⚠️ 비권장

### 4-1. AWS 콘솔에서 중지/시작

1. AWS 콘솔 → EC2 → Instances
2. `ohgunapi` 인스턴스 선택
3. "Instance state" → "Stop instance" 클릭
4. 완료 후 "Start instance" 클릭

**주의사항**:
- ❌ Elastic IP가 없으면 **Public IP 주소가 변경**됩니다
- ❌ 도메인 설정(`api.ohgun.kr`)이 깨질 수 있습니다
- ❌ 다운타임이 길어집니다 (5-10분)

**Elastic IP 설정 확인**:
- EC2 → Elastic IPs 메뉴에서 확인
- 인스턴스에 연결되어 있는지 확인

---

## 현재 상황에 맞는 재시작 방법

### 상황: Gateway 설정 파일 수정 (`application.yaml`)

**필요한 작업**:

1. **코드 변경사항 커밋 및 푸시**
   ```bash
   git add api.ohgun.site/gateway/src/main/resources/application.yaml
   git commit -m "fix: update Gateway routing to use api service"
   git push origin main
   ```

2. **GitHub Actions로 새 이미지 빌드 대기**
   - GitHub Actions 페이지에서 빌드 완료 확인
   - Docker Hub에서 새 이미지 확인

3. **EC2에서 새 이미지 Pull 및 재시작**
   ```bash
   cd /opt/ohgun-api
   docker pull ohgun0325/ohgun-api:latest
   docker-compose down
   docker-compose up -d
   ```

4. **로그 확인**
   ```bash
   docker logs -f ohgun-api
   ```

---

## 빠른 체크리스트

### 재시작 전 확인

- [ ] 변경사항이 GitHub에 푸시되었는가?
- [ ] GitHub Actions 빌드가 완료되었는가?
- [ ] Docker Hub에 새 이미지가 업로드되었는가?

### 재시작 후 확인

- [ ] 컨테이너가 실행 중인가?
  ```bash
  docker ps | grep ohgun-api
  ```

- [ ] 애플리케이션이 정상 시작되었는가?
  ```bash
  docker logs ohgun-api --tail 50
  ```

- [ ] 헬스 체크가 성공하는가?
  ```bash
  curl http://localhost:8080/actuator/health
  ```

- [ ] 외부에서 접근 가능한가?
  ```bash
  # 로컬에서 테스트
  curl https://api.ohgun.kr/oauth/naver/login-url
  ```

---

## 각 방법 비교

| 방법 | 소요 시간 | IP 변경 | 다운타임 | 권장 상황 |
|------|----------|---------|----------|----------|
| 컨테이너 재시작 | 5-10초 | ❌ | 최소 | 빠른 재시작 필요 |
| 새 이미지 Pull | 1-2분 | ❌ | 10-30초 | 설정 변경 시 |
| 인스턴스 Reboot | 1-2분 | ❌* | 1-2분 | 시스템 레벨 재시작 |
| 인스턴스 Stop/Start | 5-10분 | ⚠️ | 5-10분 | 비권장 |

*Elastic IP 사용 시 IP 유지

---

## 문제 해결

### 컨테이너가 재시작되지 않는 경우

```bash
# 컨테이너 상태 확인
docker ps -a | grep ohgun-api

# 강제 재시작
docker restart ohgun-api

# 로그 확인
docker logs ohgun-api --tail 100
```

### 새 이미지가 적용되지 않는 경우

```bash
# 기존 이미지 제거
docker rmi ohgun0325/ohgun-api:latest

# 새 이미지 Pull
docker pull ohgun0325/ohgun-api:latest

# 컨테이너 재생성
docker-compose down
docker-compose up -d
```

### 포트가 이미 사용 중인 경우

```bash
# 포트 사용 확인
sudo netstat -tlnp | grep 8080

# 기존 컨테이너 완전히 제거
docker-compose down
docker rm -f ohgun-api

# 재시작
docker-compose up -d
```

---

## 권장 워크플로우

### 일반적인 재시작

```bash
# 1. 컨테이너 재시작 (가장 빠름)
docker restart ohgun-api

# 2. 로그 확인
docker logs -f ohgun-api
```

### 설정 변경 후 재시작

```bash
# 1. 새 이미지 Pull
cd /opt/ohgun-api
docker pull ohgun0325/ohgun-api:latest

# 2. 컨테이너 재생성
docker-compose down
docker-compose up -d

# 3. 로그 확인
docker logs -f ohgun-api
```

### 시스템 레벨 재시작 필요 시

```bash
# AWS 콘솔에서 "Reboot instance" 사용
# 또는
sudo reboot
```

---

## 결론

**가장 빠르고 안전한 방법**:
1. Docker 컨테이너만 재시작 (`docker restart ohgun-api`)
2. 설정 변경 시: 새 이미지 Pull 후 재생성

**절대 하지 말아야 할 것**:
- ❌ 인스턴스 중지/시작 (IP 변경 위험)
- ❌ Elastic IP 없이 인스턴스 재시작

**현재 상황 (Gateway 설정 변경)**:
1. 코드 푸시 → GitHub Actions 빌드
2. EC2에서 새 이미지 Pull
3. 컨테이너 재생성 (`docker-compose down && docker-compose up -d`)

