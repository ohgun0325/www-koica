# OAuth ?„ë¡ ?¸ì—”???˜ì´ì§€ ?†ì´ ë¡œê·¸???„ëµ

## ê°œìš”
`/oauth/callback` ë°?`/oauth/error` ?„ë¡ ?¸ì—”???˜ì´ì§€ ?†ì´??OAuth ë¡œê·¸?¸ì´ ?•ìƒ ?™ì‘?˜ë„ë¡?ë°±ì—”?œì—??HTML??ì§ì ‘ ë°˜í™˜?˜ëŠ” ?„ëµ?…ë‹ˆ??

## ?µì‹¬ ?„í‚¤?ì²˜

### 1. ë°±ì—”??HTML ?‘ë‹µ ë°©ì‹
- **ë°˜í™˜ ?€??*: `ResponseEntity<String>` (MediaType.TEXT_HTML)
- **?¥ì **: ?„ë¡ ?¸ì—”???¼ìš°??ë¶ˆí•„?? ?…ë¦½???™ì‘
- **ì²˜ë¦¬ ?ë¦„**: ë°±ì—”?œê? ?„ì „??HTML ?˜ì´ì§€ë¥??ì„±?˜ì—¬ ë°˜í™˜

### 2. êµ¬í˜„ ë°©ì‹

#### A. ?±ê³µ ??ì²˜ë¦¬
```java
@GetMapping(value = "/callback", produces = MediaType.TEXT_HTML_VALUE)
public ResponseEntity<String> callback(@RequestParam String code, @RequestParam String state) {
    // 1. OAuth ? í° êµí™˜
    // 2. ?¬ìš©???•ë³´ ì¡°íšŒ
    // 3. JWT ? í° ?ì„±
    // 4. HTML ?˜ì´ì§€ ë°˜í™˜ (?ë™?¼ë¡œ localStorage ?€??ë°?ë¦¬ë‹¤?´ë ‰??
    
    String html = generateSuccessHtml(responseJson, frontendRedirectUrl);
    return ResponseEntity.ok()
        .contentType(MediaType.TEXT_HTML)
        .body(html);
}
```

#### B. ?ëŸ¬ ??ì²˜ë¦¬
```java
catch (Exception e) {
    String html = generateErrorHtml(errorMessage, frontendRedirectUrl);
    return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
        .contentType(MediaType.TEXT_HTML)
        .body(html);
}
```

### 3. HTML ?˜ì´ì§€ êµ¬ì¡°

#### ?±ê³µ ?˜ì´ì§€ (generateSuccessHtml)
```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>ë¡œê·¸??ì²˜ë¦¬ ì¤?..</title>
    <!-- ?¤í??¼ë§ -->
</head>
<body>
    <div class="container">
        <div class="spinner"></div>
        <h2>ë¡œê·¸???±ê³µ!</h2>
        <p>ë©”ì¸ ?˜ì´ì§€ë¡??´ë™ ì¤‘ì…?ˆë‹¤...</p>
    </div>
    <script>
        (function() {
            const response = %s; // JSON ?°ì´??ì£¼ì…
            
            // localStorage??? í° ?€??
            localStorage.setItem('accessToken', response.accessToken);
            localStorage.setItem('refreshToken', response.refreshToken);
            localStorage.setItem('userId', response.user.id);
            localStorage.setItem('userEmail', response.user.email);
            localStorage.setItem('userName', response.user.name);
            
            // ?ë™ ë¦¬ë‹¤?´ë ‰??
            setTimeout(() => window.location.href = '%s', 500);
        })();
    </script>
</body>
</html>
```

#### ?ëŸ¬ ?˜ì´ì§€ (generateErrorHtml)
```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>ë¡œê·¸???¤íŒ¨</title>
</head>
<body>
    <div class="container">
        <div class="error-icon">??/div>
        <h2>ë¡œê·¸???¤íŒ¨</h2>
        <p>%s</p> <!-- ?ëŸ¬ ë©”ì‹œì§€ -->
        <button onclick="window.location.href='%s'">?ˆìœ¼ë¡??Œì•„ê°€ê¸?/button>
    </div>
</body>
</html>
```

### 4. ?¥ì 

#### ?…ë¦½??
- ?„ë¡ ?¸ì—”??`/oauth` ?´ë” ë¶ˆí•„??
- Next.js ?¼ìš°?…ê³¼ ë¬´ê??˜ê²Œ ?™ì‘
- ë°±ì—”???¨ë…?¼ë¡œ ?„ì „??OAuth ì²˜ë¦¬

#### ë³´ì•ˆ
- ? í°??URL???¸ì¶œ?˜ì? ?ŠìŒ (HTML ?´ë??ì„œ ì²˜ë¦¬)
- ì¦‰ì‹œ localStorageë¡??´ë™
- ë¸Œë¼?°ì? ?ˆìŠ¤? ë¦¬??? í° ë¯¸ë…¸ì¶?

