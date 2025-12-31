# OAuth Service + Neon DB ?˜ê²½ ?¤ì • ê°€?´ë“œ

## ?“‹ ê°œìš”

OAuth Service??`/oauth/**` ê²½ë¡œë¡?ì§ì ‘ ?‘ê·¼?˜ë©°, Neon PostgreSQL???¬ìš©?©ë‹ˆ??

### ì£¼ìš” ë³€ê²??¬í•­

1. **ê²½ë¡œ ?¨ìˆœ??*: `/api/oauth/**` ??`/oauth/**`
2. **Neon DB ?°ë™**: ë¡œì»¬ DB ?€??Neon PostgreSQL ?¬ìš©
3. **Gateway ?¼ìš°??*: `http://localhost:8080/oauth/**` ??`oauth:8080/oauth/**`

---

## ?”§ .env ?Œì¼ ?¤ì •

?„ë¡œ?íŠ¸ ë£¨íŠ¸??`.env` ?Œì¼???ì„±?˜ê³  ?„ë˜ ?´ìš©??ì¶”ê??˜ì„¸??

```bash
# ========================================
# Neon PostgreSQL ?°ê²° ?•ë³´
# ========================================
NEON_DB_HOST=ep-withered-pond-a11avi67.ap-southeast-1.aws.neon.tech
NEON_DB_NAME=ohgundb
NEON_DB_USER=neondb_owner
NEON_DB_PASSWORD=?¤ì œ_?¤ì˜¨_ë¹„ë?ë²ˆí˜¸

# ========================================
# Upstash Redis (Gateway??
# ========================================
UPSTASH_REDIS_HOST=awaited-insect-5667.upstash.io
UPSTASH_REDIS_PORT=6379
UPSTASH_REDIS_PASSWORD=?¤ì œ_?…ìŠ¤?œì‹œ_ë¹„ë?ë²ˆí˜¸

# ========================================
# ?¤ì´ë²?OAuth ?¤ì •
# ========================================
NAVER_CLIENT_ID=CRd0KSYwlBXwo1GmcmKW
NAVER_CLIENT_SECRET=?¤ì œ_?¤ì´ë²??´ë¼?´ì–¸???œí¬ë¦?
NAVER_REDIRECT_URI=http://localhost:8080/oauth/naver/callback

# ========================================
# JWT ?¤ì •
# ========================================
JWT_SECRET=?¤ì œë¡?ì¶©ë¶„??ê¸??œë¤_ë¬¸ì??ìµœì†Œ_32???´ìƒ

# ========================================
# Spring ?¤ì •
# ========================================
SPRING_PROFILES_ACTIVE=neon
JPA_DDL_AUTO=validate
JPA_SHOW_SQL=false

# ========================================
# Redis (ë¡œì»¬ ê°œë°œ??
# ========================================
REDIS_PASSWORD=Redis0930!
```

---

## ?Œ ?¤ì´ë²?ê°œë°œ??ì½˜ì†” ?¤ì •

### 1. ?¤ì´ë²?ê°œë°œ?ì„¼???‘ì†
- URL: https://developers.naver.com/apps/#/myapps

### 2. ? í”Œë¦¬ì??´ì…˜ ?¤ì •

#### ?œë¹„??URL
```
http://localhost:3000
```

#### Callback URL (ì¤‘ìš”!)
```
http://localhost:8080/oauth/naver/callback
```

? ï¸ **ì£¼ì˜**: `/api` ?†ì´ `/oauth/naver/callback`ë¡??¤ì •?´ì•¼ ?©ë‹ˆ??

---

## ?—„ï¸?Neon DB ?¤í‚¤ë§??¤ì •

