# GitHub Secrets 설정 가이드

## EC2_SSH_KEY 설정 방법

### 1. PEM 파일 내용 확인

EC2 인스턴스를 생성할 때 다운로드한 `.pem` 파일을 엽니다.

**예시 파일명:**
- `ohgun-keypair.pem`
- `my-ec2-key.pem`
- `aws-key.pem`

### 2. PEM 파일 전체 내용 복사

PEM 파일을 텍스트 에디터로 열어서 **전체 내용**을 복사합니다.

**PEM 파일 형식 예시:**
```
-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA...
(여러 줄의 암호화된 키 내용)
...
-----END RSA PRIVATE KEY-----
```

또는

```
-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC...
(여러 줄의 암호화된 키 내용)
...
-----END PRIVATE KEY-----
```

### 3. GitHub Secrets에 추가

1. 각 서브모듈 저장소로 이동:
   - `https://github.com/ohgun0325/ohgun-api/settings/secrets/actions`
   - `https://github.com/ohgun0325/ohgun-chat/settings/secrets/actions`
   - `https://github.com/ohgun0325/ohgun-vision/settings/secrets/actions`

2. **"New repository secret"** 클릭

3. **Name:** `EC2_SSH_KEY`

4. **Secret:** PEM 파일의 **전체 내용**을 붙여넣기
   - `-----BEGIN`부터 `-----END`까지 모든 줄 포함
   - 줄바꿈도 그대로 포함

5. **"Add secret"** 클릭

### 4. 주의사항

✅ **해야 할 것:**
- PEM 파일의 전체 내용을 복사 (줄바꿈 포함)
- `-----BEGIN`과 `-----END` 라인도 포함
- 각 서브모듈 저장소에 동일하게 설정

❌ **하지 말아야 할 것:**
- PEM 파일 경로만 입력 (예: `C:\Users\hi\key.pem`)
- 파일명만 입력 (예: `ohgun-keypair.pem`)
- 일부 내용만 복사

### 5. 다른 Secrets도 함께 설정

각 서브모듈 저장소에 다음 Secrets를 모두 추가하세요:

```
DOCKER_USERNAME: your-dockerhub-username
DOCKER_PASSWORD: your-dockerhub-password
EC2_HOST: 13.125.xxx.xxx (또는 ec2-xxx.ap-northeast-2.compute.amazonaws.com)
EC2_USERNAME: ec2-user (Amazon Linux) 또는 ubuntu (Ubuntu)
EC2_SSH_KEY: -----BEGIN RSA PRIVATE KEY-----\n...전체 내용...\n-----END RSA PRIVATE KEY-----
```

### 6. EC2_HOST 확인 방법

```bash
# EC2 콘솔에서 확인
# 또는 EC2 인스턴스에 SSH 접속 후
curl ifconfig.me
```

### 7. EC2_USERNAME 확인

- **Amazon Linux 2 / Amazon Linux 2023:** `ec2-user`
- **Ubuntu:** `ubuntu`
- **CentOS:** `centos`
- **RHEL:** `ec2-user`

### 8. 테스트

GitHub Actions 워크플로우를 실행한 후, "Deploy to EC2" 단계에서 오류가 발생하면:

1. EC2 Security Group에서 SSH 포트(22) 허용 확인
2. PEM 파일 내용이 올바르게 복사되었는지 확인
3. EC2_HOST가 올바른지 확인
4. EC2_USERNAME이 올바른지 확인

---

## 전체 Secrets 설정 체크리스트

각 서브모듈 저장소 (`ohgun-api`, `ohgun-chat`, `ohgun-vision`)에 대해:

- [ ] `DOCKER_USERNAME` 설정
- [ ] `DOCKER_PASSWORD` 설정
- [ ] `EC2_HOST` 설정
- [ ] `EC2_USERNAME` 설정
- [ ] `EC2_SSH_KEY` 설정 (PEM 파일 전체 내용)

