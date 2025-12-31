# Postman?ì„œ ?€?´í????œë¹„???ŒìŠ¤??ê°€?´ë“œ

## ?œë²„ ?¤í–‰

ë¨¼ì? ML ?œë¹„?¤ë? ?¤í–‰?´ì•¼ ?©ë‹ˆ??

```bash
cd ai.ohgun.site/mlsservice
python -m uvicorn app.main:app --host 0.0.0.0 --port 9004
```

?ëŠ” Docker Composeë¥??¬ìš©?˜ëŠ” ê²½ìš°:

```bash
docker-compose up mlsservice
```

## Postman?ì„œ API ?ŒìŠ¤?¸í•˜ê¸?

### 1. ê¸°ë³¸ ?¤ì •

- **Base URL**: `http://localhost:9004`
- **Content-Type**: `application/json` (?ë™ ?¤ì •??

### 2. ?¬ìš© ê°€?¥í•œ ?”ë“œ?¬ì¸??

#### 2.1 ?œë¹„???íƒœ ?•ì¸
- **Method**: `GET`
- **URL**: `http://localhost:9004/titanic/`
- **?¤ëª…**: ?€?´í????œë¹„???íƒœ ?•ì¸

#### 2.2 ?°ì´???„ì²˜ë¦?
- **Method**: `POST`
- **URL**: `http://localhost:9004/titanic/preprocess`
- **?¤ëª…**: train.csv?€ test.csv ?°ì´?°ë? ?„ì²˜ë¦¬í•˜ê³?ë¡œê·¸ë¥?ë°˜í™˜?©ë‹ˆ??
- **?‘ë‹µ ?ˆì‹œ**:
```json
{
  "message": "?„ì²˜ë¦??„ë£Œ",
  "status": "success",
  "logs": [
    "ic| '?˜Š?˜Š ?„ì²˜ë¦??œì‘'",
    "ic| '1. Train ??type \n <class 'pandas.core.frame.DataFrame'>'",
    ...
  ]
}
```

#### 2.3 ëª¨ë¸ë§?
- **Method**: `POST`
- **URL**: `http://localhost:9004/titanic/modeling`
- **?¤ëª…**: ëª¨ë¸ë§ì„ ?¤í–‰?˜ê³  ë¡œê·¸ë¥?ë°˜í™˜?©ë‹ˆ??

#### 2.4 ?™ìŠµ
- **Method**: `POST`
- **URL**: `http://localhost:9004/titanic/learning`
- **?¤ëª…**: ëª¨ë¸ ?™ìŠµ???¤í–‰?˜ê³  ë¡œê·¸ë¥?ë°˜í™˜?©ë‹ˆ??

#### 2.5 ?‰ê?
- **Method**: `POST`
- **URL**: `http://localhost:9004/titanic/evaluating`
- **?¤ëª…**: ëª¨ë¸ ?‰ê?ë¥??¤í–‰?˜ê³  ë¡œê·¸ë¥?ë°˜í™˜?©ë‹ˆ??

#### 2.6 ?œì¶œ
- **Method**: `POST`
- **URL**: `http://localhost:9004/titanic/submit`
- **?¤ëª…**: ê²°ê³¼ ?œì¶œ???¤í–‰?˜ê³  ë¡œê·¸ë¥?ë°˜í™˜?©ë‹ˆ??

#### 2.7 ?ìœ„ 10ëª??¹ê° ì¡°íšŒ
- **Method**: `GET`
- **URL**: `http://localhost:9004/titanic/passengers/top10`
- **?¤ëª…**: train.csv?ì„œ ?ìœ„ 10ëª…ì˜ ?¹ê° ?•ë³´ë¥?ì¡°íšŒ?©ë‹ˆ??

### 3. Postman?ì„œ ?”ì²­ ?ì„±?˜ê¸°

#### ?¨ê³„ë³?ê°€?´ë“œ:

1. **???”ì²­ ?ì„±**
   - Postman?ì„œ "New" ë²„íŠ¼ ?´ë¦­
   - "HTTP Request" ? íƒ

2. **?”ì²­ ?¤ì •**
   - Method: `POST` ?ëŠ” `GET` ? íƒ
   - URL ?…ë ¥: ?? `http://localhost:9004/titanic/preprocess`

3. **?”ì²­ ?„ì†¡**
   - "Send" ë²„íŠ¼ ?´ë¦­

4. **?‘ë‹µ ?•ì¸**
   - ?˜ë‹¨??"Body" ??—??JSON ?‘ë‹µ ?•ì¸
   - "logs" ë°°ì—´?ì„œ ?¤í–‰ ë¡œê·¸ ?•ì¸

### 4. ?ˆì‹œ: ?„ì²˜ë¦??¤í–‰

1. **?”ì²­ ?¤ì •**
   ```
   POST http://localhost:9004/titanic/preprocess
   ```

2. **?‘ë‹µ ?ˆì‹œ**
   ```json
   {
     "message": "?„ì²˜ë¦??„ë£Œ",
     "status": "success",
     "logs": [
       "ic| '?˜Š?˜Š ?„ì²˜ë¦??œì‘'",
       "ic| '1. Train ??type \n <class 'pandas.core.frame.DataFrame'>'",
       "ic| '2. Train ??column \n Index(['PassengerId', 'Pclass', ...], dtype='object')'",
       "ic| '3. Train ???ìœ„ 1ê°???n ...'",
       "ic| '4. Train ??null ??ê°?ˆ˜\n ...'",
       "ic| '?˜Š?˜Š ?„ì²˜ë¦??„ë£Œ'"
     ]
   }
   ```

3. **?ëŸ¬ ë°œìƒ ??*
   ```json
   {
     "message": "?„ì²˜ë¦?ì¤??¤ë¥˜ ë°œìƒ",
     "status": "error",
     "error": "['Survived'] not found in axis",
     "logs": []
   }
   ```

### 5. ?„ì²´ ?Œí¬?Œë¡œ???ŒìŠ¤??

?¤ìŒ ?œì„œë¡?APIë¥??¸ì¶œ?˜ì—¬ ?„ì²´ ?„ë¡œ?¸ìŠ¤ë¥??ŒìŠ¤?¸í•  ???ˆìŠµ?ˆë‹¤:

1. `POST /titanic/preprocess` - ?°ì´???„ì²˜ë¦?
2. `POST /titanic/modeling` - ëª¨ë¸ë§?
3. `POST /titanic/learning` - ?™ìŠµ
4. `POST /titanic/evaluating` - ?‰ê?
5. `POST /titanic/submit` - ?œì¶œ

### 6. Swagger UI ?¬ìš©?˜ê¸°

Postman ?€??ë¸Œë¼?°ì??ì„œ ì§ì ‘ ?ŒìŠ¤?¸í•  ?˜ë„ ?ˆìŠµ?ˆë‹¤:

- **URL**: `http://localhost:9004/docs`
- Swagger UI?ì„œ ëª¨ë“  ?”ë“œ?¬ì¸?¸ë? ?•ì¸?˜ê³  ?ŒìŠ¤?¸í•  ???ˆìŠµ?ˆë‹¤.

### 7. ì£¼ì˜?¬í•­

- ?œë²„ê°€ ?¤í–‰ ì¤‘ì´?´ì•¼ ?©ë‹ˆ??(`localhost:9004`)
- `test.csv`??`Survived` ì»¬ëŸ¼???†ì–´ ?„ì²˜ë¦¬ì—???ëŸ¬ê°€ ë°œìƒ?????ˆìŠµ?ˆë‹¤ (?•ìƒ ?™ì‘)
- ë¡œê·¸??`logs` ë°°ì—´??ë¬¸ì??ë¦¬ìŠ¤?¸ë¡œ ë°˜í™˜?©ë‹ˆ??
- ê°?ë¡œê·¸ ??ª©?€ `ic|` ?‘ë‘?¬ê? ?¬í•¨?????ˆìŠµ?ˆë‹¤ (icecream ?¼ì´ë¸ŒëŸ¬ë¦?ì¶œë ¥)

### 8. ë¬¸ì œ ?´ê²°

#### ?œë²„???°ê²°?????†ëŠ” ê²½ìš°
- ?œë²„ê°€ ?¤í–‰ ì¤‘ì¸ì§€ ?•ì¸: `http://localhost:9004/health`
- ?¬íŠ¸ê°€ ?¬ë°”ë¥¸ì? ?•ì¸ (ê¸°ë³¸ê°? 9004)

#### ë¡œê·¸ê°€ ë¹„ì–´?ˆëŠ” ê²½ìš°
- icecream??ì¶œë ¥??ìº¡ì²˜?˜ì? ?Šì„ ???ˆìŠµ?ˆë‹¤
- ?œë²„ ?°ë??ì—??ì§ì ‘ ë¡œê·¸ë¥??•ì¸?˜ì„¸??

#### ?ëŸ¬ê°€ ë°œìƒ?˜ëŠ” ê²½ìš°
- ?‘ë‹µ??`error` ?„ë“œë¥??•ì¸?˜ì„¸??
- ?œë²„ ?°ë??ì˜ ?„ì²´ ?ëŸ¬ ë©”ì‹œì§€ë¥??•ì¸?˜ì„¸??

