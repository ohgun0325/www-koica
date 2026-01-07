# Docker Hub 로그인 가이드

## 문제: PowerShell에서 패스워드 입력이 안 되는 경우

PowerShell에서 `docker login`을 실행할 때 패스워드 입력이 안 되는 경우가 있습니다.

## 해결 방법

### 방법 1: Personal Access Token (PAT) 사용 (권장)

Docker Hub는 이제 일반 패스워드 대신 **Personal Access Token (PAT)**을 사용하도록 권장합니다.

#### 1단계: PAT 생성

1. [Docker Hub](https://hub.docker.com/)에 로그인
2. 우측 상단 프로필 클릭 → **Account Settings**
3. **Security** 탭 클릭
4. **New Access Token** 클릭
5. Token 이름 입력 (예: `github-actions`)
6. **Read & Write** 권한 선택
7. **Generate** 클릭
8. **생성된 토큰을 복사** (한 번만 표시되므로 반드시 복사!)

#### 2단계: PAT로 로그인

```powershell
# 방법 1: 직접 입력
docker login -u ohgun0325
# Password: (PAT 토큰 붙여넣기)

# 방법 2: 파이프 사용
echo "YOUR_PAT_TOKEN" | docker login -u ohgun0325 --password-stdin
```

#### 3단계: GitHub Secrets에 PAT 설정

GitHub Secrets의 `DOCKER_PASSWORD`에 **일반 패스워드가 아닌 PAT 토큰**을 입력하세요.

```
DOCKER_USERNAME: ohgun0325
DOCKER_PASSWORD: dckr_pat_xxxxxxxxxxxxxxxxxxxx (PAT 토큰)
```

### 방법 2: --password-stdin 옵션 사용

```powershell
# PowerShell에서
$password = Read-Host -AsSecureString "Password"
$BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($password)
$plainPassword = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)
echo $plainPassword | docker login -u ohgun0325 --password-stdin
```

### 방법 3: 환경 변수 사용

```powershell
# 환경 변수로 설정
$env:DOCKER_PASSWORD = "YOUR_PAT_TOKEN"
docker login -u ohgun0325 --password-stdin < $env:DOCKER_PASSWORD
```

### 방법 4: 직접 명령어에 포함 (비권장, 테스트용)

```powershell
# 보안상 권장하지 않지만, 테스트용으로 사용 가능
docker login -u ohgun0325 -p "YOUR_PAT_TOKEN"
```

## GitHub Actions에서 사용

GitHub Secrets에 PAT를 설정하면 자동으로 사용됩니다:

```yaml
- name: Log in to Docker Hub
  uses: docker/login-action@v3
  with:
    username: ${{ secrets.DOCKER_USERNAME }}
    password: ${{ secrets.DOCKER_PASSWORD }}  # 여기에 PAT 토큰 입력
```

## 주의사항

✅ **권장:**
- Personal Access Token (PAT) 사용
- GitHub Secrets에 PAT 저장
- 토큰은 안전하게 보관

❌ **비권장:**
- 일반 패스워드를 GitHub Secrets에 저장
- 명령어에 패스워드 직접 입력
- 토큰을 코드에 하드코딩

## PAT 토큰 형식

Docker Hub PAT 토큰은 다음과 같은 형식입니다:

```
dckr_pat_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

- `dckr_pat_`로 시작
- 약 60자 정도의 문자열

## 로그인 확인

```powershell
# 로그인 상태 확인
docker info

# 또는
docker login --help
```

## 로그아웃

```powershell
docker logout
```

