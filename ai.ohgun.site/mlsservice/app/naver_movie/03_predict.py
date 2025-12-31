# -*- coding: utf-8 -*-
"""
네이버 영화 리뷰 감성 분류 - 3단계: 예측 및 활용
"""

import joblib
import pandas as pd
import numpy as np
import re

print("="*70)
print("네이버 영화 리뷰 감성 분류 - 예측 시스템")
print("="*70)

# ============================================================
# 1. 모델 로드
# ============================================================
print("\n[1단계] 학습된 모델 로드")

try:
    vectorizer = joblib.load('tfidf_vectorizer.pkl')
    model = joblib.load('sentiment_model.pkl')
    print("✅ 모델 로드 완료!")
except FileNotFoundError:
    print("❌ 모델 파일이 없습니다!")
    print("먼저 02_train_model.py를 실행해주세요.")
    exit()

# ============================================================
# 2. 전처리 함수
# ============================================================
def clean_text(text):
    """텍스트 전처리 함수"""
    if not isinstance(text, str):
        return ""
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    return text

# ============================================================
# 3. 예측 함수
# ============================================================
def predict_sentiment(review):
    """
    리뷰의 감성을 예측하는 함수
    
    Parameters:
    -----------
    review : str
        예측할 리뷰 텍스트
    
    Returns:
    --------
    dict : 예측 결과 (label, probability, sentiment)
    """
    # 전처리
    cleaned_review = clean_text(review)
    
    # 벡터화
    review_tfidf = vectorizer.transform([cleaned_review])
    
    # 예측
    prediction = model.predict(review_tfidf)[0]
    probability = model.predict_proba(review_tfidf)[0]
    
    # 결과
    sentiment = "긍정 😊" if prediction == 1 else "부정 😞"
    confidence = probability[prediction] * 100
    
    return {
        'review': review,
        'label': int(prediction),
        'sentiment': sentiment,
        'confidence': confidence,
        'prob_negative': probability[0] * 100,
        'prob_positive': probability[1] * 100
    }

# ============================================================
# 4. 배치 예측 함수
# ============================================================
def predict_batch(reviews):
    """
    여러 리뷰를 한 번에 예측하는 함수
    
    Parameters:
    -----------
    reviews : list
        예측할 리뷰 텍스트 리스트
    
    Returns:
    --------
    list : 예측 결과 리스트
    """
    results = []
    for review in reviews:
        result = predict_sentiment(review)
        results.append(result)
    return results

# ============================================================
# 5. 테스트 예측
# ============================================================
print("\n[2단계] 테스트 예측")
print("="*70)

# 테스트 리뷰들
test_reviews = [
    "이 영화 정말 재미있어요! 강력 추천합니다",
    "완전 최고의 영화! 다시 보고 싶어요",
    "시간 낭비였어요. 별로 추천하지 않습니다",
    "너무 지루하고 재미없어요",
    "배우들 연기가 훌륭했고 스토리도 좋았어요",
    "돈 아까웠습니다. 보지 마세요",
    "그냥 그래요. 특별할 건 없었어요",
    "감동적이고 아름다운 영화였습니다",
    "최악의 영화. 시간만 버렸어요",
    "기대 이상이었어요! 꼭 보세요"
]

print("\n🎬 테스트 리뷰 감성 분석 결과:\n")

for i, review in enumerate(test_reviews, 1):
    result = predict_sentiment(review)
    print(f"{i}. 리뷰: {result['review']}")
    print(f"   → 예측: {result['sentiment']} (확신도: {result['confidence']:.2f}%)")
    print(f"   → 부정 확률: {result['prob_negative']:.2f}% | 긍정 확률: {result['prob_positive']:.2f}%")
    print()

# ============================================================
# 6. 실제 테스트 데이터 샘플 예측
# ============================================================
print("\n[3단계] 실제 테스트 데이터 샘플 예측")
print("="*70)

try:
    test_df = pd.read_csv('ratings_test_clean.csv')
    
    # 랜덤 샘플 10개 선택
    sample_df = test_df.sample(n=10, random_state=42)
    
    print("\n📊 실제 테스트 데이터 샘플 10개 예측 결과:\n")
    
    correct = 0
    for idx, row in sample_df.iterrows():
        result = predict_sentiment(row['document_clean'])
        actual = "긍정 😊" if row['label'] == 1 else "부정 😞"
        is_correct = "✅" if result['label'] == row['label'] else "❌"
        
        if result['label'] == row['label']:
            correct += 1
        
        print(f"리뷰: {row['document_clean']}")
        print(f"실제: {actual} | 예측: {result['sentiment']} {is_correct}")
        print(f"확신도: {result['confidence']:.2f}%")
        print()
    
    accuracy = (correct / len(sample_df)) * 100
    print(f"샘플 정확도: {correct}/{len(sample_df)} ({accuracy:.1f}%)")
    
except FileNotFoundError:
    print("테스트 데이터를 찾을 수 없습니다.")

# ============================================================
# 7. 대화형 예측 시스템
# ============================================================
print("\n" + "="*70)
print("💬 대화형 감성 분석 시스템")
print("="*70)
print("리뷰를 입력하면 감성을 분석해드립니다.")
print("종료하려면 'quit' 또는 'exit'를 입력하세요.\n")

while True:
    user_input = input("리뷰 입력 >>> ").strip()
    
    if user_input.lower() in ['quit', 'exit', '종료', 'q']:
        print("\n👋 감성 분석 시스템을 종료합니다. 감사합니다!")
        break
    
    if not user_input:
        print("⚠️ 리뷰를 입력해주세요.\n")
        continue
    
    # 예측
    result = predict_sentiment(user_input)
    
    print(f"\n📊 분석 결과:")
    print(f"  감성: {result['sentiment']}")
    print(f"  확신도: {result['confidence']:.2f}%")
    print(f"  부정 확률: {result['prob_negative']:.2f}% | 긍정 확률: {result['prob_positive']:.2f}%")
    print()