### 1. Neon Console ?‘ì†
- URL: https://console.neon.tech
- ?„ë¡œ?íŠ¸: `aifix` (?ëŠ” ?´ë‹¹ ?„ë¡œ?íŠ¸ëª?

### 2. ?„ìš”???Œì´ë¸??ì„±

OAuth Service???„ìš”???Œì´ë¸”ì„ ?ì„±?˜ì„¸??

```sql
-- ?¬ìš©???Œì´ë¸?(?ˆì‹œ)
CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(255) PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    provider VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- OAuth ? í° ?Œì´ë¸?(? íƒ?¬í•­)
CREATE TABLE IF NOT EXISTS oauth_tokens (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) REFERENCES users(id),
    provider VARCHAR(50) NOT NULL,
    access_token TEXT,
    refresh_token TEXT,
    expires_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ?¸ë±??
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_oauth_tokens_user_id ON oauth_tokens(user_id);
```

---

## ?? ?¤í–‰ ë°©ë²•

### 1. ?´ë?ì§€ ë¹Œë“œ

```bash
docker-compose build gateway oauth-service
```

### 2. ì»¨í…Œ?´ë„ˆ ?œì‘

```bash
docker-compose up -d gateway oauth-service
```

### 3. ë¡œê·¸ ?•ì¸

```bash
# Gateway ë¡œê·¸
docker logs gateway -f

# OAuth Service ë¡œê·¸
docker logs oauth -f
```

---

## ?” API ?”ë“œ?¬ì¸??

### ?„ë¡ ?¸ì—”?œì—???¸ì¶œ

```typescript
// 1. ?¤ì´ë²?ë¡œê·¸??URL ?”ì²­
GET http://localhost:8080/oauth/naver/login-url

Response:
{
  "url": "https://nid.naver.com/oauth2.0/authorize?...",
  "state": "uuid-string"
}

// 2. ?¬ìš©?ê? ?¤ì´ë²?ë¡œê·¸?????ë™ ì½œë°±
GET http://localhost:8080/oauth/naver/callback?code=xxx&state=xxx

Response:
{
  "data": {
    "accessToken": "jwt-token",
    "refreshToken": "jwt-refresh-token",
    "userInfo": {
      "id": "xxx",
      "email": "user@example.com",
      "name": "?ê¸¸??
    }
  }
}
```

---

## ?§ª ?ŒìŠ¤??ë°©ë²•

### 1. Gateway ?•ìƒ ?™ì‘ ?•ì¸

```bash
curl http://localhost:8080/actuator/health
```

### 2. OAuth Service ?¬ìŠ¤ ì²´í¬

```bash
curl http://localhost:8108/actuator/health
```

### 3. ?¤ì´ë²?ë¡œê·¸??URL ?ì„± ?ŒìŠ¤??

```bash
curl http://localhost:8080/oauth/naver/login-url
```

?ˆìƒ ?‘ë‹µ:
```json
{
  "url": "https://nid.naver.com/oauth2.0/authorize?response_type=code&client_id=CRd0KSYwlBXwo1GmcmKW&redirect_uri=http://localhost:8080/oauth/naver/callback&state=...",
  "state": "uuid"
}
```

---

## ?“Š ?„í‚¤?ì²˜

```
?Œâ??€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€??
?? Frontend       ??
?? (localhost:3000)??
?”â??€?€?€?€?€?€?€?¬â??€?€?€?€?€?€?€??
         ??
         ??GET /oauth/naver/login-url
         ??
?Œâ??€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€??
?? Gateway        ??
?? (localhost:8080)??
?”â??€?€?€?€?€?€?€?¬â??€?€?€?€?€?€?€??
         ??
         ??Route: /oauth/** ??oauth:8080/oauth/**
         ??
?Œâ??€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€??        ?Œâ??€?€?€?€?€?€?€?€?€?€?€?€?€??
?? OAuth Service  ?‚â??€?€?€?€?€?€?€?¶â”‚  Neon DB     ??
?? (oauth:8080)   ??        ?? (PostgreSQL)??
?”â??€?€?€?€?€?€?€?¬â??€?€?€?€?€?€?€??        ?”â??€?€?€?€?€?€?€?€?€?€?€?€?€??
         ??
         ??Callback from Naver
         ??
?Œâ??€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€??
?? Naver Login    ??
?? (nid.naver.com)??
?”â??€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€??
```

---

## ?› ?¸ëŸ¬ë¸”ìŠˆ??

### 1. Neon DB ?°ê²° ?¤íŒ¨

```bash
# ë¡œê·¸ ?•ì¸
docker logs oauth | grep -i "password\|connection"

# ?°ê²° ?ŒìŠ¤??
psql "postgresql://$NEON_DB_USER:$NEON_DB_PASSWORD@$NEON_DB_HOST/$NEON_DB_NAME?sslmode=require"
```

### 2. ?¤ì´ë²?ë¡œê·¸???¤íŒ¨

- ?¤ì´ë²?ê°œë°œ??ì½˜ì†”?ì„œ Callback URL???•í™•??`http://localhost:8080/oauth/naver/callback`?¸ì? ?•ì¸
- `.env` ?Œì¼??`NAVER_CLIENT_ID`, `NAVER_CLIENT_SECRET` ?•ì¸

### 3. CORS ?ëŸ¬

- `SecurityConfig.java`?ì„œ `/oauth/**` ê²½ë¡œê°€ `permitAll()`ë¡??¤ì •?˜ì–´ ?ˆëŠ”ì§€ ?•ì¸
- Gateway??CORS ?¤ì • ?•ì¸

---

## ?“ ì°¸ê³ ?¬í•­

### Spring Profile ?„ëµ

- **neon**: Neon PostgreSQL ?¬ìš© (?„ë¡œ?•ì…˜)
- **default**: ë¡œì»¬ DB ?¬ìš© (ê°œë°œ)

`docker-compose.yaml`?ì„œ `SPRING_PROFILES_ACTIVE=neon`?¼ë¡œ ?¤ì •??

### ë³´ì•ˆ ê³ ë ¤?¬í•­

1. **JWT Secret**: ìµœì†Œ 32???´ìƒ???œë¤ ë¬¸ì???¬ìš©
2. **DB ë¹„ë?ë²ˆí˜¸**: ê°•ë ¥??ë¹„ë?ë²ˆí˜¸ ?¬ìš©, `.env` ?Œì¼?€ Git??ì»¤ë°‹?˜ì? ë§?ê²?
3. **State ?Œë¼ë¯¸í„°**: ?„ì¬??ê²€ì¦??†ì´ ?¬ìš©, ì¶”í›„ Redis???€?¥í•˜??CSRF ë°©ì? êµ¬í˜„ ?„ìš”

---

??ê°€?´ë“œë¥?ì°¸ê³ ?˜ì—¬ OAuth Service?€ Neon DBë¥??¤ì •?˜ì„¸??

