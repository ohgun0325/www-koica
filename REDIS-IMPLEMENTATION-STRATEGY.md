# Redis êµ¬í˜„ ?„ëµ

## ?“Š ?„ì¬ ?íƒœ ë¶„ì„

### ?¸í”„??
- ??Redis ì»¨í…Œ?´ë„ˆ ?¤í–‰ ì¤?(Docker Compose)
- ??Gateway?ì„œ Rate Limiting?©ìœ¼ë¡?Redis ?¬ìš© ì¤?
- ??OAuth Service??Redis ?˜ì¡´??ì¶”ê???(`spring-boot-starter-data-redis`)
- ??OAuth Service?ì„œ Redis ?¬ìš© ë¡œì§ ?†ìŒ

### ë¬¸ì œ??
1. JWT ? í° ê´€ë¦¬ê? ?„í? ????
2. Refresh Token???´ë¼?´ì–¸?¸ì— ?¸ì¶œ??(ë³´ì•ˆ ì·¨ì•½)
3. ë¡œê·¸?„ì›ƒ ê¸°ëŠ¥ êµ¬í˜„ ë¶ˆê?
4. ? í° ?ˆì·¨ ???€??ë¶ˆê?
5. OAuth CSRF ë°©ì?(state ê²€ì¦? ë¯¸êµ¬??

---

## ?¯ Redis êµ¬í˜„ ?„ëµ

### Phase 1: Redis ê¸°ë³¸ ?¸í”„??êµ¬ì„± ??(?„ë£Œ)

**?„ë£Œ???‘ì—…:**
- Redis ?˜ì¡´??ì¶”ê? (`build.gradle`)
- Redis ?°ê²° ?¤ì • (`application.yaml`)
- Docker Compose Redis ì»¨í…Œ?´ë„ˆ ?¤ì •

---

### Phase 2: Token Storage Service êµ¬í˜„

**ëª©ì :** Refresh Token???œë²„(Redis)?ì„œ ê´€ë¦¬í•˜??ë³´ì•ˆ ê°•í™”

#### 2.1. RedisConfig ?´ë˜???ì„±
**?Œì¼:** `core.ohgun.site/oauthservice/src/main/java/site/OHGUN/core/oauth/config/RedisConfig.java`

```java
package site.OHGUN.core.oauth.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.redis.connection.RedisConnectionFactory;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.data.redis.serializer.StringRedisSerializer;

@Configuration
public class RedisConfig {

    @Bean
    public RedisTemplate<String, String> redisTemplate(RedisConnectionFactory connectionFactory) {
        RedisTemplate<String, String> template = new RedisTemplate<>();
        template.setConnectionFactory(connectionFactory);
        
        // Key?€ Value ëª¨ë‘ String Serializer ?¬ìš©
        template.setKeySerializer(new StringRedisSerializer());
        template.setValueSerializer(new StringRedisSerializer());
        template.setHashKeySerializer(new StringRedisSerializer());
        template.setHashValueSerializer(new StringRedisSerializer());
        
        return template;
    }
}
```

#### 2.2. TokenStorageService ?´ë˜???ì„±
**?Œì¼:** `core.ohgun.site/oauthservice/src/main/java/site/OHGUN/core/oauth/redis/TokenStorageService.java`

```java
package site.OHGUN.core.oauth.redis;

import lombok.RequiredArgsConstructor;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.stereotype.Service;

import java.util.concurrent.TimeUnit;

@Service
@RequiredArgsConstructor
public class TokenStorageService {

    private final RedisTemplate<String, String> redisTemplate;
    private static final String REFRESH_TOKEN_PREFIX = "refresh_token:";

    /**
     * Refresh Token??Redis???€??
     * @param userId ?¬ìš©??ID
     * @param refreshToken Refresh Token
     * @param expirationSeconds ë§Œë£Œ ?œê°„ (ì´?
     */
    public void saveRefreshToken(String userId, String refreshToken, long expirationSeconds) {
        String key = REFRESH_TOKEN_PREFIX + userId;
        redisTemplate.opsForValue().set(key, refreshToken, expirationSeconds, TimeUnit.SECONDS);
    }

    /**
     * Redis?ì„œ Refresh Token ì¡°íšŒ
     * @param userId ?¬ìš©??ID
     * @return Refresh Token (?†ìœ¼ë©?null)
     */
    public String getRefreshToken(String userId) {
        String key = REFRESH_TOKEN_PREFIX + userId;
        return redisTemplate.opsForValue().get(key);
    }

    /**
     * Refresh Token ê²€ì¦?
     * @param userId ?¬ìš©??ID
     * @param refreshToken ?´ë¼?´ì–¸?¸ê? ?œê³µ??Refresh Token
     * @return ? íš¨?˜ë©´ true, ?„ë‹ˆë©?false
     */
    public boolean isRefreshTokenValid(String userId, String refreshToken) {
        String storedToken = getRefreshToken(userId);
        return storedToken != null && storedToken.equals(refreshToken);
    }

    /**
     * Refresh Token ?? œ (ë¡œê·¸?„ì›ƒ)
     * @param userId ?¬ìš©??ID
     */
    public void deleteRefreshToken(String userId) {
        String key = REFRESH_TOKEN_PREFIX + userId;
        redisTemplate.delete(key);
    }

    /**
     * Refresh Token ?¨ì? TTL ì¡°íšŒ
     * @param userId ?¬ìš©??ID
     * @return ?¨ì? ?œê°„ (ì´?, ?†ìœ¼ë©?-2
     */
    public long getRefreshTokenTTL(String userId) {
        String key = REFRESH_TOKEN_PREFIX + userId;
        Long ttl = redisTemplate.getExpire(key, TimeUnit.SECONDS);
        return ttl != null ? ttl : -2;
    }
}
```

**Redis Key êµ¬ì¡°:**
```
refresh_token:{userId} = {refreshToken}
TTL: 7??(604800ì´?
```

**?ˆì‹œ:**
```
refresh_token:naver_12345678 = eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
TTL: 604800
```

---

### Phase 3: OAuth State ê´€ë¦?(CSRF ë°©ì?)

**ëª©ì :** ?¤ì´ë²?OAuth ë¡œê·¸????CSRF ê³µê²© ë°©ì?

#### 3.1. StateStorageService ?´ë˜???ì„±
**?Œì¼:** `core.ohgun.site/oauthservice/src/main/java/site/OHGUN/core/oauth/redis/StateStorageService.java`

```java
package site.OHGUN.core.oauth.redis;

import lombok.RequiredArgsConstructor;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.stereotype.Service;

import java.util.concurrent.TimeUnit;

@Service
@RequiredArgsConstructor
public class StateStorageService {

    private final RedisTemplate<String, String> redisTemplate;
    private static final String STATE_PREFIX = "oauth_state:";
    private static final long STATE_EXPIRATION_SECONDS = 600; // 10ë¶?

    /**
     * OAuth state ?€??
     * @param state UUID ?•íƒœ??state
     * @param metadata ì¶”ê? ë©”í??°ì´??(? íƒ?¬í•­, ?? IP ì£¼ì†Œ)
     */
    public void saveState(String state, String metadata) {
        String key = STATE_PREFIX + state;
        String value = metadata != null ? metadata : String.valueOf(System.currentTimeMillis());
        redisTemplate.opsForValue().set(key, value, STATE_EXPIRATION_SECONDS, TimeUnit.SECONDS);
    }

    /**
     * State ê²€ì¦?ë°??? œ (1?Œìš©)
     * @param state ê²€ì¦í•  state
     * @return ? íš¨?˜ë©´ true, ?„ë‹ˆë©?false
     */
    public boolean validateAndDeleteState(String state) {
        String key = STATE_PREFIX + state;
        String value = redisTemplate.opsForValue().get(key);
        
        if (value != null) {
            // 1?Œìš©?´ë?ë¡?ì¦‰ì‹œ ?? œ
            redisTemplate.delete(key);
            return true;
        }
        
        return false;
    }

    /**
     * State ì¡´ì¬ ?¬ë? ?•ì¸ (?? œ?˜ì? ?ŠìŒ)
     * @param state ?•ì¸??state
     * @return ì¡´ì¬?˜ë©´ true
     */
    public boolean isStateExists(String state) {
        String key = STATE_PREFIX + state;
        return Boolean.TRUE.equals(redisTemplate.hasKey(key));
    }
}
```

**Redis Key êµ¬ì¡°:**
```
oauth_state:{state} = {timestamp}
TTL: 10ë¶?(600ì´?
```

**?ˆì‹œ:**
```
oauth_state:d33928d0-3d7a-4831-951e-167d58b41ced = 1701234567890
TTL: 600
```

---

### Phase 4: Access Token Blacklist (? íƒ?¬í•­)

**ëª©ì :** ê°•ì œ ë¡œê·¸?„ì›ƒ ??Access Token ì¦‰ì‹œ ë¬´íš¨??

#### 4.1. TokenBlacklistService ?´ë˜???ì„±
**?Œì¼:** `core.ohgun.site/oauthservice/src/main/java/site/OHGUN/core/oauth/redis/TokenBlacklistService.java`

```java
package site.OHGUN.core.oauth.redis;

import lombok.RequiredArgsConstructor;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.stereotype.Service;

import java.util.concurrent.TimeUnit;

@Service
@RequiredArgsConstructor
public class TokenBlacklistService {

    private final RedisTemplate<String, String> redisTemplate;
    private static final String BLACKLIST_PREFIX = "blacklist_token:";

    /**
     * Access Token??ë¸”ë™ë¦¬ìŠ¤?¸ì— ì¶”ê?
     * @param accessToken Access Token
     * @param expirationSeconds ? í°???¨ì? ? íš¨ê¸°ê°„ (ì´?
     */
    public void addToBlacklist(String accessToken, long expirationSeconds) {
        String key = BLACKLIST_PREFIX + accessToken;
        redisTemplate.opsForValue().set(key, "1", expirationSeconds, TimeUnit.SECONDS);
    }

    /**
     * Access Token??ë¸”ë™ë¦¬ìŠ¤?¸ì— ?ˆëŠ”ì§€ ?•ì¸
     * @param accessToken ?•ì¸??Access Token
     * @return ë¸”ë™ë¦¬ìŠ¤?¸ì— ?ˆìœ¼ë©?true
     */
    public boolean isBlacklisted(String accessToken) {
        String key = BLACKLIST_PREFIX + accessToken;
        return Boolean.TRUE.equals(redisTemplate.hasKey(key));
    }

    /**
     * ë¸”ë™ë¦¬ìŠ¤?¸ì—??? í° ?œê±° (TTL??ì§€?˜ë©´ ?ë™ ?? œ?˜ë?ë¡??¼ë°˜?ìœ¼ë¡?ë¶ˆí•„??
     * @param accessToken ?œê±°??Access Token
     */
    public void removeFromBlacklist(String accessToken) {
        String key = BLACKLIST_PREFIX + accessToken;
        redisTemplate.delete(key);
    }
}
```

**Redis Key êµ¬ì¡°:**
```
blacklist_token:{accessToken} = "1"
TTL: Access Token???¨ì? ? íš¨ê¸°ê°„
```

**?ˆì‹œ:**
```
blacklist_token:eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9... = "1"
TTL: 300 (5ë¶??¨ìŒ)
```

---

### Phase 5: NaverController ?µí•©

#### 5.1. NaverController ?˜ì •?¬í•­

**?Œì¼:** `core.ohgun.site/oauthservice/src/main/java/site/OHGUN/core/oauth/naver/NaverController.java`

**ë³€ê²??´ìš©:**

##### 1) ?˜ì¡´??ì¶”ê?
```java
private final TokenStorageService tokenStorageService;
private final StateStorageService stateStorageService;

@Value("${jwt.refresh-token-validity-in-seconds}")
private long refreshTokenValidityInSeconds;
```

##### 2) `/login-url` ?”ë“œ?¬ì¸???˜ì •
```java
@GetMapping("/login-url")
public ResponseEntity<Map<String, String>> getLoginUrl() {
    String state = UUID.randomUUID().toString();
    String url = naverService.buildAuthorizeUrl(state);
    
    // Stateë¥?Redis???€??(CSRF ë°©ì?)
    stateStorageService.saveState(state, null);
    
    return ResponseEntity.ok(Map.of("url", url, "state", state));
}
```

##### 3) `/callback` ?”ë“œ?¬ì¸???˜ì •
```java
@GetMapping("/callback")
public RedirectView callback(
        @RequestParam String code,
        @RequestParam String state
) {
    try {
        // 1. State ê²€ì¦?(CSRF ë°©ì?)
        if (!stateStorageService.validateAndDeleteState(state)) {
            throw new RuntimeException("Invalid or expired state parameter");
        }

        // 2. ?¤ì´ë²?? í° êµí™˜
        NaverTokenResponse tokenResponse = naverService.exchangeToken(code, state);
        if (tokenResponse == null || tokenResponse.getAccessToken() == null) {
            throw new RuntimeException("?¤ì´ë²?? í° êµí™˜ ?¤íŒ¨");
        }

        // 3. ?¬ìš©???•ë³´ ì¡°íšŒ
        NaverUserInfo userInfo = naverService.fetchUserInfo(tokenResponse.getAccessToken());
        if (userInfo == null || userInfo.getId() == null) {
            throw new RuntimeException("?¬ìš©???•ë³´ ì¡°íšŒ ?¤íŒ¨");
        }

        // 4. JWT ? í° ?ì„±
        String userId = userInfo.getId();
        String accessToken = jwtTokenProvider.createAccessToken(
                userId,
                Map.of("email", userInfo.getEmail() != null ? userInfo.getEmail() : "", 
                       "name", userInfo.getName() != null ? userInfo.getName() : "")
        );
        String refreshToken = jwtTokenProvider.createRefreshToken(
                userId,
                Map.of("email", userInfo.getEmail() != null ? userInfo.getEmail() : "", 
                       "name", userInfo.getName() != null ? userInfo.getName() : "")
        );

        // 5. Refresh Token??Redis???€??
        tokenStorageService.saveRefreshToken(userId, refreshToken, refreshTokenValidityInSeconds);

        // 6. Access Tokenë§??„ë¡ ?¸ì—”?œë¡œ ?„ë‹¬ (Refresh Token?€ ?„ë‹¬?˜ì? ?ŠìŒ)
        String redirectUrl = String.format(
                "%s/oauth/callback?accessToken=%s&email=%s&name=%s",
                frontendRedirectUrl,
                URLEncoder.encode(accessToken, StandardCharsets.UTF_8),
                URLEncoder.encode(userInfo.getEmail() != null ? userInfo.getEmail() : "", StandardCharsets.UTF_8),
                URLEncoder.encode(userInfo.getName() != null ? userInfo.getName() : "", StandardCharsets.UTF_8)
        );

        return new RedirectView(redirectUrl);
    } catch (Exception e) {
        System.err.println("OAuth callback error: " + e.getMessage());
        e.printStackTrace();
        
        String errorMessage = e.getMessage() != null ? e.getMessage() : "ë¡œê·¸??ì²˜ë¦¬ ì¤??¤ë¥˜ê°€ ë°œìƒ?ˆìŠµ?ˆë‹¤.";
        String errorUrl = String.format(
                "%s/oauth/error?message=%s",
                frontendRedirectUrl,
                URLEncoder.encode(errorMessage, StandardCharsets.UTF_8)
        );
        return new RedirectView(errorUrl);
    }
}
```

##### 4) `/refresh` ?”ë“œ?¬ì¸??ì¶”ê? (?ˆë¡œ???”ë“œ?¬ì¸??
```java
@PostMapping("/refresh")
public ResponseEntity<?> refresh(@RequestBody Map<String, String> request) {
    try {
        String userId = request.get("userId");
        String refreshToken = request.get("refreshToken");

        if (userId == null || refreshToken == null) {
            return ResponseEntity.badRequest().body(Map.of("error", "userId and refreshToken are required"));
        }

        // Redis?ì„œ Refresh Token ê²€ì¦?
        if (!tokenStorageService.isRefreshTokenValid(userId, refreshToken)) {
            return ResponseEntity.status(401).body(Map.of("error", "Invalid or expired refresh token"));
        }

        // ??Access Token ?ì„±
        String newAccessToken = jwtTokenProvider.createAccessToken(
                userId,
                Map.of() // ?„ìš”??claims ì¶”ê?
        );

        return ResponseEntity.ok(Map.of(
                "accessToken", newAccessToken,
                "tokenType", "Bearer"
        ));
    } catch (Exception e) {
        return ResponseEntity.status(500).body(Map.of("error", e.getMessage()));
    }
}
```

##### 5) `/logout` ?”ë“œ?¬ì¸??ì¶”ê? (?ˆë¡œ???”ë“œ?¬ì¸??
```java
@PostMapping("/logout")
public ResponseEntity<?> logout(@RequestBody Map<String, String> request) {
    try {
        String userId = request.get("userId");

        if (userId == null) {
            return ResponseEntity.badRequest().body(Map.of("error", "userId is required"));
        }

        // Redis?ì„œ Refresh Token ?? œ
        tokenStorageService.deleteRefreshToken(userId);

        // (? íƒ?¬í•­) Access Token??Blacklist??ì¶”ê?
        // String accessToken = request.get("accessToken");
        // if (accessToken != null) {
        //     long remainingTime = ...; // JWT?ì„œ ?¨ì? ?œê°„ ê³„ì‚°
        //     tokenBlacklistService.addToBlacklist(accessToken, remainingTime);
        // }

        return ResponseEntity.ok(Map.of("message", "Logged out successfully"));
    } catch (Exception e) {
        return ResponseEntity.status(500).body(Map.of("error", e.getMessage()));
    }
}
```

---

### Phase 6: ?„ë¡ ?¸ì—”???˜ì •

#### 6.1. callback ?˜ì´ì§€ ?˜ì •
**?Œì¼:** `www.ohgun.site/app/oauth/callback/page.tsx`

**ë³€ê²??¬í•­:**
- Refresh Token???œê±° (?œë²„?ì„œ ê´€ë¦?
- userId ?€??(? í° ê°±ì‹ /ë¡œê·¸?„ì›ƒ???¬ìš©)

```typescript
'use client';

import { useEffect } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';

export default function OAuthCallbackPage() {
    const searchParams = useSearchParams();
    const router = useRouter();

    useEffect(() => {
        const accessToken = searchParams.get('accessToken');
        const email = searchParams.get('email');
        const name = searchParams.get('name');

        if (accessToken) {
            // Access Tokenë§?localStorage???€??
            localStorage.setItem('accessToken', accessToken);

            // ?¬ìš©???•ë³´ ?€??
            if (email) localStorage.setItem('userEmail', email);
            if (name) localStorage.setItem('userName', name);
            
            // userId ?€??(? í° ê°±ì‹ /ë¡œê·¸?„ì›ƒ???¬ìš©)
            // ?¤ì œë¡œëŠ” JWTë¥??Œì‹±?˜ê±°???œë²„?ì„œ userIdë¥?ë³„ë„ë¡??„ë‹¬ë°›ì•„????
            // ?¬ê¸°?œëŠ” email??userIdë¡??¬ìš©
            if (email) localStorage.setItem('userId', email);

            // ë©”ì¸ ?˜ì´ì§€ë¡?ë¦¬ë‹¤?´ë ‰??
            router.push('/');
        } else {
            // ? í°???†ìœ¼ë©??ëŸ¬ ?˜ì´ì§€ë¡?
            router.push('/oauth/error?message=? í°??ë°›ì•„?¤ì? ëª»í–ˆ?µë‹ˆ??');
        }
    }, [searchParams, router]);

    return (
        <div className="flex items-center justify-center min-h-screen">
            <div className="text-center">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900 mx-auto mb-4"></div>
                <p className="text-gray-600">ë¡œê·¸??ì²˜ë¦¬ ì¤?..</p>
            </div>
        </div>
    );
}
```

#### 6.2. ? í° ê°±ì‹  ë¡œì§ ì¶”ê?
**?Œì¼:** `www.ohgun.site/services/authservice.ts` (?ˆë¡œ ?ì„±)

```typescript
export async function refreshAccessToken(): Promise<string | null> {
    try {
        const userId = localStorage.getItem('userId');
        const refreshToken = localStorage.getItem('refreshToken'); // ?œë²„?ì„œ ê´€ë¦¬í•˜ë¯€ë¡?ë¶ˆí•„??

        if (!userId) {
            throw new Error('No userId found');
        }

        const response = await fetch('http://localhost:8080/oauth/naver/refresh', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ userId }),
        });

        if (!response.ok) {
            throw new Error('Failed to refresh token');
        }

        const data = await response.json();
        localStorage.setItem('accessToken', data.accessToken);
        return data.accessToken;
    } catch (error) {
        console.error('Token refresh error:', error);
        // ë¡œê·¸???˜ì´ì§€ë¡?ë¦¬ë‹¤?´ë ‰??
        window.location.href = '/';
        return null;
    }
}

export async function logout(): Promise<void> {
    try {
        const userId = localStorage.getItem('userId');

        if (userId) {
            await fetch('http://localhost:8080/oauth/naver/logout', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ userId }),
            });
        }

        // localStorage ?•ë¦¬
        localStorage.removeItem('accessToken');
        localStorage.removeItem('userId');
        localStorage.removeItem('userEmail');
        localStorage.removeItem('userName');

        // ?ˆìœ¼ë¡?ë¦¬ë‹¤?´ë ‰??
        window.location.href = '/';
    } catch (error) {
        console.error('Logout error:', error);
    }
}
```

---

## ?—‚ï¸?ìµœì¢… ?Œì¼ êµ¬ì¡°

```
core.ohgun.site/oauthservice/
?œâ??€ src/main/java/site/OHGUN/core/oauth/
??  ?œâ??€ config/
??  ??  ?œâ??€ SecurityConfig.java
??  ??  ?”â??€ RedisConfig.java                    # ?ˆë¡œ ì¶”ê?
??  ?œâ??€ jwt/
??  ??  ?œâ??€ JwtProperties.java
??  ??  ?”â??€ JwtTokenProvider.java
??  ?œâ??€ redis/                                   # ?ˆë¡œ ì¶”ê?
??  ??  ?œâ??€ TokenStorageService.java
??  ??  ?œâ??€ StateStorageService.java
??  ??  ?”â??€ TokenBlacklistService.java (? íƒ)
??  ?”â??€ naver/
??      ?œâ??€ dto/
??      ??  ?œâ??€ NaverTokenResponse.java
??      ??  ?œâ??€ NaverUserInfo.java
??      ??  ?”â??€ NaverLoginResponse.java
??      ?œâ??€ NaverController.java                 # ?˜ì •
??      ?”â??€ NaverService.java
?”â??€ src/main/resources/
    ?”â??€ application.yaml

www.ohgun.site/
?œâ??€ app/
??  ?”â??€ oauth/
??      ?œâ??€ callback/
??      ??  ?”â??€ page.tsx                         # ?˜ì •
??      ?”â??€ error/
??          ?”â??€ page.tsx
?”â??€ services/
    ?”â??€ authservice.ts                            # ?ˆë¡œ ì¶”ê?
```

---

## ?”„ ? í° ?Œë¡œ??(ê°œì„  ??

### ë¡œê·¸???Œë¡œ??
```
1. ?¬ìš©?? ?„ë¡ ?¸ì—”?œì—??"?¤ì´ë²?ë¡œê·¸?? ë²„íŠ¼ ?´ë¦­
2. ?„ë¡ ?¸ì—”????GET /oauth/naver/login-url
3. ë°±ì—”??
   - state = UUID ?ì„±
   - Redis??state ?€??(TTL: 10ë¶?
   - ?¤ì´ë²?ë¡œê·¸??URL ë°˜í™˜
4. ?„ë¡ ?¸ì—”?????¤ì´ë²?ë¡œê·¸???˜ì´ì§€ë¡?ë¦¬ë‹¤?´ë ‰??
5. ?¬ìš©?? ?¤ì´ë²„ì—??ë¡œê·¸??
6. ?¤ì´ë²???GET /oauth/naver/callback?code=xxx&state=yyy
7. ë°±ì—”??
   - Redis?ì„œ state ê²€ì¦?(CSRF ë°©ì?)
   - ?¤ì´ë²?APIë¡?? í° êµí™˜
   - ?¤ì´ë²?APIë¡??¬ìš©???•ë³´ ì¡°íšŒ
   - JWT Access Token + Refresh Token ?ì„±
   - Refresh Token ??Redis ?€??(TTL: 7??
   - Access Tokenë§??„ë¡ ?¸ì—”?œë¡œ ë¦¬ë‹¤?´ë ‰??
8. ?„ë¡ ?¸ì—”??
   - Access Token ??localStorage ?€??
   - userId ??localStorage ?€??
   - ë©”ì¸ ?˜ì´ì§€ë¡??´ë™
```

### ? í° ê°±ì‹  ?Œë¡œ??
```
1. ?„ë¡ ?¸ì—”?? Access Token ë§Œë£Œ ê°ì?
2. ?„ë¡ ?¸ì—”????POST /oauth/naver/refresh
   Body: { userId }
3. ë°±ì—”??
   - Redis?ì„œ Refresh Token ì¡°íšŒ
   - Refresh Token ê²€ì¦?
   - ??Access Token ?ì„±
   - ??Access Token ë°˜í™˜
4. ?„ë¡ ?¸ì—”??
   - ??Access Token ??localStorage ?…ë°?´íŠ¸
```

### ë¡œê·¸?„ì›ƒ ?Œë¡œ??
```
1. ?¬ìš©?? "ë¡œê·¸?„ì›ƒ" ë²„íŠ¼ ?´ë¦­
2. ?„ë¡ ?¸ì—”????POST /oauth/naver/logout
   Body: { userId }
3. ë°±ì—”??
   - Redis?ì„œ Refresh Token ?? œ
   - (? íƒ) Access Token??Blacklist??ì¶”ê?
4. ?„ë¡ ?¸ì—”??
   - localStorage ëª¨ë“  ?°ì´???? œ
   - ?ˆìœ¼ë¡?ë¦¬ë‹¤?´ë ‰??
```

---

## ?“ êµ¬í˜„ ì²´í¬ë¦¬ìŠ¤??

### Phase 2: Token Storage Service
- [ ] `RedisConfig.java` ?ì„±
- [ ] `TokenStorageService.java` ?ì„±
- [ ] Redis ?°ê²° ?ŒìŠ¤??

### Phase 3: OAuth State ê´€ë¦?
- [ ] `StateStorageService.java` ?ì„±
- [ ] `/login-url`??state ?€??ë¡œì§ ì¶”ê?
- [ ] `/callback`??state ê²€ì¦?ë¡œì§ ì¶”ê?

### Phase 4: Access Token Blacklist (? íƒ)
- [ ] `TokenBlacklistService.java` ?ì„±
- [ ] `/logout`??Blacklist ì¶”ê? ë¡œì§ êµ¬í˜„

### Phase 5: NaverController ?µí•©
- [ ] ?˜ì¡´??ì£¼ì… ì¶”ê?
- [ ] `/login-url` ?˜ì •
- [ ] `/callback` ?˜ì • (Refresh Token Redis ?€??
- [ ] `/refresh` ?”ë“œ?¬ì¸??ì¶”ê?
- [ ] `/logout` ?”ë“œ?¬ì¸??ì¶”ê?

### Phase 6: ?„ë¡ ?¸ì—”???˜ì •
- [ ] `callback/page.tsx` ?˜ì • (Refresh Token ?œê±°)
- [ ] `authservice.ts` ?ì„± (? í° ê°±ì‹ /ë¡œê·¸?„ì›ƒ ë¡œì§)
- [ ] API ?”ì²­ ?¸í„°?‰í„° ì¶”ê? (Access Token ?ë™ ê°±ì‹ )

---

## ?”’ ë³´ì•ˆ ê³ ë ¤?¬í•­

### 1. Refresh Token ë³´ì•ˆ
- ??Refresh Token?€ Redis?ë§Œ ?€??(?´ë¼?´ì–¸???¸ì¶œ ë°©ì?)
- ??TTL 7???¤ì •
- ??ë¡œê·¸?„ì›ƒ ??ì¦‰ì‹œ ?? œ

### 2. State ê²€ì¦?(CSRF ë°©ì?)
- ??1?Œìš© state ?¬ìš©
- ??TTL 10ë¶„ìœ¼ë¡??œí•œ
- ??ê²€ì¦???ì¦‰ì‹œ ?? œ

### 3. Access Token
- ? ï¸ ?´ë¼?´ì–¸??localStorage)???€?¥ë˜ë¯€ë¡?XSS ì·¨ì•½
- ??ì§§ì? TTL (15ë¶? ?¤ì •
- ??HTTPS ?¬ìš© ?„ìˆ˜

### 4. Redis ë³´ì•ˆ
- ??ë¹„ë?ë²ˆí˜¸ ?¤ì • (`REDIS_PASSWORD`)
- ? ï¸ ?„ë¡œ?•ì…˜ ?˜ê²½?ì„œ??Redis SSL/TLS ?¬ìš© ê¶Œì¥
- ? ï¸ Redis ?¤íŠ¸?Œí¬ ê²©ë¦¬ (?¸ë? ?‘ê·¼ ì°¨ë‹¨)

---

## ?› ?¸ëŸ¬ë¸”ìŠˆ??

### Redis ?°ê²° ?¤íŒ¨
```bash
# Redis ì»¨í…Œ?´ë„ˆ ?•ì¸
docker ps | grep redis

# Redis ë¡œê·¸ ?•ì¸
docker logs redis

# Redis ?°ê²° ?ŒìŠ¤??
docker exec -it redis redis-cli -a Redis0930! ping
```

### Token Storage ?ŒìŠ¤??
```bash
# Redis??ì§ì ‘ ?‘ì†
docker exec -it redis redis-cli -a Redis0930!

# Refresh Token ?•ì¸
KEYS refresh_token:*
GET refresh_token:naver_12345678

# State ?•ì¸
KEYS oauth_state:*
GET oauth_state:d33928d0-3d7a-4831-951e-167d58b41ced

# TTL ?•ì¸
TTL refresh_token:naver_12345678
```

---

## ?“š ì°¸ê³  ?ë£Œ

- [Spring Data Redis Documentation](https://docs.spring.io/spring-data/redis/docs/current/reference/html/)
- [Redis TTL Commands](https://redis.io/commands/ttl/)
- [OAuth 2.0 Security Best Practices](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-security-topics)
- [JWT Best Practices](https://tools.ietf.org/html/rfc8725)

---

## ?“… ?¤ìŒ ?¨ê³„

1. **Phase 2ë¶€???œì°¨?ìœ¼ë¡?êµ¬í˜„**
2. **ê°?Phase ?„ë£Œ ???ŒìŠ¤??*
3. **?„ë¡ ?¸ì—”???µí•© ?ŒìŠ¤??*
4. **ë³´ì•ˆ ê²€??ë°?ìµœì ??*

---

**?‘ì„±??** 2025-12-04  
**ë²„ì „:** 1.0  
**?íƒœ:** êµ¬í˜„ ?€ê¸?ì¤?