#### UX
- ë¡œë”© ? ë‹ˆë©”ì´???œê³µ
- ëª…í™•???±ê³µ/?¤íŒ¨ ?¼ë“œë°?
- ?ë™ ë¦¬ë‹¤?´ë ‰??

#### ? ì?ë³´ìˆ˜
- ë°±ì—”?œì—??ëª¨ë“  OAuth ë¡œì§ ê´€ë¦?
- ?„ë¡ ?¸ì—”??ë¹Œë“œ/ë°°í¬?€ ?…ë¦½??
- HTML ?œí”Œë¦??˜ì •ë§Œìœ¼ë¡?UI ë³€ê²?ê°€??

### 5. ?™ì‘ ?ë¦„

```
1. ?¬ìš©??ë¡œê·¸??ë²„íŠ¼ ?´ë¦­
   ??
2. /oauth/naver/login-url ?¸ì¶œ ???¤ì´ë²?ë¡œê·¸??URL ë°˜í™˜
   ??
3. ?¤ì´ë²?ë¡œê·¸???˜ì´ì§€ë¡?ë¦¬ë‹¤?´ë ‰??
   ??
4. ?¤ì´ë²??¸ì¦ ?„ë£Œ
   ??
5. /oauth/naver/callback?code=xxx&state=xxx ?¸ì¶œ
   ??
6. ë°±ì—”??
   - ?¤ì´ë²?? í° êµí™˜
   - ?¬ìš©???•ë³´ ì¡°íšŒ
   - JWT ? í° ?ì„±
   - HTML ?˜ì´ì§€ ?ì„± (? í° ?¬í•¨)
   ??
7. ë¸Œë¼?°ì??ì„œ HTML ?Œë”ë§?
   - JavaScript ?ë™ ?¤í–‰
   - localStorage??? í° ?€??
   - 500ms ??ë©”ì¸ ?˜ì´ì§€ë¡?ë¦¬ë‹¤?´ë ‰??
   ??
8. ë©”ì¸ ?˜ì´ì§€ ?„ì°© (ë¡œê·¸???„ë£Œ)
```

### 6. ?„ìš”???Œì¼

#### ë°±ì—”??
- `NaverController.java`: HTML ?ì„± ë°?ë°˜í™˜ ë¡œì§
- `OAuthLoginResponse.java`: ?‘ë‹µ DTO
- `JwtTokenProvider.java`: JWT ? í° ?ì„±

#### ?„ë¡ ?¸ì—”??
- **ë¶ˆí•„??*: `/app/oauth/callback/page.tsx` ?? œ ê°€??
- **ë¶ˆí•„??*: `/app/oauth/error/page.tsx` ?? œ ê°€??
- `mainservice.ts`: ë¡œê·¸??URL ?”ì²­ë§??´ë‹¹

### 7. ?˜ê²½ ë³€??

```yaml
oauth:
  frontend:
    redirect-url: http://localhost:3002  # ?±ê³µ ??ë¦¬ë‹¤?´ë ‰?¸í•  ?„ë¡ ?¸ì—”??URL
```

### 8. ë³´ì•ˆ ê³ ë ¤?¬í•­

#### CSRF ë°©ì–´
- `state` ?Œë¼ë¯¸í„°ë¥?Redis???€?¥í•˜??ê²€ì¦?(TODO)
- ?¤ì´ë²?ì½œë°± ??`state` ë§¤ì¹­ ?•ì¸

#### XSS ë°©ì–´
- HTML ???¬ìš©???…ë ¥ ?°ì´???´ìŠ¤ì¼€?´í”„
- Content-Security-Policy ?¤ë” ì¶”ê? ê³ ë ¤

#### Token ?¸ì¶œ ë°©ì?
- URL??? í° ?¬í•¨?˜ì? ?ŠìŒ
- HTML body ??JavaScriptë¡œë§Œ ì²˜ë¦¬
- ì¦‰ì‹œ localStorage ?€????ë³€???? œ

### 9. ?•ì¥ ê°€?¥ì„±

#### ?¤ì¤‘ Provider ì§€??
```java
@GetMapping("/{provider}/callback")
public ResponseEntity<String> callback(
    @PathVariable String provider,
    @RequestParam String code,
    @RequestParam String state
) {
    // provider???°ë¼ ?¤ë¥¸ ?œë¹„???¸ì¶œ
}
```

#### ì»¤ìŠ¤?€ ë¦¬ë‹¤?´ë ‰??
```java
// ì¿¼ë¦¬ ?Œë¼ë¯¸í„°ë¡?ë¦¬ë‹¤?´ë ‰??URL ?„ë‹¬
@RequestParam(required = false) String returnUrl
```

