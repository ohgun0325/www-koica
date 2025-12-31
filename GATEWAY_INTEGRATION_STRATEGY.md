# ?”„ Gateway ?µí•© ?„ëµ: FastAPI ??Spring Cloud Gateway

## ?“‹ ëª©ì°¨
1. [?„ì¬ ?í™© ë¶„ì„](#?„ì¬-?í™©-ë¶„ì„)
2. [?µí•© ?„ëµ ê°œìš”](#?µí•©-?„ëµ-ê°œìš”)
3. [?¨ê³„ë³??¤í–‰ ê³„íš](#?¨ê³„ë³??¤í–‰-ê³„íš)
4. [ê¸°ìˆ ??ê³ ë ¤?¬í•­](#ê¸°ìˆ ??ê³ ë ¤?¬í•­)
5. [ë§ˆì´ê·¸ë ˆ?´ì…˜ ì²´í¬ë¦¬ìŠ¤??(#ë§ˆì´ê·¸ë ˆ?´ì…˜-ì²´í¬ë¦¬ìŠ¤??

---

## ?” ?„ì¬ ?í™© ë¶„ì„

### ê¸°ì¡´ ?„í‚¤?ì²˜

```
?Œâ??€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€??
??                        ?´ë¼?´ì–¸??                           ??
?”â??€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?¬â??€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€??
                       ??
        ?Œâ??€?€?€?€?€?€?€?€?€?€?€?€?€?´â??€?€?€?€?€?€?€?€?€?€?€?€?€??
        ??                            ??
        ??                            ??
?Œâ??€?€?€?€?€?€?€?€?€?€?€?€?€?€??           ?Œâ??€?€?€?€?€?€?€?€?€?€?€?€?€?€?€??
?? FastAPI      ??           ?? Spring Cloud  ??
?? Gateway      ??           ?? Gateway       ??
?? (Port 9000)  ??           ?? (Port 8080)   ??
?”â??€?€?€?€?€?€?¬â??€?€?€?€?€?€??           ?”â??€?€?€?€?€?€?€?¬â??€?€?€?€?€?€??
        ??                            ??
   ?Œâ??€?€?€?´â??€?€?€??                  ?Œâ??€?€?€?´â??€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€??
   ??        ??                  ??                      ??
   ??        ??                  ??                      ??
?Œâ??€?€?€?€?? ?Œâ??€?€?€?€??        ?Œâ??€?€?€?€?€?€?€?€?€??         ?Œâ??€?€?€?€?€?€?€?€?€??
?‚Crawl?? ?‚Chat ??        ?‚User      ??         ?‚Common    ??
?‚er   ?? ?‚bot  ??        ?‚Service   ??         ?‚Service   ??
??001 ?? ??002 ??        ??104      ??         ??101      ??
?”â??€?€?€?€?? ?”â??€?€?€?€??        ?”â??€?€?€?€?€?€?€?€?€??         ?”â??€?€?€?€?€?€?€?€?€??
                         ?Œâ??€?€?€?€?€?€?€?€?€??         ?Œâ??€?€?€?€?€?€?€?€?€??
                         ?‚Environ   ??         ?‚Social    ??
                         ?‚ment      ??         ?‚Service   ??
                         ??105      ??         ??106      ??
                         ?”â??€?€?€?€?€?€?€?€?€??         ?”â??€?€?€?€?€?€?€?€?€??
                         ?Œâ??€?€?€?€?€?€?€?€?€??
                         ?‚Govern    ??
                         ?‚ance      ??
                         ??107      ??
                         ?”â??€?€?€?€?€?€?€?€?€??
```

### ë¬¸ì œ??
1. **?´ì¤‘ ê²Œì´?¸ì›¨??êµ¬ì¡°**: FastAPI?€ Spring Gatewayê°€ ë¶„ë¦¬?˜ì–´ ê´€ë¦?ë³µì¡??ì¦ê?
2. **?¼ê???ë¶€ì¡?*: Rate Limiting, Circuit Breaker ?±ì˜ ?•ì±…???µì¼?˜ì? ?ŠìŒ
3. **ëª¨ë‹ˆ?°ë§ ë¶„ì‚°**: ??ê²Œì´?¸ì›¨?´ì˜ ë©”íŠ¸ë¦?„ ?°ë¡œ ê´€ë¦¬í•´????
4. **ë°°í¬ ë³µì¡??*: ??ê°œì˜ ê²Œì´?¸ì›¨?´ë? ê°ê° ë°°í¬?˜ê³  ê´€ë¦¬í•´????

---

## ?¯ ?µí•© ?„ëµ ê°œìš”

### ëª©í‘œ ?„í‚¤?ì²˜

```
?Œâ??€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€??
??                        ?´ë¼?´ì–¸??                           ??
?”â??€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?¬â??€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€??
                       ??
                       ??
              ?Œâ??€?€?€?€?€?€?€?€?€?€?€?€?€?€?€??
              ?? Spring Cloud  ??
              ?? Gateway       ??
              ?? (Port 8080)   ??
              ?”â??€?€?€?€?€?€?€?¬â??€?€?€?€?€?€??
                       ??
    ?Œâ??€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?¼â??€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€?€??
    ??                 ??                     ??
    ??                 ??                     ??
?Œâ??€?€?€?€?€?€?€?€??     ?Œâ??€?€?€?€?€?€?€?€?€??         ?Œâ??€?€?€?€?€?€?€?€?€??
?‚Crawler  ??     ?‚Chatbot   ??         ?‚User      ??
?‚Service  ??     ?‚Service   ??         ?‚Service   ??
??FastAPI)??     ??FastAPI) ??         ??Spring)  ??
??001     ??     ??002      ??         ??104      ??
?”â??€?€?€?€?€?€?€?€??     ?”â??€?€?€?€?€?€?€?€?€??         ?”â??€?€?€?€?€?€?€?€?€??
                                       ?Œâ??€?€?€?€?€?€?€?€?€??
                                       ?‚Common    ??
                                       ?‚Service   ??
                                       ??101      ??
                                       ?”â??€?€?€?€?€?€?€?€?€??
                                       ?Œâ??€?€?€?€?€?€?€?€?€??
                                       ?‚Environ   ??
                                       ?‚ment      ??
                                       ??105      ??
                                       ?”â??€?€?€?€?€?€?€?€?€??
                                       ?Œâ??€?€?€?€?€?€?€?€?€??
                                       ?‚Social    ??
                                       ?‚Service   ??
                                       ??106      ??
                                       ?”â??€?€?€?€?€?€?€?€?€??
                                       ?Œâ??€?€?€?€?€?€?€?€?€??
                                       ?‚Govern    ??
                                       ?‚ance      ??
                                       ??107      ??
                                       ?”â??€?€?€?€?€?€?€?€?€??
```

### ?µì‹¬ ?„ëµ
1. **FastAPI Gateway ?œê±°**: `ai.ohgun.site/gateway` ?? œ
2. **FastAPI ?œë¹„???…ë¦½??*: Crawler, Chatbot ?œë¹„?¤ë? ?…ë¦½ ?¤í–‰
3. **Spring Gateway ?¼ìš°??ì¶”ê?**: FastAPI ?œë¹„?¤ë¡œ???¼ìš°???¤ì •
4. **?µí•© ëª¨ë‹ˆ?°ë§**: ëª¨ë“  ?œë¹„?¤ë? Spring Gatewayë¥??µí•´ ê´€ë¦?

---

## ?“ ?¨ê³„ë³??¤í–‰ ê³„íš

### Phase 1: FastAPI ?œë¹„???…ë¦½??(?°ì„ ?œìœ„: ?’ìŒ)

#### 1.1 Crawler Service ?…ë¦½ ?¤í–‰ ?¤ì •

**ëª©í‘œ**: Crawler ?œë¹„?¤ê? Gateway ?†ì´ ?…ë¦½?ìœ¼ë¡??¤í–‰?˜ë„ë¡??˜ì •

**?‘ì—… ?´ìš©**:
```yaml
# ai.ohgun.site/docker-compose.yaml ?˜ì •
services:
  crawlerservice:
    build:
      context: ./feed/crawlerservice
      dockerfile: Dockerfile
    ports:
      - "9001:9001"
    container_name: crawler-service
    networks:
      spring-network:  # ???¤íŠ¸?Œí¬ ?µí•©
        aliases:
          - crawler.local
    restart: unless-stopped
```

**Dockerfile ?•ì¸**:
```dockerfile
# ai.ohgun.site/feed/crawlerservice/Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

EXPOSE 9001

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "9001"]
```

#### 1.2 Chatbot Service ?…ë¦½ ?¤í–‰ ?¤ì •

**?‘ì—… ?´ìš©**:
```yaml
# ai.ohgun.site/docker-compose.yaml ?˜ì •
services:
  chatbotservice:
    build:
      context: ./rag/chatbotservice
      dockerfile: Dockerfile
    ports:
      - "9002:9002"
    container_name: chatbot-service
    networks:
      spring-network:  # ???¤íŠ¸?Œí¬ ?µí•©
        aliases:
          - chatbot.local
    restart: unless-stopped
```

---

### Phase 2: Spring Gateway ?¼ìš°??ì¶”ê? (?°ì„ ?œìœ„: ?’ìŒ)

#### 2.1 application.yaml??FastAPI ?œë¹„???¼ìš°??ì¶”ê?

**?Œì¼**: `api.ohgun.site/gateway/src/main/resources/application.yaml`

```yaml
spring:
  cloud:
    gateway:
      routes:
        # ========================================
        # FastAPI Services (AI/ML)
        # ========================================
        
        # Crawler Service - Rate Limiting + Circuit Breaker
        - id: crawler-service
          uri: http://crawler:9001
          predicates:
            - Path=/api/crawler/**
          filters:
            - StripPrefix=1
            - name: RequestRateLimiter
              args:
                redis-rate-limiter.replenishRate: 10
                redis-rate-limiter.burstCapacity: 20
                redis-rate-limiter.requestedTokens: 1
                key-resolver: "#{@ipKeyResolver}"
            - name: CircuitBreaker
              args:
                name: crawlerCircuitBreaker
        
        # Chatbot Service - Rate Limiting + Circuit Breaker
        - id: chatbot-service
          uri: http://chatbot:9002
          predicates:
            - Path=/api/chatbot/**
          filters:
            - StripPrefix=1
            - name: RequestRateLimiter
              args:
                redis-rate-limiter.replenishRate: 15
                redis-rate-limiter.burstCapacity: 30
                redis-rate-limiter.requestedTokens: 1
                key-resolver: "#{@ipKeyResolver}"
            - name: CircuitBreaker
              args:
                name: chatbotCircuitBreaker
        
        # Crawler Service - OpenAPI Docs
        - id: crawler-api-docs
          uri: http://crawler:9001
          predicates:
            - Path=/api-docs/crawler
          filters:
            - RewritePath=/api-docs/crawler, /openapi.json
        
        # Chatbot Service - OpenAPI Docs
        - id: chatbot-api-docs
          uri: http://chatbot:9002
          predicates:
            - Path=/api-docs/chatbot
          filters:
            - RewritePath=/api-docs/chatbot, /openapi.json

# Resilience4j Circuit Breaker ?¤ì • ì¶”ê?
resilience4j:
  circuitbreaker:
    instances:
      crawlerCircuitBreaker:
        sliding-window-size: 10
        failure-rate-threshold: 50
        wait-duration-in-open-state: 10s
        permitted-number-of-calls-in-half-open-state: 3
        automatic-transition-from-open-to-half-open-enabled: true
      chatbotCircuitBreaker:
        sliding-window-size: 10
        failure-rate-threshold: 50
        wait-duration-in-open-state: 10s
        permitted-number-of-calls-in-half-open-state: 3
        automatic-transition-from-open-to-half-open-enabled: true
```

#### 2.2 Swagger UI??FastAPI ?œë¹„??ì¶”ê?

```yaml
springdoc:
  swagger-ui:
    urls:
      - url: /v3/api-docs
        name: Gateway
      - url: /api-docs/user
        name: User Service
      - url: /api-docs/common
        name: Common Service
      - url: /api-docs/environment
        name: Environment Service
      - url: /api-docs/social
        name: Social Service
      - url: /api-docs/governance
        name: Governance Service
      - url: /api-docs/crawler
        name: Crawler Service (FastAPI)
      - url: /api-docs/chatbot
        name: Chatbot Service (FastAPI)
```

---

### Phase 3: Docker Compose ë¶„ë¦¬ ?´ì˜ ?¤ì • (?°ì„ ?œìœ„: ì¤‘ê°„)

#### 3.1 ?¤íŠ¸?Œí¬ ë¶„ë¦¬ ?„ëµ

**ëª©í‘œ**: `api.ohgun.site`?€ `ai.ohgun.site`ë¥?**ë³„ë„ë¡?docker-compose up** ?˜ë˜, Spring Gatewayê°€ FastAPI ?œë¹„?¤ì— ?‘ê·¼ ê°€?¥í•˜?„ë¡ ?¤ì •

**?„ëµ**:
- ??Docker Compose??**?…ë¦½?ìœ¼ë¡??¤í–‰**
- FastAPI ?œë¹„?¤ëŠ” **?¸ìŠ¤???¤íŠ¸?Œí¬ë¥??µí•´ ?‘ê·¼** (`localhost:9001`, `localhost:9002`)
- ?ëŠ” **?¸ë? Docker ?¤íŠ¸?Œí¬ ?ì„±**?˜ì—¬ ê³µìœ 

#### 3.2 ë°©ë²• 1: ?¸ìŠ¤???¤íŠ¸?Œí¬ ?‘ê·¼ (ê¶Œì¥)

**?¥ì **: ê°„ë‹¨?˜ê³  ê´€ë¦??©ì´, Docker Compose ?„ì „ ë¶„ë¦¬

**api.ohgun.site/gateway/src/main/resources/application.yaml ?˜ì •**:
```yaml
spring:
  cloud:
    gateway:
      routes:
        # Crawler Service - ?¸ìŠ¤?¸ë? ?µí•´ ?‘ê·¼
        - id: crawler-service
          uri: http://host.docker.internal:9001  # ???¸ìŠ¤???‘ê·¼
          predicates:
            - Path=/api/crawler/**
          filters:
            - StripPrefix=1
            - name: RequestRateLimiter
              args:
                redis-rate-limiter.replenishRate: 10
                redis-rate-limiter.burstCapacity: 20
                redis-rate-limiter.requestedTokens: 1
                key-resolver: "#{@ipKeyResolver}"
            - name: CircuitBreaker
              args:
                name: crawlerCircuitBreaker
        
        # Chatbot Service - ?¸ìŠ¤?¸ë? ?µí•´ ?‘ê·¼
        - id: chatbot-service
          uri: http://host.docker.internal:9002  # ???¸ìŠ¤???‘ê·¼
          predicates:
            - Path=/api/chatbot/**
          filters:
            - StripPrefix=1
            - name: RequestRateLimiter
              args:
                redis-rate-limiter.replenishRate: 15
                redis-rate-limiter.burstCapacity: 30
                redis-rate-limiter.requestedTokens: 1
                key-resolver: "#{@ipKeyResolver}"
            - name: CircuitBreaker
              args:
                name: chatbotCircuitBreaker
```

**?¤í–‰ ë°©ë²•**:
```bash
# Terminal 1: API ?œë¹„???¤í–‰
cd api.ohgun.site
docker-compose up -d

# Terminal 2: AI ?œë¹„???¤í–‰
cd ai.ohgun.site
docker-compose up -d
```

**ì£¼ì˜?¬í•­**:
- Windows/Mac: `host.docker.internal` ?¬ìš©
- Linux: `extra_hosts` ?¤ì • ?„ìš” (?„ë˜ ì°¸ê³ )

**Linux???¤ì •** (`api.ohgun.site/docker-compose.yaml`):
```yaml
services:
  gateway:
    build:
      context: .
      dockerfile: ./gateway/Dockerfile
    container_name: gateway
    ports:
      - "8080:8080"
    extra_hosts:
      - "host.docker.internal:host-gateway"  # ??Linux??ì¶”ê?
    depends_on:
      - redis
    environment:
      - REDIS_HOST=redis
      - REDIS_PORT=6379
      - REDIS_PASSWORD=${REDIS_PASSWORD:-Redis0930!}
    networks:
      spring-network:
        aliases:
          - gateway.local
```

#### 3.3 ë°©ë²• 2: ?¸ë? Docker ?¤íŠ¸?Œí¬ ê³µìœ  (ê³ ê¸‰)

**?¥ì **: ì»¨í…Œ?´ë„ˆ ê°?ì§ì ‘ ?µì‹ , ???˜ì? ?±ëŠ¥

**1?¨ê³„: ?¸ë? ?¤íŠ¸?Œí¬ ?ì„±**:
```bash
docker network create OHGUN-shared-network
```

**2?¨ê³„: api.ohgun.site/docker-compose.yaml ?˜ì •**:
```yaml
services:
  gateway:
    build:
      context: .
      dockerfile: ./gateway/Dockerfile
    container_name: gateway
    ports:
      - "8080:8080"
    depends_on:
      - redis
    environment:
      - REDIS_HOST=redis
      - REDIS_PORT=6379
      - REDIS_PASSWORD=${REDIS_PASSWORD:-Redis0930!}
    networks:
      - spring-network
      - OHGUN-shared-network  # ???¸ë? ?¤íŠ¸?Œí¬ ì¶”ê?

networks:
  spring-network:
    driver: bridge
  OHGUN-shared-network:
    external: true  # ???¸ë? ?¤íŠ¸?Œí¬ ?¬ìš©
```

**3?¨ê³„: ai.ohgun.site/docker-compose.yaml ?˜ì •**:
```yaml
services:
  crawlerservice:
    build:
      context: ./feed/crawlerservice
      dockerfile: Dockerfile
    ports:
      - "9001:9001"
    container_name: crawler-service
    networks:
      - ai-network
      - OHGUN-shared-network  # ???¸ë? ?¤íŠ¸?Œí¬ ì¶”ê?
    restart: unless-stopped

  chatbotservice:
    build:
      context: ./rag/chatbotservice
      dockerfile: Dockerfile
    ports:
      - "9002:9002"
    container_name: chatbot-service
    networks:
      - ai-network
      - OHGUN-shared-network  # ???¸ë? ?¤íŠ¸?Œí¬ ì¶”ê?
    restart: unless-stopped

networks:
  ai-network:
    driver: bridge
  OHGUN-shared-network:
    external: true  # ???¸ë? ?¤íŠ¸?Œí¬ ?¬ìš©
```

**4?¨ê³„: application.yaml?ì„œ ì»¨í…Œ?´ë„ˆ ?´ë¦„?¼ë¡œ ?‘ê·¼**:
```yaml
spring:
  cloud:
    gateway:
      routes:
        - id: crawler-service
          uri: http://crawler-service:9001  # ??ì»¨í…Œ?´ë„ˆ ?´ë¦„ ì§ì ‘ ?¬ìš©
          predicates:
            - Path=/api/crawler/**
```

#### 3.4 ai.ohgun.site ?´ë” ?•ë¦¬

**?‘ì—… ?´ìš©**:
1. `ai.ohgun.site/gateway` ?´ë” **?? œ**
2. `ai.ohgun.site/docker-compose.yaml` **? ì?** (?…ë¦½ ?¤í–‰??
3. FastAPI Gateway ê´€??ì½”ë“œ ?œê±°

---

### Phase 4: ?ŒìŠ¤??ë°?ê²€ì¦?(?°ì„ ?œìœ„: ?’ìŒ)

#### 4.1 ê¸°ëŠ¥ ?ŒìŠ¤??

**Crawler Service ?ŒìŠ¤??*:
```bash
# Spring Gatewayë¥??µí•œ ?‘ê·¼
curl http://localhost:8080/api/crawler/
curl http://localhost:8080/api/crawler/bugsmusic
curl http://localhost:8080/api/crawler/danawa

# ì§ì ‘ ?‘ê·¼ (ê°œë°œ??
curl http://localhost:9001/
curl http://localhost:9001/bugsmusic
curl http://localhost:9001/danawa
```

**Chatbot Service ?ŒìŠ¤??*:
```bash
# Spring Gatewayë¥??µí•œ ?‘ê·¼
curl http://localhost:8080/api/chatbot/

# ì§ì ‘ ?‘ê·¼ (ê°œë°œ??
curl http://localhost:9002/
```

#### 4.2 Rate Limiting ?ŒìŠ¤??

```bash
# Crawler Service Rate Limit ?ŒìŠ¤??(10 req/s)
for i in {1..15}; do
  curl -w "\n%{http_code}\n" http://localhost:8080/api/crawler/
  sleep 0.05
done

# 429 Too Many Requests ?‘ë‹µ ?•ì¸
```

#### 4.3 Circuit Breaker ?ŒìŠ¤??

```bash
# Crawler Service ì¤‘ë‹¨ ??Circuit Breaker ?™ì‘ ?•ì¸
docker stop crawler

# ?¬ëŸ¬ ë²??”ì²­?˜ì—¬ Circuit Open ?•ì¸
for i in {1..15}; do
  curl http://localhost:8080/api/crawler/
done

# 503 Service Unavailable ?‘ë‹µ ?•ì¸
```

#### 4.4 Swagger UI ?µí•© ?•ì¸

```bash
# Swagger UI ?‘ê·¼
http://localhost:8080/swagger-ui.html

# FastAPI ?œë¹„?¤ê? ?œë¡­?¤ìš´???œì‹œ?˜ëŠ”ì§€ ?•ì¸:
# - Crawler Service (FastAPI)
# - Chatbot Service (FastAPI)
```

---

## ?”§ ê¸°ìˆ ??ê³ ë ¤?¬í•­

### 1. FastAPI?€ Spring Gateway ?µí•© ??ì£¼ì˜?¬í•­

#### 1.1 OpenAPI ?¤í™ ì°¨ì´
- **ë¬¸ì œ**: FastAPI??OpenAPI 3.0, Spring?€ OpenAPI 3.0/3.1 ì§€??
- **?´ê²°**: FastAPI??`/openapi.json` ?”ë“œ?¬ì¸?¸ë? ê·¸ë?ë¡??„ë¡??

#### 1.2 CORS ?¤ì •
- **ë¬¸ì œ**: FastAPI ?œë¹„?¤ì— ?ì²´ CORS ?¤ì •???ˆì„ ???ˆìŒ
- **?´ê²°**: FastAPI ?œë¹„?¤ì˜ CORS ë¯¸ë“¤?¨ì–´ ?œê±°, Gateway?ì„œ ?µí•© ê´€ë¦?

```python
# ai.ohgun.site/feed/crawlerservice/app/main.py
# CORS ë¯¸ë“¤?¨ì–´ ?œê±° (Gateway?ì„œ ì²˜ë¦¬)
# app.add_middleware(CORSMiddleware, ...) ???? œ
```

#### 1.3 ê²½ë¡œ ë§¤í•‘
- **ê¸°ì¡´**: `/crawler/bugsmusic` (FastAPI Gateway)
- **ë³€ê²?*: `/api/crawler/bugsmusic` (Spring Gateway)
- **?„ë¡ ?¸ì—”???˜ì • ?„ìš”**: API ?¸ì¶œ ê²½ë¡œ ?…ë°?´íŠ¸

### 2. ?¤íŠ¸?Œí¬ ?µì‹ 

#### 2.1 Docker Compose ë¶„ë¦¬ ?´ì˜
- **api.ohgun.site**: ?…ë¦½ ?¤í–‰ (`spring-network`)
- **ai.ohgun.site**: ?…ë¦½ ?¤í–‰ (`ai-network`)
- **?µì‹  ë°©ë²•**:
  - **ë°©ë²• 1 (ê¶Œì¥)**: `host.docker.internal`???µí•œ ?¸ìŠ¤???¤íŠ¸?Œí¬ ?‘ê·¼
  - **ë°©ë²• 2**: ?¸ë? Docker ?¤íŠ¸?Œí¬ ê³µìœ  (`OHGUN-shared-network`)

#### 2.2 ?œë¹„???”ìŠ¤ì»¤ë²„ë¦?
- Spring ?œë¹„?? Docker DNS ?ëŠ” Eureka (? íƒ?¬í•­)
- FastAPI ?œë¹„?? 
  - ë°©ë²• 1: `host.docker.internal:9001`, `host.docker.internal:9002`
  - ë°©ë²• 2: `crawler-service:9001`, `chatbot-service:9002` (?¸ë? ?¤íŠ¸?Œí¬ ?¬ìš© ??

### 3. ëª¨ë‹ˆ?°ë§ ë°?ë¡œê¹…

#### 3.1 ?µí•© ë¡œê¹…
```yaml
# api.ohgun.site/gateway/src/main/resources/application.yaml
logging:
  level:
    org.springframework.cloud.gateway: DEBUG
    reactor.netty.http.client: DEBUG  # FastAPI ?¸ì¶œ ë¡œê¹…
```

#### 3.2 ë©”íŠ¸ë¦??˜ì§‘
```yaml
# Actuatorë¥??µí•œ ë©”íŠ¸ë¦??¸ì¶œ
management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics,prometheus,gateway
```

### 4. ?±ëŠ¥ ìµœì ??

#### 4.1 Connection Pool ?¤ì •
```yaml
# Gateway??HTTP ?´ë¼?´ì–¸???œë‹
spring:
  cloud:
    gateway:
      httpclient:
        pool:
          max-connections: 100
          max-idle-time: 30s
```

#### 4.2 Timeout ?¤ì •
```yaml
spring:
  cloud:
    gateway:
      routes:
        - id: crawler-service
          uri: http://crawler:9001
          predicates:
            - Path=/api/crawler/**
          filters:
            - StripPrefix=1
          metadata:
            response-timeout: 30000  # 30ì´?
            connect-timeout: 5000    # 5ì´?
```

---

## ??ë§ˆì´ê·¸ë ˆ?´ì…˜ ì²´í¬ë¦¬ìŠ¤??

### Phase 1: ì¤€ë¹??¨ê³„
- [ ] ?„ì¬ FastAPI Gateway???¼ìš°??ê·œì¹™ ë¬¸ì„œ??
- [ ] FastAPI ?œë¹„?¤ì˜ ?”ë“œ?¬ì¸??ëª©ë¡ ?‘ì„±
- [ ] ?„ë¡ ?¸ì—”?œì˜ API ?¸ì¶œ ê²½ë¡œ ?Œì•…
- [ ] ë°±ì—… ë°?ë¡¤ë°± ê³„íš ?˜ë¦½

### Phase 2: FastAPI ?œë¹„???…ë¦½??
- [ ] Crawler Service Dockerfile ê²€ì¦?
- [ ] Chatbot Service Dockerfile ê²€ì¦?
- [ ] ?…ë¦½ ?¤í–‰ ?ŒìŠ¤??(ë¡œì»¬)
- [ ] ?˜ê²½ ë³€??ë°??¤ì • ?•ì¸

### Phase 3: Spring Gateway ?¤ì •
- [ ] `application.yaml`??Crawler ?¼ìš°??ì¶”ê?
- [ ] `application.yaml`??Chatbot ?¼ìš°??ì¶”ê?
- [ ] Rate Limiting ?¤ì • ì¶”ê?
- [ ] Circuit Breaker ?¤ì • ì¶”ê?
- [ ] Swagger UI ?µí•©

### Phase 4: Docker Compose ë¶„ë¦¬ ?´ì˜ ?¤ì •
- [ ] ?¤íŠ¸?Œí¬ ?‘ê·¼ ë°©ë²• ? íƒ (?¸ìŠ¤???‘ê·¼ vs ?¸ë? ?¤íŠ¸?Œí¬)
- [ ] `application.yaml`?ì„œ FastAPI ?œë¹„??URI ?¤ì •
- [ ] Linux ?˜ê²½??ê²½ìš° `extra_hosts` ?¤ì •
- [ ] ??Docker Compose ?…ë¦½ ?¤í–‰ ?ŒìŠ¤??

### Phase 5: ?ŒìŠ¤??
- [ ] ë¡œì»¬ ?˜ê²½?ì„œ ?„ì²´ ?¤íƒ ?¤í–‰
- [ ] Crawler Service ê¸°ëŠ¥ ?ŒìŠ¤??
- [ ] Chatbot Service ê¸°ëŠ¥ ?ŒìŠ¤??
- [ ] Rate Limiting ?™ì‘ ?•ì¸
- [ ] Circuit Breaker ?™ì‘ ?•ì¸
- [ ] Swagger UI ?µí•© ?•ì¸
- [ ] ?±ëŠ¥ ?ŒìŠ¤??(ë¶€???ŒìŠ¤??

### Phase 6: ?„ë¡ ?¸ì—”???…ë°?´íŠ¸
- [ ] API ?¸ì¶œ ê²½ë¡œ ë³€ê²?(`/crawler/**` ??`/api/crawler/**`)
- [ ] ?ëŸ¬ ì²˜ë¦¬ ë¡œì§ ?•ì¸
- [ ] ?µí•© ?ŒìŠ¤??

### Phase 7: ?•ë¦¬
- [ ] `ai.ohgun.site/gateway` ?´ë” ?? œ
- [ ] `ai.ohgun.site/docker-compose.yaml` ? ì? (?…ë¦½ ?¤í–‰??
- [ ] FastAPI Gateway ê´€??ì½”ë“œ ?œê±°
- [ ] ë¬¸ì„œ ?…ë°?´íŠ¸

### Phase 8: ë°°í¬
- [ ] ?¤í…Œ?´ì§• ?˜ê²½ ë°°í¬
- [ ] ?¤í…Œ?´ì§• ?˜ê²½ ê²€ì¦?
- [ ] ?„ë¡œ?•ì…˜ ë°°í¬ ê³„íš ?˜ë¦½
- [ ] ?„ë¡œ?•ì…˜ ë°°í¬
- [ ] ëª¨ë‹ˆ?°ë§ ë°??Œë¦¼ ?¤ì •

---

## ?? ?¤í–‰ ?œì„œ ?”ì•½

1. **FastAPI ?œë¹„???…ë¦½??* (1-2?œê°„)
   - Dockerfile ê²€ì¦?
   - ?…ë¦½ ?¤í–‰ ?ŒìŠ¤??

2. **Spring Gateway ?¤ì •** (2-3?œê°„)
   - `application.yaml` ?˜ì •
   - Rate Limiting, Circuit Breaker ?¤ì •

3. **Docker Compose ë¶„ë¦¬ ?´ì˜ ?¤ì •** (1-2?œê°„)
   - ?¤íŠ¸?Œí¬ ?‘ê·¼ ë°©ë²• ? íƒ
   - URI ?¤ì • (`host.docker.internal` ?ëŠ” ?¸ë? ?¤íŠ¸?Œí¬)

4. **?ŒìŠ¤??ë°?ê²€ì¦?* (2-4?œê°„)
   - ê¸°ëŠ¥ ?ŒìŠ¤??
   - ?±ëŠ¥ ?ŒìŠ¤??
   - Swagger UI ?•ì¸

5. **?„ë¡ ?¸ì—”???…ë°?´íŠ¸** (1-2?œê°„)
   - API ê²½ë¡œ ë³€ê²?
   - ?µí•© ?ŒìŠ¤??

6. **?•ë¦¬ ë°?ë°°í¬** (1-2?œê°„)
   - ë¶ˆí•„?”í•œ ?Œì¼ ?œê±°
   - ë¬¸ì„œ ?…ë°?´íŠ¸
   - ë°°í¬

**ì´??ˆìƒ ?œê°„**: 8-15?œê°„

---

## ?“Š ê¸°ë? ?¨ê³¼

### 1. ?´ì˜ ?¨ìœ¨??
- ???¨ì¼ ê²Œì´?¸ì›¨?´ë¡œ ê´€ë¦?ë³µì¡??ê°ì†Œ
- ???µí•© ëª¨ë‹ˆ?°ë§ ë°?ë¡œê¹…
- ???¼ê???ë³´ì•ˆ ?•ì±… ?ìš©

### 2. ?±ëŠ¥
- ??ê²Œì´?¸ì›¨????ê°ì†Œ (2-hop ??1-hop)
- ??Spring WebFlux???¼ë¸”ë¡œí‚¹ I/O ?œìš©
- ??Redis ê¸°ë°˜ Rate Limiting

### 3. ?•ì¥??
- ???ˆë¡œ???œë¹„??ì¶”ê? ?©ì´
- ???¸ì–´??êµ¬ì• ë°›ì? ?ŠëŠ” ?„í‚¤?ì²˜
- ??ë§ˆì´?¬ë¡œ?œë¹„???¨í„´ ì¤€??

### 4. ê°œë°œ ?ì‚°??
- ??Swagger UI ?µí•©?¼ë¡œ API ë¬¸ì„œ ?µí•©
- ???¼ê????ëŸ¬ ì²˜ë¦¬
- ???œì??”ëœ ?¼ìš°??ê·œì¹™

---

## ?”„ ë¡¤ë°± ê³„íš

ë§Œì•½ ?µí•© ê³¼ì •?ì„œ ë¬¸ì œê°€ ë°œìƒ?˜ë©´:

1. **ì¦‰ì‹œ ë¡¤ë°±**:
   ```bash
   # ê¸°ì¡´ FastAPI Gateway ?¬ì‹œ??
   cd ai.ohgun.site
   docker-compose up -d gateway
   ```

2. **?„ë¡ ?¸ì—”??ê²½ë¡œ ë³µì›**:
   - API ?¸ì¶œ ê²½ë¡œë¥??ë˜?€ë¡?ë³µì›

3. **ë¬¸ì œ ë¶„ì„**:
   - ë¡œê·¸ ?•ì¸
   - ?ëŸ¬ ë©”ì‹œì§€ ë¶„ì„
   - ?¤íŠ¸?Œí¬ ?°ê²° ?•ì¸

4. **?¬ì‹œ??*:
   - ë¬¸ì œ ?´ê²° ???¨ê³„ë³„ë¡œ ?¬ì‹œ??

---

## ?“š ì°¸ê³  ?ë£Œ

- [Spring Cloud Gateway ê³µì‹ ë¬¸ì„œ](https://spring.io/projects/spring-cloud-gateway)
- [FastAPI ê³µì‹ ë¬¸ì„œ](https://fastapi.tiangolo.com/)
- [Resilience4j Circuit Breaker](https://resilience4j.readme.io/docs/circuitbreaker)
- [Redis Rate Limiting](https://redis.io/docs/manual/patterns/rate-limiter/)

---

**?‘ì„±??*: 2025-12-02  
**?‘ì„±??*: AI Assistant  
**ë²„ì „**: 1.0

