# -*- coding: utf-8 -*-
"""
네이버 영화 리뷰 감성 분류 - 2단계: 모델 학습 (TF-IDF + Logistic Regression)
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import cross_val_score
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import time
import warnings
warnings.filterwarnings('ignore')

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

print("="*70)
print("네이버 영화 리뷰 감성 분류 - 모델 학습")
print("="*70)

# ============================================================
# 1. 데이터 로드
# ============================================================
print("\n[1단계] 전처리된 데이터 로드")

try:
    train_df = pd.read_csv('ratings_train_clean.csv')
    test_df = pd.read_csv('ratings_test_clean.csv')
    print(f"✅ 학습 데이터: {len(train_df):,}개")
    print(f"✅ 테스트 데이터: {len(test_df):,}개")
except FileNotFoundError:
    print("❌ 전처리된 데이터가 없습니다!")
    print("먼저 01_eda.py를 실행해주세요.")
    exit()

# ============================================================
# 2. 데이터 준비
# ============================================================
print("\n[2단계] 데이터 준비")

X_train = train_df['document_clean'].values
y_train = train_df['label'].values

X_test = test_df['document_clean'].values
y_test = test_df['label'].values

print(f"학습 데이터: {X_train.shape}, 레이블: {y_train.shape}")
print(f"테스트 데이터: {X_test.shape}, 레이블: {y_test.shape}")

# ============================================================
# 3. TF-IDF 벡터화
# ============================================================
print("\n[3단계] TF-IDF 벡터화")
print("⏳ 벡터화 진행 중... (몇 분 소요될 수 있습니다)")

start_time = time.time()

# TF-IDF Vectorizer 설정
vectorizer = TfidfVectorizer(
    max_features=10000,      # 상위 10,000개 단어만 사용
    min_df=2,                # 최소 2개 문서에 등장해야 함
    max_df=0.8,              # 80% 이상의 문서에 등장하면 제외 (불용어 효과)
    ngram_range=(1, 2),      # 1-gram, 2-gram 모두 사용
    sublinear_tf=True        # TF에 로그 스케일 적용
)

# 학습 데이터로 fit & transform
X_train_tfidf = vectorizer.fit_transform(X_train)

# 테스트 데이터는 transform만
X_test_tfidf = vectorizer.transform(X_test)

elapsed_time = time.time() - start_time

print(f"✅ 벡터화 완료! (소요 시간: {elapsed_time:.2f}초)")
print(f"학습 데이터 shape: {X_train_tfidf.shape}")
print(f"테스트 데이터 shape: {X_test_tfidf.shape}")
print(f"사용된 단어(특성) 개수: {len(vectorizer.get_feature_names_out()):,}개")

# TF-IDF 벡터라이저 저장
joblib.dump(vectorizer, 'tfidf_vectorizer.pkl')
print("✅ TF-IDF 벡터라이저 저장: tfidf_vectorizer.pkl")

# ============================================================
# 4. 모델 학습
# ============================================================
print("\n[4단계] Logistic Regression 모델 학습")
print("⏳ 학습 진행 중...")

start_time = time.time()

# Logistic Regression 모델
model = LogisticRegression(
    max_iter=1000,           # 최대 반복 횟수
    C=1.0,                   # 정규화 강도 (작을수록 강함)
    random_state=42,
    solver='lbfgs',          # 최적화 알고리즘
    n_jobs=-1                # 모든 CPU 코어 사용
)

# 학습
model.fit(X_train_tfidf, y_train)

elapsed_time = time.time() - start_time

print(f"✅ 모델 학습 완료! (소요 시간: {elapsed_time:.2f}초)")

# 모델 저장
joblib.dump(model, 'sentiment_model.pkl')
print("✅ 모델 저장: sentiment_model.pkl")

# ============================================================
# 5. 교차 검증
# ============================================================
print("\n[5단계] 교차 검증 (5-Fold)")
print("⏳ 검증 진행 중... (시간이 다소 걸릴 수 있습니다)")

# 샘플링해서 빠르게 교차 검증 (전체 데이터로 하면 시간이 오래 걸림)
sample_size = 20000
sample_indices = np.random.choice(len(X_train), sample_size, replace=False)
X_train_sample = X_train_tfidf[sample_indices]
y_train_sample = y_train[sample_indices]

start_time = time.time()
cv_scores = cross_val_score(model, X_train_sample, y_train_sample, cv=5, scoring='accuracy', n_jobs=-1)
elapsed_time = time.time() - start_time

print(f"✅ 교차 검증 완료! (소요 시간: {elapsed_time:.2f}초)")
print(f"CV 점수: {cv_scores}")
print(f"평균 정확도: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")

# ============================================================
# 6. 학습 데이터 예측 및 평가
# ============================================================
print("\n[6단계] 학습 데이터 평가")

y_train_pred = model.predict(X_train_tfidf)
train_accuracy = accuracy_score(y_train, y_train_pred)

print(f"학습 데이터 정확도: {train_accuracy:.4f} ({train_accuracy*100:.2f}%)")

# ============================================================
# 7. 테스트 데이터 예측 및 평가
# ============================================================
print("\n[7단계] 테스트 데이터 평가")

y_test_pred = model.predict(X_test_tfidf)
test_accuracy = accuracy_score(y_test, y_test_pred)

print(f"테스트 데이터 정확도: {test_accuracy:.4f} ({test_accuracy*100:.2f}%)")

# 분류 리포트
print("\n📊 상세 분류 리포트:")
print(classification_report(y_test, y_test_pred, 
                          target_names=['부정(0)', '긍정(1)'],
                          digits=4))

# ============================================================
# 8. Confusion Matrix 시각화
# ============================================================
print("\n[8단계] Confusion Matrix 생성")

cm = confusion_matrix(y_test, y_test_pred)

plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=['부정(0)', '긍정(1)'],
            yticklabels=['부정(0)', '긍정(1)'],
            cbar_kws={'label': '개수'})
plt.title('Confusion Matrix', fontsize=14, fontweight='bold')
plt.ylabel('실제 레이블', fontsize=12)
plt.xlabel('예측 레이블', fontsize=12)

# 정확도 표시
for i in range(2):
    for j in range(2):
        value = cm[i, j]
        total = cm[i].sum()
        percentage = value / total * 100
        plt.text(j + 0.5, i + 0.7, f'({percentage:.1f}%)', 
                ha='center', va='center', fontsize=10, color='gray')

plt.tight_layout()
plt.savefig('03_confusion_matrix.png', dpi=300, bbox_inches='tight')
print("✅ Confusion Matrix 저장: 03_confusion_matrix.png")
plt.close()

# ============================================================
# 9. 주요 특성(단어) 분석
# ============================================================
print("\n[9단계] 주요 특성(단어) 분석")

# 모델의 계수 추출
feature_names = vectorizer.get_feature_names_out()
coefficients = model.coef_[0]

# 긍정적 영향을 미치는 단어 (계수가 큰 단어)
top_positive_idx = np.argsort(coefficients)[-20:][::-1]
top_positive_words = [(feature_names[i], coefficients[i]) for i in top_positive_idx]

# 부정적 영향을 미치는 단어 (계수가 작은 단어)
top_negative_idx = np.argsort(coefficients)[:20]
top_negative_words = [(feature_names[i], coefficients[i]) for i in top_negative_idx]

print("\n✨ 긍정 예측에 가장 영향을 주는 단어 TOP 20:")
print("="*70)
for i, (word, coef) in enumerate(top_positive_words, 1):
    print(f"{i:2d}. {word:20s} (계수: {coef:8.4f})")

print("\n💔 부정 예측에 가장 영향을 주는 단어 TOP 20:")
print("="*70)
for i, (word, coef) in enumerate(top_negative_words, 1):
    print(f"{i:2d}. {word:20s} (계수: {coef:8.4f})")

# 시각화
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# 긍정 단어
pos_words = [w for w, _ in top_positive_words]
pos_coefs = [c for _, c in top_positive_words]
axes[0].barh(range(len(pos_words)), pos_coefs, color='#4ecdc4')
axes[0].set_yticks(range(len(pos_words)))
axes[0].set_yticklabels(pos_words)
axes[0].set_xlabel('계수 값', fontsize=11)
axes[0].set_title('긍정 예측에 영향을 주는 단어 TOP 20', fontsize=12, fontweight='bold')
axes[0].invert_yaxis()

# 부정 단어
neg_words = [w for w, _ in top_negative_words]
neg_coefs = [c for _, c in top_negative_words]
axes[1].barh(range(len(neg_words)), neg_coefs, color='#ff6b6b')
axes[1].set_yticks(range(len(neg_words)))
axes[1].set_yticklabels(neg_words)
axes[1].set_xlabel('계수 값', fontsize=11)
axes[1].set_title('부정 예측에 영향을 주는 단어 TOP 20', fontsize=12, fontweight='bold')
axes[1].invert_yaxis()

plt.tight_layout()
plt.savefig('04_feature_importance.png', dpi=300, bbox_inches='tight')
print("\n✅ 특성 중요도 그래프 저장: 04_feature_importance.png")
plt.close()

# ============================================================
# 10. 최종 요약
# ============================================================
print("\n" + "="*70)
print("📊 최종 모델 성능 요약")
print("="*70)

print(f"\n✅ 모델: Logistic Regression")
print(f"✅ 특성 추출: TF-IDF (max_features=10,000)")
print(f"\n📈 성능:")
print(f"  - 학습 데이터 정확도: {train_accuracy:.4f} ({train_accuracy*100:.2f}%)")
print(f"  - 테스트 데이터 정확도: {test_accuracy:.4f} ({test_accuracy*100:.2f}%)")
print(f"  - 교차 검증 평균: {cv_scores.mean():.4f} ({cv_scores.mean()*100:.2f}%)")

print(f"\n💾 저장된 파일:")
print(f"  - tfidf_vectorizer.pkl (TF-IDF 벡터라이저)")
print(f"  - sentiment_model.pkl (학습된 모델)")
print(f"  - 03_confusion_matrix.png (혼동 행렬)")
print(f"  - 04_feature_importance.png (특성 중요도)")

print("\n" + "="*70)
print("🎉 모델 학습 완료!")
print("다음 단계: 03_predict.py로 새로운 리뷰 예측")
print("="*70)

