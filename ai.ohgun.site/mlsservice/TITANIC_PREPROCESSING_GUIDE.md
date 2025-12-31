# ?€?´í????°ì´???„ì²˜ë¦?ê°€?´ë“œ

## ëª©ì°¨
1. [?„ì²˜ë¦?ê°œìš”](#?„ì²˜ë¦?ê°œìš”)
2. [?„ì²˜ë¦?ì½”ë“œ ?ì„¸ ?¤ëª…](#?„ì²˜ë¦?ì½”ë“œ-?ì„¸-?¤ëª…)
3. [?°ì´???€?…ë³„ ì²˜ë¦¬ ë°©ë²•](#?°ì´???€?…ë³„-ì²˜ë¦¬-ë°©ë²•)
4. [?„ì²˜ë¦??„í›„ ë¹„êµ](#?„ì²˜ë¦??„í›„-ë¹„êµ)
5. [ì£¼ìš” ê°œë… ?•ë¦¬](#ì£¼ìš”-ê°œë…-?•ë¦¬)

---

## ?„ì²˜ë¦?ê°œìš”

### ???„ì²˜ë¦¬ê? ?„ìš”?œê??
ë¨¸ì‹ ?¬ë‹ ëª¨ë¸?€ **ê¹¨ë—?˜ê³  ?•í˜•?”ëœ ?«ì ?°ì´??*ë§??™ìŠµ?????ˆìŠµ?ˆë‹¤. ?˜ì?ë§??¤ì œ ?°ì´?°ëŠ”:
- ??ê²°ì¸¡ì¹?Null)ê°€ ?ˆìŒ
- ???ìŠ¤???°ì´?°ê? ?¬í•¨??(?´ë¦„, ?°ì¼“ ë²ˆí˜¸ ??
- ??ë²”ì£¼???°ì´?°ê? ë¬¸ì?´ë¡œ ?œí˜„??(?±ë³„: male/female)
- ???˜ì¹˜ ë²”ìœ„ê°€ ?ˆë¬´ ?“ê±°??ë¶„í¬ê°€ ì¹˜ìš°ì³??ˆìŒ

?„ì²˜ë¦¬ëŠ” ?´ëŸ¬??**? ê²ƒ(raw) ?°ì´?°ë? ëª¨ë¸???™ìŠµ ê°€?¥í•œ ?•íƒœë¡?ë³€??*?˜ëŠ” ê³¼ì •?…ë‹ˆ??

### ?€?´í????°ì´?°ì…‹ êµ¬ì¡°
- **?™ìŠµ ?°ì´??train.csv)**: 891ê°??? 12ê°?ì»¬ëŸ¼ (Survived ?¬í•¨)
- **?ŒìŠ¤???°ì´??test.csv)**: 418ê°??? 11ê°?ì»¬ëŸ¼ (Survived ?†ìŒ)

---

## ?„ì²˜ë¦?ì½”ë“œ ?ì„¸ ?¤ëª…

### 1. ì´ˆê¸°??ë°??°ì´??ë¡œë“œ

```python
def preprogress(self):
    ic("?˜Š?˜Š ?„ì²˜ë¦??œì‘")
```
**?¤ëª…**: ë©”ì„œ???œì‘???Œë¦¬??ë¡œê·¸ ì¶œë ¥
- `ic`: icecream ?¼ì´ë¸ŒëŸ¬ë¦?(?”ë²„ê¹…ìš© print)

---

```python
    the_method = TitanicMethod()
```
**?¤ëª…**: `TitanicMethod` ?´ë˜???¸ìŠ¤?´ìŠ¤ ?ì„±
- ??ê°ì²´ë¥??µí•´ ëª¨ë“  ?°ì´??ì²˜ë¦¬ ë©”ì„œ?œë? ?¸ì¶œ?©ë‹ˆ??
- ?¬ì‚¬??ê°€?¥í•œ ë©”ì„œ?œë“¤??ìº¡ìŠ?”í•œ ?´ë˜??

---

```python
    df_train = the_method.new_model('train.csv')
    df_test = the_method.new_model('test.csv')
```
**?¤ëª…**: CSV ?Œì¼??pandas DataFrame?¼ë¡œ ë¡œë“œ
- `train.csv`: ?™ìŠµ???°ì´??(Survived ì»¬ëŸ¼ ?¬í•¨)
- `test.csv`: ?ŒìŠ¤???ˆì¸¡???°ì´??(Survived ì»¬ëŸ¼ ?†ìŒ)
- `pd.read_csv()`ë¥??´ë??ìœ¼ë¡??¬ìš©

**?ë³¸ ?°ì´???ˆì‹œ**:
```
PassengerId  Survived  Pclass  Name                 Sex     Age  SibSp  Parch  Ticket    Fare   Cabin  Embarked
1            0         3       Braund, Mr. Owen     male    22   1      0      A/5 21171 7.25   NaN    S
2            1         1       Cumings, Mrs. John   female  38   1      0      PC 17599  71.28  C85    C
```

---

### 2. ?ˆì´ë¸?Survived) ë¶„ë¦¬

```python
    this_train = the_method.create_train(df_train, 'Survived')
```
**?¤ëª…**: `df_train`?ì„œ **'Survived' ì»¬ëŸ¼???œê±°**
- ?˜ë¨¸ì§€ ?¼ì²˜?¤ë§Œ `this_train`???€??
- **??ë¶„ë¦¬?˜ë‚˜??**
  - ë¨¸ì‹ ?¬ë‹ ?™ìŠµ ???¼ì²˜(X)?€ ?ˆì´ë¸?y)??ë¶„ë¦¬?´ì•¼ ??
  - ?¼ì²˜(X): ?…ë ¥ ?°ì´??(?˜ì´, ?±ë³„, ê°ì‹¤ ?±ê¸‰ ??
  - ?ˆì´ë¸?y): ?ˆì¸¡ ?€??(?ì¡´ ?¬ë?)

**?´ë? ì½”ë“œ**:
```python
def create_train(self, df: pd.DataFrame, label: str) -> pd.DataFrame:
    return df.drop(columns=[label])
```

---

### 3. ?ŒìŠ¤???°ì´??Survived ì»¬ëŸ¼ ì²´í¬

```python
    if 'Survived' in df_test.columns:
        this_test = the_method.create_train(df_test, 'Survived')
    else:
        this_test = df_test  # Survived ì»¬ëŸ¼???†ìœ¼ë©?ê·¸ë?ë¡??¬ìš©
        ic("Test ?°ì´?°ì—??Survived ì»¬ëŸ¼???†ìŠµ?ˆë‹¤ (?ˆì¸¡???°ì´??")
```
**?¤ëª…**: ?ŒìŠ¤???°ì´?°ì˜ Survived ì»¬ëŸ¼ ì¡´ì¬ ?¬ë? ?•ì¸
- `test.csv`?ëŠ” ë³´í†µ Survived ì»¬ëŸ¼???†ìŒ (?ˆì¸¡ ?€?ì´ë¯€ë¡?
- ?ˆìœ¼ë©??œê±°, ?†ìœ¼ë©?ê·¸ë?ë¡??¬ìš©
- **?ëŸ¬ ë°©ì?ë¥??„í•œ ?ˆì „?¥ì¹˜**

---

### 4. ?„ì²˜ë¦????íƒœ ì¶œë ¥

```python
    ic(f'1. Train ???ìœ„ 5ê°???n {this_train.head(5).to_dict(orient="records")} ')
```
**?¤ëª…**: ?°ì´?°ì˜ ?ìœ„ 5ê°??‰ì„ ?•ì…”?ˆë¦¬ ë¦¬ìŠ¤???•íƒœë¡?ì¶œë ¥
- `head(5)`: ?ìœ„ 5ê°??‰ë§Œ ê°€?¸ì˜¤ê¸?
- `to_dict(orient="records")`: ê°??‰ì„ ?•ì…”?ˆë¦¬ë¡?ë³€??
  ```python
  [
    {'PassengerId': 1, 'Pclass': 3, 'Name': '...', 'Age': 22, ...},
    {'PassengerId': 2, 'Pclass': 1, 'Name': '...', 'Age': 38, ...},
    ...
  ]
  ```
- JSON ì§ë ¬??ê°€?¥í•œ ?•íƒœ (API ?‘ë‹µ???¬ìš© ê°€??

---

```python
    ic(f'2. Train ??null ??ê°?ˆ˜\n {this_train.isnull().sum().to_dict()}ê°?)
```
**?¤ëª…**: ê°?ì»¬ëŸ¼ë³?ê²°ì¸¡ì¹?Null) ê°œìˆ˜ ì¶œë ¥
- `isnull()`: ê°??€??null?¸ì? True/False ë°˜í™˜
- `.sum()`: ê°?ì»¬ëŸ¼ë³„ë¡œ True(null) ê°œìˆ˜ ?©ì‚°
- `to_dict()`: ?•ì…”?ˆë¦¬ë¡?ë³€??

**ì¶œë ¥ ?ˆì‹œ**:
```python
{
  'PassengerId': 0,
  'Pclass': 0,
  'Name': 0,
  'Sex': 0,
  'Age': 177,      # 177ê°œì˜ ?˜ì´ ?•ë³´ ?„ë½
  'SibSp': 0,
  'Parch': 0,
  'Ticket': 0,
  'Fare': 0,
  'Cabin': 687,    # 687ê°œì˜ ê°ì‹¤ ?•ë³´ ?„ë½
  'Embarked': 2    # 2ê°œì˜ ?¹ì„  ??µ¬ ?•ë³´ ?„ë½
}
```

---

### 5. ë¶ˆí•„?”í•œ ?¼ì²˜ ?? œ

```python
    drop_features = ['SibSp', 'Parch', 'Cabin', 'Ticket']
    the_method.drop_feature(this_train, *drop_features)
```
**?¤ëª…**: ëª¨ë¸ ?™ìŠµ??ë¶ˆí•„?”í•˜ê±°ë‚˜ ?ˆì§ˆ????? ?¼ì²˜ ?œê±°

#### ?? œ ?´ìœ 
| ì»¬ëŸ¼ | ?˜ë? | ?? œ ?´ìœ  |
|------|------|-----------|
| **SibSp** | Siblings/Spouse (?•ì œ/ë°°ìš°???? | ê°€ì¡?ê´€ê³??•ë³´??ë³µì¡?˜ê³  ?ˆì¸¡?¥ì´ ??Œ |
| **Parch** | Parents/Children (ë¶€ëª??ë? ?? | ê°€ì¡?ê´€ê³??•ë³´??ë³µì¡?˜ê³  ?ˆì¸¡?¥ì´ ??Œ |
| **Cabin** | ê°ì‹¤ ë²ˆí˜¸ | **Null??687ê°?*(77%)ë¡??ˆë¬´ ë§ì•„???¬ìš© ë¶ˆê? |
| **Ticket** | ?°ì¼“ ë²ˆí˜¸ | ë¬´ì‘??ë¬¸ì?´ë¡œ ?ˆì¸¡???„ì? ????|

**`*drop_features` ?¸íŒ¨??*:
```python
# ?´ë ‡ê²??¸ì¶œ??
drop_feature(this_train, 'SibSp', 'Parch', 'Cabin', 'Ticket')

# ë©”ì„œ???•ì˜
def drop_feature(self, df: pd.DataFrame, *features: str) -> pd.DataFrame:
    return df.drop(columns=list(features))
```

---

### 6. Pclass (ê°ì‹¤ ?±ê¸‰) - Ordinal ì²˜ë¦¬

```python
    this_train = the_method.pclass_ordinal(this_train)
```
**?¤ëª…**: ê°ì‹¤ ?±ê¸‰ ?°ì´?°ë? Ordinal(?œì„œ?? ?°ì´?°ë¡œ ì²˜ë¦¬
- **Ordinal**: ?œì„œê°€ ?ˆëŠ” ë²”ì£¼???°ì´??
- Pclass: 1?±ê¸‰ > 2?±ê¸‰ > 3?±ê¸‰ (?œì„œ???˜ë? ?ˆìŒ)
- ?´ë? ?«ì(1, 2, 3)ë¡??˜ì–´ ?ˆì–´??ì¶”ê? ë³€??ë¶ˆí•„??

**?´ë? ì²˜ë¦¬**:
```python
def pclass_ordinal(self, df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # Pclass???´ë? 1, 2, 3?¼ë¡œ ?˜ì–´ ?ˆìœ¼ë¯€ë¡?ê·¸ë?ë¡??¬ìš©
    # ?„ìš” ???¤ì??¼ë§ë§??ìš© ê°€??
    return df
```

**??One-Hot Encoding?????˜ë‚˜??**
- Pclass??**?œì„œê°€ ì¤‘ìš”???°ì´??*?´ë?ë¡??«ì ê·¸ë?ë¡?? ì?
- 1?±ê¸‰??3?±ê¸‰ë³´ë‹¤ "??ì¢‹ë‹¤"???œì„œ ?•ë³´ë¥?ë³´ì¡´

---

### 7. Title (?¸ì¹­) - Nominal ì²˜ë¦¬

```python
    this_train = the_method.title_nominal(this_train)
```
**?¤ëª…**: Name?ì„œ ?¸ì¹­??ì¶”ì¶œ?˜ì—¬ ?ˆë¡œ???¼ì²˜ ?ì„±
- **Name**: "Braund, Mr. Owen Harris" ??**Title**: "Mr"

#### ì²˜ë¦¬ ê³¼ì •

**1?¨ê³„: ?•ê·œ?œí˜„?ìœ¼ë¡??¸ì¹­ ì¶”ì¶œ**
```python
df['Title'] = df['Name'].str.extract(r' ([A-Za-z]+)\.')
```
- ?¨í„´: `ê³µë°± + (?ë¬¸??1ê°??´ìƒ) + ë§ˆì¹¨??
- ê²°ê³¼: Mr, Mrs, Miss, Master, Dr, Rev, Col ??

**2?¨ê³„: ?¬ê? ?¸ì¹­ ?µí•©**
```python
rare_titles = ['Dr', 'Rev', 'Col', 'Major', 'Capt', 'Countess', 'Don', 'Dona', 'Lady', 'Sir', 'Jonkheer']
df['Title'] = df['Title'].replace(rare_titles, 'Rare')
```
- ë¹ˆë„ê°€ ??? ?¸ì¹­?¤ì„ 'Rare'ë¡?ê·¸ë£¹??
- ?°ì´???¬ì†Œ??ë¬¸ì œ ?´ê²°

**3?¨ê³„: One-Hot Encoding**
```python
title_dummies = pd.get_dummies(df['Title'], prefix='Title')
df = pd.concat([df, title_dummies], axis=1)
```
- ê°??¸ì¹­??ë³„ë„ ì»¬ëŸ¼?¼ë¡œ ë¶„ë¦¬
- ê²°ê³¼: `Title_Mr`, `Title_Mrs`, `Title_Miss`, `Title_Rare`

**ìµœì¢… ê²°ê³¼**:
```
Name                         ??Title   Title_Mr  Title_Mrs  Title_Miss  Title_Rare
Braund, Mr. Owen Harris      ??Mr      1         0          0           0
Cumings, Mrs. John Bradley   ??Mrs     0         1          0           0
Heikkinen, Miss. Laina       ??Miss    0         0          1           0
```

---

### 8. Gender (?±ë³„) - Nominal ì²˜ë¦¬

```python
    this_train = the_method.gender_nominal(this_train)
```
**?¤ëª…**: ?±ë³„???˜ì¹˜???°ì´?°ë¡œ ë³€??

#### ì²˜ë¦¬ ê³¼ì •

**1?¨ê³„: ì»¬ëŸ¼ëª?ë³€ê²?*
```python
df = df.rename(columns={'Sex': 'Gender'})
```
- `Sex` ??`Gender`ë¡?ëª…ì¹­ ë³€ê²?(?˜ë?????ëª…í™•)

**2?¨ê³„: Label Encoding**
```python
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
df['Gender_encoded'] = le.fit_transform(df['Gender'])
```
- male ??1
- female ??0
- ?œì„œ ?†ëŠ” ?«ì ?¸ì½”??

**3?¨ê³„: One-Hot Encoding**
```python
gender_dummies = pd.get_dummies(df['Gender'], prefix='Gender')
df = pd.concat([df, gender_dummies], axis=1)
```
- `Gender_male`: male?´ë©´ 1, ?„ë‹ˆë©?0
- `Gender_female`: female?´ë©´ 1, ?„ë‹ˆë©?0

**ìµœì¢… ê²°ê³¼**:
```
Sex     ??Gender  Gender_encoded  Gender_male  Gender_female
male    ??male    1               1            0
female  ??female  0               0            1
```

**????ê°€ì§€ ë°©ë²• ëª¨ë‘ ?¬ìš©?˜ë‚˜??**
- **Label Encoding**: ?¼ë? ëª¨ë¸(?¸ë¦¬ ê¸°ë°˜)?ì„œ ?¨ìœ¨??
- **One-Hot Encoding**: ? í˜• ëª¨ë¸?ì„œ ?„ìˆ˜
- ?????œê³µ?˜ì—¬ ëª¨ë¸ ? íƒ ??? ì—°???•ë³´

---

### 9. Age (?˜ì´) - Ratio ì²˜ë¦¬

```python
    this_train = the_method.age_ratio(this_train)
```
**?¤ëª…**: ?°ì†???˜ì´ ?°ì´?°ë? ?•ê·œ?”í•˜ê³?ë²”ì£¼??

#### ì²˜ë¦¬ ê³¼ì •

**1?¨ê³„: Null ê°?ì±„ìš°ê¸?*
```python
df['Age'].fillna(df['Age'].median(), inplace=True)
```
- **?„ëµ**: ì¤‘ì•™ê°?median) ?¬ìš©
- **???‰ê· (mean)???„ë‹Œ ì¤‘ì•™ê°’ì¸ê°€?**
  - ?˜ì´ ?°ì´?°ëŠ” ?´ìƒì¹?outliers)??ë¯¼ê°
  - ì¤‘ì•™ê°’ì´ ???ˆì •?ì¸ ?€??°’

**?ˆì‹œ**:
```
?ë³¸ ?˜ì´ ë¶„í¬: [22, 38, 26, NaN, 35, NaN, 54, ...]
ì¤‘ì•™ê°?median): 28??
ê²°ê³¼: [22, 38, 26, 28, 35, 28, 54, ...]
```

**2?¨ê³„: Binning (êµ¬ê°„??**
```python
df['AgeGroup'] = pd.cut(
    df['Age'], 
    bins=[0, 12, 18, 35, 60, 100], 
    labels=['Child', 'Teen', 'Youth', 'Adult', 'Mature']
)
```
- ?°ì†???°ì´?°ë? ë²”ì£¼?•ìœ¼ë¡?ë³€??
- **êµ¬ê°„ ?•ì˜**:
  - 0-12?? Child (?´ë¦°??
  - 13-18?? Teen (ì²?†Œ??
  - 19-35?? Youth (ì²?…„)
  - 36-60?? Adult (?¥ë…„)
  - 61-100?? Mature (?¸ë…„)

**ìµœì¢… ê²°ê³¼**:
```
Age (?ë³¸)  ??Age (ì±„ì›Œì§?  ??AgeGroup
22          ??22           ??Youth
NaN         ??28           ??Youth
35          ??35           ??Youth
62          ??62           ??Mature
```

**??Binning???˜ë‚˜??**
- ?˜ì´??**ë¹„ì„ ?•ì  ?¨í„´** ?¬ì°©
  - ?? ?´ë¦°?´ì? ?¸ì¸???ì¡´?¨ì´ ?’ì„ ???ˆìŒ
- ëª¨ë¸??ê³¼ì ??overfitting) ë°©ì?
- ë²”ì£¼?•ìœ¼ë¡?ë³€?˜í•˜ë©?One-Hot Encoding ê°€??

---

### 10. Fare (?´ì„) - Ratio ì²˜ë¦¬

```python
    this_train = the_method.fare_ratio(this_train)
```
**?¤ëª…**: ?´ì„ ?°ì´?°ë? ?•ê·œ??

#### ì²˜ë¦¬ ê³¼ì •

**1?¨ê³„: Null ê°?ì±„ìš°ê¸?*
```python
df['Fare'].fillna(df['Fare'].median(), inplace=True)
```
- ì¤‘ì•™ê°’ìœ¼ë¡?ê²°ì¸¡ì¹??€ì²?

**2?¨ê³„: ë¡œê·¸ ë³€??*
```python
df['Fare_log'] = np.log1p(df['Fare'])
```
- `log1p(x)` = `log(1 + x)`

**??ë¡œê·¸ ë³€?˜ì´ ?„ìš”?œê??**

?´ì„ ?°ì´?°ì˜ ë¶„í¬:
```
ìµœì†Œê°? 0
ì¤‘ì•™ê°? 14.45
?‰ê· ê°? 32.20
ìµœë?ê°? 512.33
```
- **ë¬¸ì œ**: ë¶„í¬ê°€ ?¤ë¥¸ìª½ìœ¼ë¡?ì¹˜ìš°ì¹?(right-skewed)
- **?´ê²°**: ë¡œê·¸ ë³€?˜ìœ¼ë¡??•ê·œ ë¶„í¬??ê°€ê¹ê²Œ ë§Œë“¦

**ë³€???ˆì‹œ**:
```
Fare (?ë³¸)  ??Fare_log (ë³€????
7.25         ??log(1 + 7.25) = 2.11
71.28        ??log(1 + 71.28) = 4.28
512.33       ??log(1 + 512.33) = 6.24
```

**?¨ê³¼**:
- ê·¹ë‹¨?ì¸ ê°?outliers)???í–¥ ê°ì†Œ
- ëª¨ë¸ ?™ìŠµ ???˜ë ´ ?ë„ ?¥ìƒ
- ? í˜• ê´€ê³?ê°œì„ 

---

### 11. Embarked (?¹ì„  ??µ¬) - Nominal ì²˜ë¦¬

```python
    this_train = the_method.embarked_nominal(this_train)
```
**?¤ëª…**: ?¹ì„  ??µ¬ë¥?ë²”ì£¼??ë³€?˜ë¡œ ì²˜ë¦¬

#### ì²˜ë¦¬ ê³¼ì •

**1?¨ê³„: Null ê°?ì±„ìš°ê¸?*
```python
df['Embarked'].fillna(df['Embarked'].mode()[0], inplace=True)
```
- **?„ëµ**: ìµœë¹ˆê°?mode) ?¬ìš©
- `mode()[0]`: ê°€??ë§ì´ ?±ì¥?˜ëŠ” ê°?(ë³´í†µ 'S')

**Embarked ê°?ë¶„í¬**:
```
S (Southampton): 644ëª?(72%)  ??ìµœë¹ˆê°?
C (Cherbourg):   168ëª?(19%)
Q (Queenstown):   77ëª?(9%)
NaN:               2ëª?
```

**2?¨ê³„: One-Hot Encoding**
```python
embarked_dummies = pd.get_dummies(df['Embarked'], prefix='Embarked')
df = pd.concat([df, embarked_dummies], axis=1)
```

**ìµœì¢… ê²°ê³¼**:
```
Embarked  ??Embarked_C  Embarked_Q  Embarked_S
S         ??0           0           1
C         ??1           0           0
Q         ??0           1           0
NaN       ??0           0           1  (ìµœë¹ˆê°?Së¡??€ì²?
```

**??One-Hot Encoding?¸ê??**
- Embarked??**?œì„œê°€ ?†ëŠ” ë²”ì£¼???°ì´??* (Nominal)
- S, C, Q ê°„ì— ?¬ê³  ?‘ìŒ???†ìŒ
- ê°ê°???…ë¦½?ì¸ ?¼ì²˜ë¡?ë¶„ë¦¬?´ì•¼ ??

---

### 12. Name ì»¬ëŸ¼ ?? œ

```python
    drop_features = ['Name']
    this_train = the_method.drop_feature(this_train, *drop_features)
```
**?¤ëª…**: ?ë³¸ Name ì»¬ëŸ¼ ?œê±°
- ?´ë? **Titleë¡?ì¶”ì¶œ**?ˆìœ¼ë¯€ë¡??ë³¸ ë¶ˆí•„??
- ?ìŠ¤???°ì´?°ëŠ” ëª¨ë¸??ì§ì ‘ ?™ìŠµ ë¶ˆê???
- ë©”ëª¨ë¦??ˆì•½ ë°??±ëŠ¥ ?¥ìƒ

---

### 13. ?„ì²˜ë¦??„ë£Œ ???íƒœ ì¶œë ¥

```python
    ic("?˜Š?˜Š ?„ì²˜ë¦??„ë£Œ")
    ic(f'1. Train ???ìœ„ 5ê°???n {this_train.head(5).to_dict(orient="records")} ')
    ic(f'2. Train ??null ??ê°?ˆ˜\n {this_train.isnull().sum().to_dict()}ê°?)
```
**?¤ëª…**: ?„ì²˜ë¦????°ì´???íƒœ ?•ì¸
- ?ˆë¡œ???¼ì²˜?¤ì´ ì¶”ê??˜ì—ˆ?”ì? ?•ì¸
- Null ê°’ì´ ?ì ˆ??ì²˜ë¦¬?˜ì—ˆ?”ì? ?•ì¸

---

## ?°ì´???€?…ë³„ ì²˜ë¦¬ ë°©ë²•

### 1. Ordinal (?œì„œ?? ?°ì´??
**?¹ì§•**: ?œì„œê°€ ?˜ë? ?ˆëŠ” ë²”ì£¼???°ì´??
- ?? ê°ì‹¤ ?±ê¸‰ (1?±ê¸‰ > 2?±ê¸‰ > 3?±ê¸‰)
- **ì²˜ë¦¬ ë°©ë²•**: ?«ì ê·¸ë?ë¡?? ì? ?ëŠ” Label Encoding
- **ì£¼ì˜**: One-Hot Encoding ?¬ìš© ???œì„œ ?•ë³´ ?ì‹¤

```python
# Pclass: 1, 2, 3 ê·¸ë?ë¡??¬ìš©
df['Pclass']  # 1, 2, 3
```

---

### 2. Nominal (ëª…ëª©?? ?°ì´??
**?¹ì§•**: ?œì„œê°€ ?†ëŠ” ë²”ì£¼???°ì´??
- ?? ?±ë³„ (male, female), ?¹ì„  ??µ¬ (S, C, Q)
- **ì²˜ë¦¬ ë°©ë²•**: One-Hot Encoding (?„ìˆ˜)
- **?´ìœ **: ?œì„œê°€ ?†ìœ¼ë¯€ë¡?ê°ê°???…ë¦½?ì¸ ?¼ì²˜ë¡?ë¶„ë¦¬

```python
# Gender: male/female ??Gender_male, Gender_female
pd.get_dummies(df['Gender'], prefix='Gender')
```

---

### 3. Ratio (ë¹„ìœ¨/?°ì†?? ?°ì´??
**?¹ì§•**: ?°ì†?ì¸ ?˜ì¹˜ ?°ì´??
- ?? ?˜ì´ (Age), ?´ì„ (Fare)
- **ì²˜ë¦¬ ë°©ë²•**:
  1. Null ê°?ì±„ìš°ê¸?(ì¤‘ì•™ê°??‰ê· ê°?
  2. ?¤ì??¼ë§ (StandardScaler, MinMaxScaler)
  3. ë¡œê·¸ ë³€??(ë¶„í¬ê°€ ì¹˜ìš°ì¹?ê²½ìš°)
  4. Binning (ë²”ì£¼?”ê? ? ë¦¬??ê²½ìš°)

```python
# Age: Null ??median, Binning
df['Age'].fillna(df['Age'].median(), inplace=True)
df['AgeGroup'] = pd.cut(df['Age'], bins=[...], labels=[...])

# Fare: Null ??median, Log ë³€??
df['Fare'].fillna(df['Fare'].median(), inplace=True)
df['Fare_log'] = np.log1p(df['Fare'])
```

---

## ?„ì²˜ë¦??„í›„ ë¹„êµ

### ì»¬ëŸ¼ êµ¬ì¡° ë³€??

#### ?„ì²˜ë¦???(12ê°?ì»¬ëŸ¼)
```
PassengerId, Pclass, Name, Sex, Age, SibSp, Parch, Ticket, Fare, Cabin, Embarked
```

#### ?„ì²˜ë¦???(19ê°?ì»¬ëŸ¼)
```
PassengerId, Pclass, Gender, Age, Ticket, Fare, Cabin, Embarked
+ Title (ì¶”ì¶œ)
+ Gender_encoded, Gender_male, Gender_female (?¸ì½”??
+ AgeGroup (êµ¬ê°„??
+ Fare_log (ë¡œê·¸ ë³€??
+ Embarked_C, Embarked_Q, Embarked_S (One-Hot)
```

---

### Null ê°?ë³€??

| ì»¬ëŸ¼ | ?„ì²˜ë¦???Null | ?„ì²˜ë¦???Null | ì²˜ë¦¬ ë°©ë²• |
|------|----------------|----------------|-----------|
| **Age** | 177ê°?(20%) | 0ê°???| ì¤‘ì•™ê°’ìœ¼ë¡?ì±„ì? |
| **Embarked** | 2ê°?(0.2%) | 0ê°???| ìµœë¹ˆê°’ìœ¼ë¡?ì±„ì? |
| **Cabin** | 687ê°?(77%) | 687ê°?(? ì?) | ?? œ ?ˆì • |
| **Fare** | 0ê°?| 0ê°???| ?ë˜ ?†ìŒ |

---

### ?°ì´???ˆì‹œ ë¹„êµ

#### ?„ì²˜ë¦???
```
PassengerId  Pclass  Name                  Sex     Age   Fare    Embarked
1            3       Braund, Mr. Owen      male    22    7.25    S
2            1       Cumings, Mrs. John    female  38    71.28   C
3            3       Heikkinen, Miss.      female  26    7.93    S
```

#### ?„ì²˜ë¦???
```
PassengerId  Pclass  Gender  Age  Title  Gender_encoded  Gender_male  Gender_female  AgeGroup  Fare_log  Embarked_C  Embarked_Q  Embarked_S
1            3       male    22   Mr     1               1            0              Youth     2.11      0           0           1
2            1       female  38   Mrs    0               0            1              Mature    4.28      1           0           0
3            3       female  26   Miss   0               0            1              Adult     2.19      0           0           1
```

---

## ì£¼ìš” ê°œë… ?•ë¦¬

### 1. ê²°ì¸¡ì¹?ì²˜ë¦¬ ?„ëµ

| ?°ì´???€??| ì¶”ì²œ ë°©ë²• | ?´ìœ  |
|------------|----------|------|
| **?˜ì¹˜??* | ì¤‘ì•™ê°?median) | ?´ìƒì¹˜ì— ??ë¯¼ê° |
| **ë²”ì£¼??* | ìµœë¹ˆê°?mode) | ê°€???”í•œ ê°’ìœ¼ë¡??€ì²?|
| **?ìŠ¤??* | 'Unknown' ?ëŠ” ?œê±° | ?˜ë? ?ˆëŠ” ?€??°’ ?†ìŒ |
| **Null ë¹„ìœ¨ > 70%** | ì»¬ëŸ¼ ?? œ | ?•ë³´?‰ì´ ?ˆë¬´ ?ìŒ (?? Cabin) |

---

### 2. ?¸ì½”??ë°©ë²• ? íƒ

```mermaid
graph TD
    A[ë²”ì£¼???°ì´?? --> B{?œì„œê°€ ?ˆëŠ”ê°€?}
    B -->|?ˆìŒ| C[Ordinal]
    B -->|?†ìŒ| D[Nominal]
    C --> E[Label Encoding<br/>?ëŠ” ?«ì ? ì?]
    D --> F[One-Hot Encoding]
```

#### Label Encoding
- **?¬ìš© ?œê¸°**: ?œì„œ???ëŠ” ?´ì§„(binary) ?°ì´??
- **??*: male=0, female=1
- **?¥ì **: ì»¬ëŸ¼ ??ì¦ê? ?†ìŒ
- **?¨ì **: ?œì„œ ?•ë³´ê°€ ?†ëŠ”???¬ìš©?˜ë©´ ëª¨ë¸???˜ëª» ?™ìŠµ

#### One-Hot Encoding
- **?¬ìš© ?œê¸°**: ëª…ëª©???°ì´??
- **??*: Embarked ??Embarked_S, Embarked_C, Embarked_Q
- **?¥ì **: ?œì„œ ?•ë³´ ?¤í•´ ë°©ì?
- **?¨ì **: ì»¬ëŸ¼ ??ì¦ê? (ì°¨ì›???€ì£?

---

### 3. ?¤ì??¼ë§ (Scaling)

#### ???„ìš”?œê??
- ?¼ì²˜ ê°?**?¨ìœ„?€ ë²”ìœ„ê°€ ?¤ë¥´ë©?* ëª¨ë¸ ?™ìŠµ???…ì˜??
- ?? Age(0-100) vs Fare(0-500) ??Fareê°€ ê³¼ë„?˜ê²Œ ?í–¥

#### ì£¼ìš” ë°©ë²•

**StandardScaler (?œì???**
```python
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
df['Age_scaled'] = scaler.fit_transform(df[['Age']])
```
- ?‰ê· =0, ?œì??¸ì°¨=1ë¡?ë³€??
- **?¬ìš© ?œê¸°**: ?•ê·œ ë¶„í¬??ê°€ê¹Œìš´ ?°ì´??

**MinMaxScaler (?•ê·œ??**
```python
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
df['Fare_scaled'] = scaler.fit_transform(df[['Fare']])
```
- 0-1 ë²”ìœ„ë¡?ë³€??
- **?¬ìš© ?œê¸°**: ë¶„í¬ ëª¨ì–‘ ? ì??˜ë©´??ë²”ìœ„ë§?ì¡°ì •

**Log Transformation (ë¡œê·¸ ë³€??**
```python
df['Fare_log'] = np.log1p(df['Fare'])
```
- ì¹˜ìš°ì¹?ë¶„í¬ë¥??•ê·œ ë¶„í¬??ê°€ê¹ê²Œ ë³€??
- **?¬ìš© ?œê¸°**: ?¤ë¥¸ìª½ìœ¼ë¡?ì¹˜ìš°ì¹?right-skewed) ?°ì´??

---

### 4. Feature Engineering ì²´í¬ë¦¬ìŠ¤??

#### ???„ì²˜ë¦??„ë£Œ ê¸°ì?
- [ ] **ê²°ì¸¡ì¹?0ê°?* (?ëŠ” ?? œ)
- [ ] **ëª¨ë“  ?°ì´?°ê? ?«ì??*
- [ ] **ë²”ì£¼???°ì´???¸ì½”???„ë£Œ**
- [ ] **?´ìƒì¹?ì²˜ë¦¬ ?„ë£Œ**
- [ ] **?¤ì??¼ë§ ?„ë£Œ** (?„ìš” ??
- [ ] **ë¶ˆí•„?”í•œ ?¼ì²˜ ?œê±°** (ID, ?´ë¦„, ?°ì¼“ ??

#### ???”í•œ ?¤ìˆ˜
- Nominal ?°ì´?°ì— Label Encoding ?¬ìš©
- Null ê°?ê·¸ë?ë¡??ê¸°
- ?ìŠ¤???°ì´?°ë? ?«ìë¡?ë³€??????
- ?´ìƒì¹˜ë? ë¬´ì‹œ
- Train/Test???¤ë¥¸ ?„ì²˜ë¦??ìš©

---

## ?¤ìŒ ?¨ê³„

?„ì²˜ë¦¬ê? ?„ë£Œ?˜ë©´ ?¤ìŒ ?¨ê³„ë¡?ì§„í–‰?©ë‹ˆ??

1. **Feature Selection** (?¼ì²˜ ? íƒ)
   - ì¤‘ìš”?„ê? ??? ?¼ì²˜ ?œê±°
   - ?¤ì¤‘ê³µì„ ??multicollinearity) ì²´í¬

2. **Modeling** (ëª¨ë¸ë§?
   - ëª¨ë¸ ? íƒ (RandomForest, XGBoost, LogisticRegression ??
   - ?˜ì´?¼íŒŒ?¼ë????œë‹

3. **Learning** (?™ìŠµ)
   - Train/Validation ë¶„í• 
   - ëª¨ë¸ ?™ìŠµ ë°?ê²€ì¦?

4. **Evaluating** (?‰ê?)
   - ?•í™•??Accuracy), ?•ë???Precision), ?¬í˜„??Recall) ê³„ì‚°
   - Confusion Matrix ë¶„ì„

5. **Submit** (?œì¶œ)
   - ?ŒìŠ¤???°ì´???ˆì¸¡
   - ê²°ê³¼ ?Œì¼ ?ì„±

---

## ì°¸ê³  ?ë£Œ

### ì£¼ìš” ?¼ì´ë¸ŒëŸ¬ë¦?
- **pandas**: ?°ì´??ì²˜ë¦¬ ë°?ì¡°ì‘
- **numpy**: ?˜ì¹˜ ?°ì‚°
- **sklearn.preprocessing**: ?¸ì½”??ë°??¤ì??¼ë§
- **sklearn.model_selection**: ?°ì´??ë¶„í• 

### ? ìš©??pandas ë©”ì„œ??
```python
# ?°ì´???•ì¸
df.head()           # ?ìœ„ 5ê°???
df.info()           # ?°ì´???€??ë°?Null ?•ë³´
df.describe()       # ?µê³„ ?”ì•½
df.isnull().sum()   # Null ê°œìˆ˜

# ?°ì´??ì²˜ë¦¬
df.fillna()         # Null ê°?ì±„ìš°ê¸?
df.drop()           # ??ì»¬ëŸ¼ ?? œ
df.rename()         # ì»¬ëŸ¼ëª?ë³€ê²?
df.replace()        # ê°??€ì²?

# ?°ì´??ë³€??
pd.cut()            # Binning (êµ¬ê°„??
pd.get_dummies()    # One-Hot Encoding
df.str.extract()    # ë¬¸ì??ì¶”ì¶œ
```

---

## ?°ìŠµ ë¬¸ì œ

### Q1: ?¤ìŒ ?°ì´?°ì˜ ?„ì²˜ë¦??„ëµ???˜ë¦½?˜ì„¸??
```
Education: ['High School', 'Bachelor', 'Master', 'PhD']
```
<details>
<summary>?•ë‹µ ë³´ê¸°</summary>

**Ordinal ?°ì´??* (?œì„œ ?ˆìŒ)
- Label Encoding: High School=0, Bachelor=1, Master=2, PhD=3
- ?ëŠ” ?œì„œ ë³´ì¡´ ë§¤í•‘
</details>

---

### Q2: ?¤ìŒ ?°ì´?°ì˜ Null ê°?ì²˜ë¦¬ ë°©ë²•???œì•ˆ?˜ì„¸??
```
Income: [50000, 60000, NaN, 75000, 1000000, NaN]
```
<details>
<summary>?•ë‹µ ë³´ê¸°</summary>

**ì¤‘ì•™ê°?median) ?¬ìš©**
- ?´ìœ : 1,000,000???´ìƒì¹˜ì´ë¯€ë¡??‰ê· ê°’ì? ë¶€?ì ˆ
- median = 60,000 (?´ìƒì¹˜ì— ??ë¯¼ê°)
</details>

---

### Q3: ?¤ìŒ ?°ì´?°ì— ë¡œê·¸ ë³€?˜ì´ ?„ìš”?œê???
```
Height (cm): [160, 165, 170, 175, 180]
```
<details>
<summary>?•ë‹µ ë³´ê¸°</summary>

**?„ìš” ?†ìŒ**
- ë¶„í¬ê°€ ê· ë“±?˜ê³  ?•ê·œ ë¶„í¬??ê°€ê¹Œì?
- ë²”ìœ„ê°€ ?“ì? ?ŠìŒ (160-180)
- StandardScaler ?ëŠ” MinMaxScalerë§??ìš©
</details>

---

## ë§ˆë¬´ë¦?

??ê°€?´ë“œ???€?´í????°ì´?°ì…‹???„ì²˜ë¦?ê³¼ì •???™ìŠµ?˜ê¸° ?„í•œ ?ë£Œ?…ë‹ˆ??
- ê°??¨ê³„??**?´ìœ **?€ **?¨ê³¼**ë¥??´í•´?˜ëŠ” ê²ƒì´ ì¤‘ìš”?©ë‹ˆ??
- ?¤ë¥¸ ?°ì´?°ì…‹?ë„ **?™ì¼???ì¹™**???ìš©?????ˆìŠµ?ˆë‹¤.
- ?¤ë¬´?ì„œ??**?°ì´???¹ì„±??ë§ëŠ” ?„ëµ**??? íƒ?´ì•¼ ?©ë‹ˆ??

ì§ˆë¬¸?´ë‚˜ ê°œì„  ?¬í•­???ˆë‹¤ë©??¸ì œ? ì? ë¬¸ì˜?˜ì„¸?? ??

---

**?‘ì„±??*: 2025-12-08  
**ë²„ì „**: 1.0  
**?‘ì„±??*: AI Assistant

