# ?˜ê²½ ë³€???¤ì • ê°€?´ë“œ

## ?“‹ .env ?Œì¼ êµ¬ì„±

?„ë¡œ?íŠ¸ ë£¨íŠ¸??`.env` ?Œì¼???ì„±?˜ê³  ?„ë˜ ?´ìš©??ì¶”ê??˜ì„¸??

```bash
# ========================================
# Neon PostgreSQL ?°ê²° ?•ë³´
# ========================================
# Neon ?€?œë³´??> Dashboard > Connection Details ?ì„œ ?•ì¸
NEON_DB_HOST=ep-withered-pond-a11avi67.ap-southeast-1.aws.neon.tech
NEON_DB_NAME=ohgundb
NEON_DB_USER=neondb_owner
NEON_DB_PASSWORD=your-neon-password-here

# ========================================
# Upstash Redis ?°ê²° ?•ë³´ (Gateway ?„ìš©)
# ========================================
# Upstash Console > Details ??—???•ì¸
# Endpoint: awaited-insect-5667.upstash.io
# Port: 6379
# TLS/SSL: Enabled
UPSTASH_REDIS_HOST=awaited-insect-5667.upstash.io
UPSTASH_REDIS_PORT=6379
UPSTASH_REDIS_PASSWORD=your_upstash_password_here

# ========================================
# Spring ?¤ì •
# ========================================
SPRING_PROFILES_ACTIVE=production

# JPA ?¤ì •
JPA_DDL_AUTO=validate
JPA_SHOW_SQL=false

# SQL ë¡œê¹… ?ˆë²¨
SQL_LOG_LEVEL=INFO
SQL_PARAM_LOG_LEVEL=INFO

# ========================================
# Redis ?¤ì • (ë¡œì»¬ ê°œë°œ??
# ========================================
REDIS_PASSWORD=Redis0930!
```

## ?”§ Neon PostgreSQL ?°ê²° ?•ë³´ ?•ì¸

### 1. Neon Console ?‘ì†
- URL: https://console.neon.tech
- ?„ë¡œ?íŠ¸: `aifix`

### 2. Connection String ë³µì‚¬
Dashboard > Connection Details ?ì„œ ?•ì¸:

```
postgresql://neondb_owner:your-password@ep-withered-pond-a11avi67.ap-southeast-1.aws.neon.tech/ohgundb?sslmode=require
```

### 3. ?˜ê²½ ë³€??ë¶„ë¦¬
??Connection String??ë¶„ë¦¬?˜ì—¬ `.env`???…ë ¥:

- `NEON_DB_HOST`: `ep-withered-pond-a11avi67.ap-southeast-1.aws.neon.tech`
- `NEON_DB_NAME`: `ohgundb`
- `NEON_DB_USER`: `neondb_owner`
- `NEON_DB_PASSWORD`: `your-password` (?¤ì œ ë¹„ë?ë²ˆí˜¸)

## ?”§ Upstash Redis ?°ê²° ?•ë³´ ?•ì¸

### 1. Upstash Console ?‘ì†
- URL: https://console.upstash.com

### 2. Redis ?¸ìŠ¤?´ìŠ¤ ? íƒ
- Details ??—???°ê²° ?•ë³´ ?•ì¸

### 3. TCP ?°ê²° ?•ë³´ ?•ì¸
Details ??> **TCP** ??—???¤ìŒ ?•ë³´ë¥??•ì¸:

```
redis-cli --tls -u redis://default:********@awaited-insect-5667.upstash.io:6379
```

### 4. ?˜ê²½ ë³€???…ë ¥
??ëª…ë ¹?´ì—???•ë³´ë¥?ì¶”ì¶œ?˜ì—¬ `.env`???…ë ¥:

- `UPSTASH_REDIS_HOST`: `awaited-insect-5667.upstash.io`
- `UPSTASH_REDIS_PORT`: `6379`
- `UPSTASH_REDIS_PASSWORD`: `********` ë¶€ë¶„ì˜ ?¤ì œ ë¹„ë?ë²ˆí˜¸ (Token / Readonly Token ì¤?**Token** ?¬ìš©)

## ?“ ?Œì¼ ?„ì¹˜

```
feature-ys/
?œâ??€ .env                          # ???¬ê¸°??ëª¨ë“  ?˜ê²½ ë³€???µí•©
?œâ??€ .gitignore                    # .env ?Œì¼ ?œì™¸ (?´ë? ?¤ì •??
?œâ??€ application-production.yaml   # ?„ë¡œ?•ì…˜ ?¤ì • (Neon + Upstash)
?œâ??€ docker-compose.yaml           # env_file: .env ?¬ìš©
?”â??€ ENV-SETUP-GUIDE.md           # ??ê°€?´ë“œ
```

## ?”’ ë³´ì•ˆ ì£¼ì˜?¬í•­

1. **?ˆë? Git??ì»¤ë°‹?˜ì? ë§ˆì„¸??**
   - `.env` ?Œì¼?€ `.gitignore`???¬í•¨??
   - ë¯¼ê°???•ë³´ ?¬í•¨

2. **?„ë¡œ?•ì…˜ ?˜ê²½**
   - AWS Secrets Manager
   - HashiCorp Vault
   - GitHub Secrets (CI/CD)

3. **?€ ê³µìœ **
   - ?ˆì „??ì±„ë„ë¡œë§Œ ê³µìœ  (Slack DM, 1Password ??
   - ?´ë©”??ê³µê°œ ì±„íŒ… ê¸ˆì?

## ?¯ ?„ë¡œ?Œì¼ë³??¤ì •

### ë¡œì»¬ ê°œë°œ (ê¸°ë³¸)
```bash
SPRING_PROFILES_ACTIVE=default
# ë¡œì»¬ PostgreSQL + ë¡œì»¬ Redis ?¬ìš©
```

### ?„ë¡œ?•ì…˜ (Neon + Upstash)
```bash
SPRING_PROFILES_ACTIVE=production
# Neon PostgreSQL + Upstash Redis ?¬ìš©
```

## ?› ?¸ëŸ¬ë¸”ìŠˆ??

### Neon ?°ê²° ?¤íŒ¨
```bash
# 1. ë¹„ë?ë²ˆí˜¸ ?•ì¸
cat .env | grep NEON_DB_PASSWORD

# 2. ?°ê²° ?ŒìŠ¤??
psql "postgresql://$NEON_DB_USER:$NEON_DB_PASSWORD@$NEON_DB_HOST/$NEON_DB_NAME?sslmode=require"
```

### Upstash ?°ê²° ?¤íŒ¨
```bash
# 1. Redis CLIë¡??ŒìŠ¤??
redis-cli -h $UPSTASH_REDIS_HOST -p $UPSTASH_REDIS_PORT -a $UPSTASH_REDIS_PASSWORD ping

# 2. ?‘ë‹µ ?•ì¸
# ?ˆìƒ: PONG
```

## ?“Š ë¦¬ì†Œ???œí•œ

### Neon (Free Plan)
- Storage: 0.5 GB
- Compute: ìµœë? 2 CU
- Branches: 10ê°?

### Upstash (Free Plan)
- Commands: 10,000/day
- Max Data Size: 256 MB
- Max Request Size: 1 MB

---

**??ê°€?´ë“œë¥?ì°¸ê³ ?˜ì—¬ `.env` ?Œì¼???¤ì •?˜ì„¸??**

