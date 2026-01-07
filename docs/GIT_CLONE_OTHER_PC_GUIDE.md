# 다른 PC에서 프로젝트 가져오기 가이드

다른 PC에서 프로젝트를 처음 클론하거나 최신 변경사항을 가져오는 방법을 설명합니다.

## 📋 목차

1. [처음 클론하기](#처음-클론하기)
2. [기존 프로젝트 업데이트하기](#기존-프로젝트-업데이트하기)
3. [서브모듈 관리](#서브모듈-관리)
4. [문제 해결](#문제-해결)
5. [빠른 참조](#빠른-참조)

---

## 처음 클론하기

### 프로젝트 구조

이 프로젝트는 **Git 서브모듈**을 사용합니다:

```
class (메인 저장소)
├── api.ohgun.site (서브모듈 → ohgun-api 저장소)
├── vision.ohgun.site (서브모듈 → ohgun-vision 저장소)
└── chat.ohgun.site (서브모듈 → ohgun-chat 저장소)
```

### 방법 1: 서브모듈 포함하여 클론 (권장)

```bash
# 메인 저장소와 모든 서브모듈을 한 번에 클론
git clone --recurse-submodules https://github.com/ohgun0325/www-koica.git

# 또는 짧은 버전
git clone --recursive https://github.com/ohgun0325/www-koica.git
```

**결과**:
- 메인 저장소 클론
- 모든 서브모듈 자동 클론
- 각 서브모듈이 최신 커밋으로 체크아웃됨

### 방법 2: 단계별 클론

```bash
# 1. 메인 저장소만 클론
git clone https://github.com/ohgun0325/www-koica.git
cd www-koica

# 2. 서브모듈 초기화 및 클론
git submodule init
git submodule update

# 또는 한 번에
git submodule update --init --recursive
```

### 방법 3: 서브모듈 없이 클론 후 나중에 추가

```bash
# 1. 메인 저장소만 클론
git clone https://github.com/ohgun0325/www-koica.git
cd www-koica

# 2. 나중에 서브모듈이 필요할 때
git submodule update --init --recursive
```

---

## 기존 프로젝트 업데이트하기

### 메인 저장소 업데이트

```bash
# 현재 디렉토리로 이동
cd /path/to/www-koica

# 최신 변경사항 가져오기
git pull origin main
```

### 서브모듈 포함하여 업데이트 (권장)

```bash
# 메인 저장소와 모든 서브모듈을 한 번에 업데이트
git pull --recurse-submodules origin main

# 또는
git pull origin main
git submodule update --remote --recursive
```

### 서브모듈만 업데이트

```bash
# 모든 서브모듈을 최신 버전으로 업데이트
git submodule update --remote --recursive

# 특정 서브모듈만 업데이트
cd api.ohgun.site
git pull origin main
cd ..
```

---

## 서브모듈 관리

### 서브모듈 상태 확인

```bash
# 서브모듈 상태 확인
git submodule status

# 상세 정보 확인
git submodule foreach 'git status'
```

**예상 출력**:
```
 a1b2c3d api.ohgun.site (v1.0.0)
 e4f5g6h vision.ohgun.site (v1.0.0)
 i7j8k9l chat.ohgun.site (v1.0.0)
```

### 서브모듈에서 작업하기

#### 1. 서브모듈로 이동

```bash
cd api.ohgun.site
```

#### 2. 서브모듈에서 변경사항 확인

```bash
# 서브모듈 내부에서
git status
git log --oneline -5
```

#### 3. 서브모듈에서 커밋 및 푸시

```bash
# 서브모듈 내부에서
git add .
git commit -m "변경사항"
git push origin main
```

#### 4. 메인 저장소에서 서브모듈 변경사항 반영

```bash
# 메인 저장소로 돌아가기
cd ..

# 서브모듈 변경사항을 메인 저장소에 반영
git add api.ohgun.site
git commit -m "Update api.ohgun.site submodule"
git push origin main
```

### 서브모듈 브랜치 변경

```bash
# 서브모듈의 특정 브랜치로 전환
cd api.ohgun.site
git checkout develop
cd ..

# 메인 저장소에 반영
git add api.ohgun.site
git commit -m "Switch api.ohgun.site to develop branch"
```

---

## 문제 해결

### 문제 1: 서브모듈이 비어있음

**증상**:
```
api.ohgun.site/ (빈 폴더)
```

**해결**:
```bash
# 서브모듈 초기화 및 클론
git submodule update --init --recursive
```

### 문제 2: 서브모듈 업데이트 후 충돌

**증상**:
```
fatal: refusing to merge unrelated histories
```

**해결**:
```bash
# 서브모듈 내부에서
cd api.ohgun.site
git pull origin main --allow-unrelated-histories
```

### 문제 3: 서브모듈이 최신 버전이 아님

**증상**: 서브모듈이 오래된 커밋을 가리키고 있음

**해결**:
```bash
# 모든 서브모듈을 최신으로 업데이트
git submodule update --remote --recursive

# 또는 특정 서브모듈만
cd api.ohgun.site
git checkout main
git pull origin main
cd ..
git add api.ohgun.site
git commit -m "Update api.ohgun.site to latest"
```

### 문제 4: 서브모듈 삭제 후 다시 추가

**증상**: 서브모듈 폴더가 삭제되었거나 손상됨

**해결**:
```bash
# 서브모듈 완전히 제거
git submodule deinit -f api.ohgun.site
git rm -f api.ohgun.site
rm -rf .git/modules/api.ohgun.site

# 다시 추가
git submodule add https://github.com/ohgun0325/ohgun-api.git api.ohgun.site
git submodule update --init --recursive
```

### 문제 5: 권한 오류 (Private 저장소)

**증상**:
```
Permission denied (publickey)
```

**해결**:
1. SSH 키 설정 확인
2. GitHub에 SSH 키 등록
3. 또는 HTTPS 사용 (Personal Access Token 필요)

```bash
# HTTPS로 클론 (토큰 필요)
git clone https://YOUR_TOKEN@github.com/ohgun0325/www-koica.git
```

---

## 빠른 참조

### 자주 사용하는 명령어

```bash
# 처음 클론
git clone --recurse-submodules https://github.com/ohgun0325/www-koica.git

# 업데이트
git pull --recurse-submodules origin main

# 서브모듈 상태 확인
git submodule status

# 서브모듈 업데이트
git submodule update --remote --recursive

# 서브모듈에서 작업
cd api.ohgun.site
git pull origin main
cd ..
git add api.ohgun.site
git commit -m "Update submodule"
```

### Git 설정 (처음 한 번만)

```bash
# 사용자 정보 설정
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# 서브모듈 자동 업데이트 설정 (선택사항)
git config --global submodule.recurse true
```

이 설정을 하면 `git pull` 시 서브모듈도 자동으로 업데이트됩니다.

---

## 시나리오별 가이드

### 시나리오 1: 새로운 PC에서 처음 시작

```bash
# 1. 프로젝트 클론
git clone --recurse-submodules https://github.com/ohgun0325/www-koica.git
cd www-koica

# 2. 환경 변수 설정 (필요한 경우)
cp .env.example .env
vim .env

# 3. 완료!
```

### 시나리오 2: 기존 PC에서 최신 변경사항 가져오기

```bash
# 1. 프로젝트 디렉토리로 이동
cd /path/to/www-koica

# 2. 최신 변경사항 가져오기
git pull --recurse-submodules origin main

# 3. 완료!
```

### 시나리오 3: 특정 서브모듈만 업데이트

```bash
# 1. 특정 서브모듈로 이동
cd api.ohgun.site

# 2. 최신 변경사항 가져오기
git pull origin main

# 3. 메인 저장소로 돌아가기
cd ..

# 4. 변경사항 반영 (선택사항)
git add api.ohgun.site
git commit -m "Update api.ohgun.site"
```

### 시나리오 4: 서브모듈에서 작업 후 푸시

```bash
# 1. 서브모듈로 이동
cd api.ohgun.site

# 2. 변경사항 커밋
git add .
git commit -m "기능 추가"
git push origin main

# 3. 메인 저장소로 돌아가기
cd ..

# 4. 서브모듈 변경사항 반영
git add api.ohgun.site
git commit -m "Update api.ohgun.site submodule"
git push origin main
```

---

## 주의사항

### 1. 서브모듈은 독립적인 저장소

- 각 서브모듈은 독립적인 Git 저장소입니다
- 서브모듈에서 변경사항을 커밋하려면 서브모듈 내부에서 커밋해야 합니다
- 메인 저장소는 서브모듈의 특정 커밋을 가리키고 있습니다

### 2. 서브모듈 업데이트 시 주의

- 서브모듈을 업데이트하면 메인 저장소에도 반영해야 합니다
- 팀원들과 서브모듈 버전을 동기화해야 합니다

### 3. 배포와의 관계

- GitHub Actions는 각 서브모듈의 저장소에서 독립적으로 실행됩니다
- `api.ohgun.site` 서브모듈에 푸시하면 해당 저장소의 GitHub Actions가 실행됩니다
- 메인 저장소에 푸시해도 서브모듈의 GitHub Actions는 실행되지 않습니다

---

## 체크리스트

### 처음 클론 시

- [ ] Git 설치 확인 (`git --version`)
- [ ] 저장소 클론 (`git clone --recurse-submodules`)
- [ ] 서브모듈 상태 확인 (`git submodule status`)
- [ ] 환경 변수 설정 (필요한 경우)

### 업데이트 시

- [ ] 메인 저장소 업데이트 (`git pull`)
- [ ] 서브모듈 업데이트 (`git submodule update`)
- [ ] 변경사항 확인 (`git status`)

### 작업 시

- [ ] 올바른 저장소에서 작업하는지 확인
- [ ] 서브모듈 변경사항은 서브모듈에서 커밋
- [ ] 메인 저장소 변경사항은 메인 저장소에서 커밋

---

## 참고 문서

- [Git 서브모듈 설정 가이드](./GIT_SUBMODULE_SETUP_GUIDE.md)
- [GitHub Actions 자동 배포 가이드](./GITHUB_ACTIONS_AUTOMATIC_DEPLOYMENT.md)
- [공식 Git 서브모듈 문서](https://git-scm.com/book/en/v2/Git-Tools-Submodules)

---

## 요약

### 다른 PC에서 처음 클론

```bash
git clone --recurse-submodules https://github.com/ohgun0325/www-koica.git
cd www-koica
```

### 기존 프로젝트 업데이트

```bash
git pull --recurse-submodules origin main
```

### 서브모듈만 업데이트

```bash
git submodule update --remote --recursive
```

**이제 다른 PC에서도 쉽게 프로젝트를 가져올 수 있습니다! 🚀**