#### HTML ?œí”Œë¦??¸ë???
- Thymeleaf ?ëŠ” Freemarker ?¬ìš©
- ë³„ë„ HTML ?Œì¼ë¡?ê´€ë¦?
- ?¤êµ­??ì§€??

### 10. ?ŒìŠ¤??ë°©ë²•

#### ë¡œì»¬ ?ŒìŠ¤??
```bash
# 1. oauth-service ë¹Œë“œ ë°??œì‘
docker-compose build oauth-service
docker-compose up -d oauth-service

# 2. ë¡œê·¸ ?•ì¸
docker logs -f oauth

# 3. ë¸Œë¼?°ì??ì„œ ë¡œê·¸???œë„
http://localhost:3002
```

#### ?±ê³µ ???•ì¸ ?¬í•­
- [ ] ?°ë??ì— "???¤ì´ë²?ë¡œê·¸???±ê³µ!" ì¶œë ¥
- [ ] ë¸Œë¼?°ì???ë¡œë”© ? ë‹ˆë©”ì´???œì‹œ
- [ ] localStorage??? í° ?€???•ì¸ (F12 ??Application ??Local Storage)
- [ ] ë©”ì¸ ?˜ì´ì§€ë¡??ë™ ë¦¬ë‹¤?´ë ‰??

#### ?¤íŒ¨ ???•ì¸ ?¬í•­
- [ ] ?ëŸ¬ ?˜ì´ì§€ ?œì‹œ
- [ ] ?ëŸ¬ ë©”ì‹œì§€ ëª…í™•?˜ê²Œ ?œì‹œ
- [ ] "?ˆìœ¼ë¡??Œì•„ê°€ê¸? ë²„íŠ¼ ?™ì‘

### 11. ë§ˆì´ê·¸ë ˆ?´ì…˜ ì²´í¬ë¦¬ìŠ¤??

#### ?„ë¡ ?¸ì—”???•ë¦¬
- [ ] `/app/oauth/callback/page.tsx` ?? œ
- [ ] `/app/oauth/error/page.tsx` ?? œ
- [ ] `/app/oauth` ?´ë” ?? œ (ë¹„ì–´?ˆì„ ê²½ìš°)

#### ë°±ì—”???•ì¸
- [ ] `NaverController.java` ?…ë°?´íŠ¸ ?„ë£Œ
- [ ] `ObjectMapper` ?˜ì¡´??ì£¼ì… ?•ì¸
- [ ] HTML ?ì„± ë©”ì„œ??êµ¬í˜„ ?•ì¸

#### ?ŒìŠ¤??
- [ ] ë¡œê·¸???±ê³µ ?Œë¡œ???ŒìŠ¤??
- [ ] ë¡œê·¸???¤íŒ¨ ?Œë¡œ???ŒìŠ¤??
- [ ] ? í° ?€???•ì¸
- [ ] ë¦¬ë‹¤?´ë ‰???•ì¸

### 12. ?¸ëŸ¬ë¸”ìŠˆ??

#### "ë¡œê·¸??ì²˜ë¦¬ ì¤??¤ë¥˜" ?œì‹œ
- ë°±ì—”??ë¡œê·¸ ?•ì¸: `docker logs oauth`
- ?¤ì´ë²?? í° êµí™˜ ?¤íŒ¨ ?¬ë? ?•ì¸
- ?˜ê²½ë³€??(NAVER_CLIENT_ID, NAVER_CLIENT_SECRET) ?•ì¸

#### ? í°???€?¥ë˜ì§€ ?ŠìŒ
- ë¸Œë¼?°ì? ì½˜ì†” ?ëŸ¬ ?•ì¸
- localStorage ì¿¼í„° ?•ì¸
- ì¿ í‚¤/localStorage ì°¨ë‹¨ ?¤ì • ?•ì¸

#### ë¦¬ë‹¤?´ë ‰?¸ë˜ì§€ ?ŠìŒ
- JavaScript ?ëŸ¬ ?•ì¸
- `oauth.frontend.redirect-url` ?¤ì • ?•ì¸
- ?¤íŠ¸?Œí¬ ??—??ë¦¬ë‹¤?´ë ‰??URL ?•ì¸

---

## ê²°ë¡ 

???„ëµ?€ ?„ë¡ ?¸ì—”???¼ìš°???†ì´??OAuth ë¡œê·¸?¸ì„ ?„ì „?˜ê²Œ ì²˜ë¦¬?????ˆëŠ” ?…ë¦½?ì´ê³??ˆì „??ë°©ì‹?…ë‹ˆ?? ë°±ì—”?œì—??HTML??ì§ì ‘ ?ì„±?˜ì—¬ ë°˜í™˜?¨ìœ¼ë¡œì¨ ?„ë¡ ?¸ì—”???˜ì¡´?±ì„ ìµœì†Œ?”í•˜ê³?? ì?ë³´ìˆ˜?±ì„ ?’ì…?ˆë‹¤.

