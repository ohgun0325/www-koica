# Git 서브모듈 설정 가이드

이 문서는 기존 프로젝트의 폴더를 Git 서브모듈로 전환하는 과정을 단계별로 설명합니다.

## 📋 목차

1. [서브모듈이란?](#서브모듈이란)
2. [사전 준비사항](#사전-준비사항)
3. [전체 과정 개요](#전체-과정-개요)
4. [단계별 상세 가이드](#단계별-상세-가이드)
5. [문제 해결](#문제-해결)
6. [참고사항](#참고사항)

---

## 서브모듈이란?

Git 서브모듈은 하나의 Git 저장소 안에 다른 Git 저장소를 포함할 수 있게 해주는 기능입니다. 이를 통해:

- **독립적인 버전 관리**: 각 서브모듈은 독립적인 Git 저장소로 관리됩니다
- **모듈화**: 큰 프로젝트를 작은 모듈로 분리하여 관리할 수 있습니다
- **재사용성**: 여러 프로젝트에서 동일한 서브모듈을 재사용할 수 있습니다

### 프로젝트 구조

```
www-koica (메인 저장소)
├── api.ohgun.site (서브모듈 → ohgun-api 저장소)
├── vision.ohgun.site (서브모듈 → ohgun-vision 저장소)
└── chat.ohgun.site (서브모듈 → ohgun-chat 저장소)
```

---

## 사전 준비사항

### 1. GitHub 저장소 생성

각 서브모듈에 대한 별도의 GitHub 저장소가 필요합니다:

- ✅ `https://github.com/ohgun0325/ohgun-api.git`
- ✅ `https://github.com/ohgun0325/ohgun-vision.git`
- ✅ `https://github.com/ohgun0325/ohgun-chat.git`

### 2. 현재 상태 확인

- 메인 저장소: `https://github.com/ohgun0325/www-koica.git`
- 로컬에 `api.ohgun.site`, `vision.ohgun.site`, `chat.ohgun.site` 폴더가 존재
- 각 폴더가 독립적인 Git 저장소로 초기화되어 있음

---

## 전체 과정 개요

```
1단계: 각 서브모듈 저장소에 기존 파일 푸시
   ↓
2단계: 메인 저장소에서 기존 폴더를 Git 추적에서 제거
   ↓
3단계: 기존 폴더 삭제
   ↓
4단계: 서브모듈 추가
   ↓
5단계: 서브모듈 초기화
   ↓
6단계: 변경사항 커밋 및 푸시
```

---

## 단계별 상세 가이드

### 1단계: 각 서브모듈 저장소에 기존 파일 푸시

각 폴더로 이동하여 해당 GitHub 저장소에 파일을 푸시합니다.

#### API 서브모듈

```bash
cd api.ohgun.site

# 원격 저장소 확인
git remote -v

# 원격 저장소가 없다면 추가
git remote add origin https://github.com/ohgun0325/ohgun-api.git

# 브랜치 이름을 main으로 설정 (필요시)
git branch -M main

# 원격 저장소에 푸시
git push -u origin main

cd ..
```

#### Vision 서브모듈

```bash
cd vision.ohgun.site

git remote add origin https://github.com/ohgun0325/ohgun-vision.git
git branch -M main
git push -u origin main

cd ..
```

#### Chat 서브모듈

```bash
cd chat.ohgun.site

git remote add origin https://github.com/ohgun0325/ohgun-chat.git
git branch -M main
git push -u origin main

cd ..
```

#### 확인 방법

```bash
# 각 폴더에서 원격 저장소 확인
cd api.ohgun.site
git remote -v
cd ..

cd vision.ohgun.site
git remote -v
cd ..

cd chat.ohgun.site
git remote -v
cd ..
```

---

### 2단계: 메인 저장소에서 기존 폴더를 Git 추적에서 제거

메인 저장소(`www-koica`)에서 기존 폴더들을 Git 추적에서 제거합니다. **파일은 로컬에 그대로 유지됩니다.**

```bash
# 루트 디렉토리에서 실행
cd C:\Users\hi\Documents\classs\class

# Git 캐시에서 제거 (파일은 유지)
git rm -r --cached api.ohgun.site
git rm -r --cached vision.ohgun.site
git rm -r --cached chat.ohgun.site

# 변경사항 커밋
git commit -m "chore: 기존 폴더를 서브모듈로 전환하기 위해 제거"
```

#### 확인 방법

```bash
# Git 상태 확인
git status --short

# 결과 예시:
# D  api.ohgun.site/
# D  vision.ohgun.site/
# D  chat.ohgun.site/
```

---

### 3단계: 기존 폴더 삭제

기존 폴더를 삭제합니다. **이미 각 저장소에 푸시했으므로 안전합니다.**

#### PowerShell 사용 시

```powershell
# 루트 디렉토리에서 실행
Remove-Item -Recurse -Force api.ohgun.site
Remove-Item -Recurse -Force vision.ohgun.site
Remove-Item -Recurse -Force chat.ohgun.site
```

또는 짧게:

```powershell
rm -r -Force api.ohgun.site
rm -r -Force vision.ohgun.site
rm -r -Force chat.ohgun.site
```

#### CMD 사용 시

```bash
rmdir /s /q api.ohgun.site
rmdir /s /q vision.ohgun.site
rmdir /s /q chat.ohgun.site
```

#### 안전한 방법 (백업 후 삭제)

```bash
# 백업 (선택사항)
move api.ohgun.site api.ohgun.site.backup
move vision.ohgun.site vision.ohgun.site.backup
move chat.ohgun.site chat.ohgun.site.backup

# 나중에 서브모듈이 정상 작동하면 백업 폴더 삭제
rmdir /s /q api.ohgun.site.backup
rmdir /s /q vision.ohgun.site.backup
rmdir /s /q chat.ohgun.site.backup
```

#### 확인 방법

```bash
# 폴더 존재 여부 확인
Test-Path api.ohgun.site    # False여야 함
Test-Path vision.ohgun.site # False여야 함
Test-Path chat.ohgun.site   # False여야 함
```

---

### 4단계: 서브모듈 추가

메인 저장소에 서브모듈을 추가합니다.

```bash
# 루트 디렉토리에서 실행
git submodule add https://github.com/ohgun0325/ohgun-api.git api.ohgun.site
git submodule add https://github.com/ohgun0325/ohgun-vision.git vision.ohgun.site
git submodule add https://github.com/ohgun0325/ohgun-chat.git chat.ohgun.site
```

#### 명령어 형식

```
git submodule add <GitHub_저장소_URL> <로컬_폴더명>
```

- `<GitHub_저장소_URL>`: 각 서브모듈의 GitHub 저장소 URL
- `<로컬_폴더명>`: 프로젝트 내에서 사용할 폴더명

#### 실행 결과

각 명령어 실행 시 다음과 같은 출력이 나타납니다:

```
Cloning into 'C:/Users/hi/Documents/classs/class/api.ohgun.site'...
remote: Enumerating objects: XX, done.
remote: Counting objects: 100% (XX/XX), done.
remote: Compressing objects: 100% (XX/XX), done.
remote: Total XX (delta XX), reused XX (delta XX), pack-reused 0 (from 0)
Receiving objects: 100% (XX/XX), XX KiB | XX MiB/s, done.
Resolving deltas: 100% (XX/XX), done.
```

#### 생성되는 파일

- `.gitmodules`: 서브모듈 설정 파일이 자동으로 생성됩니다

---

### 5단계: 서브모듈 초기화

서브모듈을 초기화하고 업데이트합니다. (4단계에서 자동으로 되지만 확인 차원에서 실행)

```bash
git submodule update --init --recursive
```

#### 명령어 설명

- `--init`: 서브모듈 초기화
- `--recursive`: 중첩된 서브모듈도 포함

---

### 6단계: 변경사항 커밋 및 푸시

메인 저장소에 변경사항을 커밋하고 푸시합니다.

```bash
# .gitmodules와 서브모듈 폴더 추가
git add .gitmodules
git add api.ohgun.site vision.ohgun.site chat.ohgun.site

# 커밋
git commit -m "feat: api, vision, chat을 서브모듈로 추가"

# 푸시
git push origin main
```

#### 확인 방법

```bash
# .gitmodules 파일 확인
cat .gitmodules

# 서브모듈 상태 확인
git submodule status

# Git 상태 확인
git status
```

---

## 서브모듈 연결 확인

### 1. .gitmodules 파일 확인

```bash
cat .gitmodules
```

**예상 출력:**

```ini
[submodule "api.ohgun.site"]
	path = api.ohgun.site
	url = https://github.com/ohgun0325/ohgun-api.git
[submodule "vision.ohgun.site"]
	path = vision.ohgun.site
	url = https://github.com/ohgun0325/ohgun-vision.git
[submodule "chat.ohgun.site"]
	path = chat.ohgun.site
	url = https://github.com/ohgun0325/ohgun-chat.git
```

### 2. 서브모듈 상태 확인

```bash
git submodule status
```

**예상 출력:**

```
 b9f60dcacdd4e683866fa6c697b88224670f436f api.ohgun.site (heads/main)
 3fa6d88952c213da3e74dc0206417275730d4605 chat.ohgun.site (heads/main)
 88f93da0d895aae0d4c581b5bc190e77c0997c3b vision.ohgun.site (heads/main)
```

### 3. VS Code에서 확인

- 서브모듈 폴더 옆에 **'S' 아이콘**이 표시됩니다
- `.gitmodules` 파일이 생성됩니다

---

## 문제 해결

### 문제 1: PowerShell에서 `rmdir /s /q` 오류

**오류 메시지:**
```
Remove-Item : '/q' 인수를 허용하는 위치 매개 변수를 찾을 수 없습니다.
```

**원인:** PowerShell에서는 CMD 명령어 옵션이 작동하지 않습니다.

**해결 방법:**

```powershell
# PowerShell 명령어 사용
Remove-Item -Recurse -Force api.ohgun.site

# 또는 CMD를 직접 호출
cmd /c rmdir /s /q api.ohgun.site
```

### 문제 2: 서브모듈 추가 시 "already exists" 오류

**오류 메시지:**
```
'api.ohgun.site' already exists in the index
```

**원인:** 기존 폴더가 Git 추적에서 완전히 제거되지 않았습니다.

**해결 방법:**

```bash
# Git 캐시에서 완전히 제거
git rm -r --cached api.ohgun.site
git commit -m "Remove api.ohgun.site from index"

# 폴더 삭제
Remove-Item -Recurse -Force api.ohgun.site

# 서브모듈 다시 추가
git submodule add https://github.com/ohgun0325/ohgun-api.git api.ohgun.site
```

### 문제 3: 서브모듈이 비어있음

**증상:** 서브모듈 폴더가 비어있거나 파일이 없습니다.

**해결 방법:**

```bash
# 서브모듈 초기화 및 업데이트
git submodule update --init --recursive

# 특정 서브모듈만 초기화
git submodule update --init api.ohgun.site
```

### 문제 4: 서브모듈 수정 후 메인 저장소에 반영 안 됨

**원인:** 서브모듈 내부에서 변경사항을 커밋하고 푸시한 후, 메인 저장소에서 서브모듈의 새로운 커밋을 참조하도록 업데이트해야 합니다.

**해결 방법:**

```bash
# 서브모듈 내부에서 변경사항 커밋 및 푸시
cd api.ohgun.site
git add .
git commit -m "Update files"
git push origin main
cd ..

# 메인 저장소에서 서브모듈 참조 업데이트
git add api.ohgun.site
git commit -m "Update api.ohgun.site submodule"
git push origin main
```

---

## 서브모듈 사용 방법

### 서브모듈 클론하기

다른 개발자가 프로젝트를 클론할 때:

```bash
# 서브모듈 포함하여 클론
git clone --recursive https://github.com/ohgun0325/www-koica.git

# 또는 클론 후 서브모듈 초기화
git clone https://github.com/ohgun0325/www-koica.git
cd www-koica
git submodule update --init --recursive
```

### 서브모듈 업데이트하기

```bash
# 모든 서브모듈 업데이트
git submodule update --remote

# 특정 서브모듈만 업데이트
git submodule update --remote api.ohgun.site
```

### 서브모듈 내부 작업하기

```bash
# 서브모듈로 이동
cd api.ohgun.site

# 일반적인 Git 작업 수행
git checkout -b feature-branch
git add .
git commit -m "Add new feature"
git push origin feature-branch

# 메인 저장소로 돌아가기
cd ..

# 서브모듈 변경사항 반영
git add api.ohgun.site
git commit -m "Update api.ohgun.site to latest"
```

---

## 참고사항

### 서브모듈의 장점

1. **독립적인 버전 관리**: 각 모듈이 독립적으로 버전 관리됨
2. **모듈화**: 큰 프로젝트를 작은 단위로 분리
3. **재사용성**: 여러 프로젝트에서 동일한 모듈 재사용 가능
4. **명확한 의존성**: 메인 저장소에서 특정 커밋을 참조하여 안정성 확보

### 서브모듈의 단점

1. **복잡성**: 일반 Git 작업보다 복잡함
2. **동기화 필요**: 서브모듈 변경 시 메인 저장소도 업데이트 필요
3. **클론 시 주의**: `--recursive` 옵션 필요

### 주의사항

1. **서브모듈은 특정 커밋을 참조**: 항상 최신 버전이 아닌 특정 커밋을 참조합니다
2. **변경사항 반영**: 서브모듈 내부에서 변경 후 메인 저장소에도 커밋해야 합니다
3. **팀 협업**: 팀원들이 서브모듈 사용법을 이해해야 합니다

---

## 요약

### 전체 명령어 순서 (한 번에 실행)

```bash
# 1단계: 각 서브모듈 저장소에 푸시 (각 폴더에서 실행)
cd api.ohgun.site && git remote add origin https://github.com/ohgun0325/ohgun-api.git && git push -u origin main && cd ..
cd vision.ohgun.site && git remote add origin https://github.com/ohgun0325/ohgun-vision.git && git push -u origin main && cd ..
cd chat.ohgun.site && git remote add origin https://github.com/ohgun0325/ohgun-chat.git && git push -u origin main && cd ..

# 2단계: 메인 저장소에서 제거
git rm -r --cached api.ohgun.site vision.ohgun.site chat.ohgun.site
git commit -m "chore: 기존 폴더를 서브모듈로 전환하기 위해 제거"

# 3단계: 폴더 삭제 (PowerShell)
Remove-Item -Recurse -Force api.ohgun.site, vision.ohgun.site, chat.ohgun.site

# 4단계: 서브모듈 추가
git submodule add https://github.com/ohgun0325/ohgun-api.git api.ohgun.site
git submodule add https://github.com/ohgun0325/ohgun-vision.git vision.ohgun.site
git submodule add https://github.com/ohgun0325/ohgun-chat.git chat.ohgun.site

# 5단계: 서브모듈 초기화
git submodule update --init --recursive

# 6단계: 커밋 및 푸시
git add .gitmodules api.ohgun.site vision.ohgun.site chat.ohgun.site
git commit -m "feat: api, vision, chat을 서브모듈로 추가"
git push origin main
```

---

## 작성일

- 작성일: 2025-01-XX
- 프로젝트: www-koica
- 서브모듈: ohgun-api, ohgun-vision, ohgun-chat

---

## 추가 자료

- [Git 공식 문서 - 서브모듈](https://git-scm.com/book/en/v2/Git-Tools-Submodules)
- [Git 서브모듈 완전 가이드](https://www.atlassian.com/git/tutorials/git-submodule)

