# -*- coding: utf-8 -*-
"""
네이버 영화 리뷰 감성 분류 - 1단계: EDA 및 데이터 전처리
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'  # Windows
plt.rcParams['axes.unicode_minus'] = False
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (12, 6)

print("="*70)
print("네이버 영화 리뷰 감성 분류 - EDA 및 데이터 전처리")
print("="*70)

# ============================================================
# 1. 데이터 로드
# ============================================================
print("\n[1단계] 데이터 로드 중...")

train_df = pd.read_csv('ratings_train.txt', sep='\t')
test_df = pd.read_csv('ratings_test.txt', sep='\t')

print(f"✅ 학습 데이터 크기: {train_df.shape}")
print(f"✅ 테스트 데이터 크기: {test_df.shape}")

# ============================================================
# 2. 기본 정보 확인
# ============================================================
print("\n[2단계] 데이터 기본 정보 확인")
print("\n학습 데이터 샘플:")
print(train_df.head())

print("\n데이터 타입:")
print(train_df.info())

# ============================================================
# 3. 결측치 확인 및 처리
# ============================================================
print("\n[3단계] 결측치 확인 및 처리")

print(f"\n학습 데이터 결측치: {train_df.isnull().sum().sum()}개")
print(train_df.isnull().sum())

print(f"\n테스트 데이터 결측치: {test_df.isnull().sum().sum()}개")
print(test_df.isnull().sum())

# 결측치 제거
train_clean = train_df.dropna(subset=['document']).reset_index(drop=True)
test_clean = test_df.dropna(subset=['document']).reset_index(drop=True)

print(f"\n✅ 결측치 제거 완료")
print(f"  학습: {len(train_df)} → {len(train_clean)} (제거: {len(train_df) - len(train_clean)}개)")
print(f"  테스트: {len(test_df)} → {len(test_clean)} (제거: {len(test_df) - len(test_clean)}개)")

# ============================================================
# 4. 중복 데이터 확인
# ============================================================
print("\n[4단계] 중복 데이터 확인")

train_duplicates = train_clean.duplicated(subset=['document']).sum()
test_duplicates = test_clean.duplicated(subset=['document']).sum()

print(f"학습 데이터 중복: {train_duplicates}개")
print(f"테스트 데이터 중복: {test_duplicates}개")

# ============================================================
# 5. 레이블 분포 확인
# ============================================================
print("\n[5단계] 레이블 분포 확인")

train_label_counts = train_clean['label'].value_counts()
test_label_counts = test_clean['label'].value_counts()

print("\n학습 데이터:")
print(f"  긍정(1): {train_label_counts.get(1, 0):,}개 ({train_label_counts.get(1, 0)/len(train_clean)*100:.2f}%)")
print(f"  부정(0): {train_label_counts.get(0, 0):,}개 ({train_label_counts.get(0, 0)/len(train_clean)*100:.2f}%)")

print("\n테스트 데이터:")
print(f"  긍정(1): {test_label_counts.get(1, 0):,}개 ({test_label_counts.get(1, 0)/len(test_clean)*100:.2f}%)")
print(f"  부정(0): {test_label_counts.get(0, 0):,}개 ({test_label_counts.get(0, 0)/len(test_clean)*100:.2f}%)")

# 레이블 분포 시각화
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].bar(train_label_counts.index, train_label_counts.values, color=['#ff6b6b', '#4ecdc4'])
axes[0].set_title('학습 데이터 레이블 분포', fontsize=14, fontweight='bold')
axes[0].set_xlabel('레이블 (0: 부정, 1: 긍정)')
axes[0].set_ylabel('개수')
axes[0].set_xticks([0, 1])
for i, v in enumerate(train_label_counts.values):
    axes[0].text(i, v + 1000, f'{v:,}\n({v/len(train_clean)*100:.1f}%)', 
                 ha='center', fontsize=11, fontweight='bold')

axes[1].bar(test_label_counts.index, test_label_counts.values, color=['#ff6b6b', '#4ecdc4'])
axes[1].set_title('테스트 데이터 레이블 분포', fontsize=14, fontweight='bold')
axes[1].set_xlabel('레이블 (0: 부정, 1: 긍정)')
axes[1].set_ylabel('개수')
axes[1].set_xticks([0, 1])
for i, v in enumerate(test_label_counts.values):
    axes[1].text(i, v + 500, f'{v:,}\n({v/len(test_clean)*100:.1f}%)', 
                 ha='center', fontsize=11, fontweight='bold')

plt.tight_layout()
plt.savefig('01_label_distribution.png', dpi=300, bbox_inches='tight')
print("\n✅ 레이블 분포 그래프 저장: 01_label_distribution.png")
plt.close()

# ============================================================
# 6. 리뷰 길이 분석
# ============================================================
print("\n[6단계] 리뷰 길이 분석")

train_clean['review_length'] = train_clean['document'].apply(len)
test_clean['review_length'] = test_clean['document'].apply(len)

print("\n리뷰 길이 통계 (학습 데이터):")
print(train_clean['review_length'].describe())

print(f"\n평균 리뷰 길이:")
print(f"  전체: {train_clean['review_length'].mean():.2f}자")
print(f"  긍정: {train_clean[train_clean['label']==1]['review_length'].mean():.2f}자")
print(f"  부정: {train_clean[train_clean['label']==0]['review_length'].mean():.2f}자")

# 리뷰 길이 시각화
fig, axes = plt.subplots(2, 2, figsize=(15, 10))

# 전체 분포
axes[0, 0].hist(train_clean['review_length'], bins=50, color='skyblue', edgecolor='black', alpha=0.7)
axes[0, 0].set_title('리뷰 길이 분포 (전체)', fontsize=12, fontweight='bold')
axes[0, 0].set_xlabel('리뷰 길이 (문자 수)')
axes[0, 0].set_ylabel('빈도')
axes[0, 0].axvline(train_clean['review_length'].mean(), color='red', 
                   linestyle='--', linewidth=2, label=f'평균: {train_clean["review_length"].mean():.1f}')
axes[0, 0].legend()

# 박스플롯
axes[0, 1].boxplot([train_clean[train_clean['label']==0]['review_length'],
                    train_clean[train_clean['label']==1]['review_length']],
                   labels=['부정(0)', '긍정(1)'])
axes[0, 1].set_title('감성별 리뷰 길이 비교', fontsize=12, fontweight='bold')
axes[0, 1].set_ylabel('리뷰 길이 (문자 수)')

# 긍정 리뷰
axes[1, 0].hist(train_clean[train_clean['label']==1]['review_length'], 
                bins=50, color='#4ecdc4', edgecolor='black', alpha=0.7)
axes[1, 0].set_title('긍정 리뷰 길이 분포', fontsize=12, fontweight='bold')
axes[1, 0].set_xlabel('리뷰 길이 (문자 수)')
axes[1, 0].set_ylabel('빈도')

# 부정 리뷰
axes[1, 1].hist(train_clean[train_clean['label']==0]['review_length'], 
                bins=50, color='#ff6b6b', edgecolor='black', alpha=0.7)
axes[1, 1].set_title('부정 리뷰 길이 분포', fontsize=12, fontweight='bold')
axes[1, 1].set_xlabel('리뷰 길이 (문자 수)')
axes[1, 1].set_ylabel('빈도')

plt.tight_layout()
plt.savefig('02_review_length_analysis.png', dpi=300, bbox_inches='tight')
print("\n✅ 리뷰 길이 분석 그래프 저장: 02_review_length_analysis.png")
plt.close()

# ============================================================
# 7. 샘플 리뷰 출력
# ============================================================
print("\n[7단계] 샘플 리뷰 확인")

print("\n😊 긍정 리뷰 샘플 5개:")
print("="*70)
for i, (idx, row) in enumerate(train_clean[train_clean['label']==1].head(5).iterrows(), 1):
    print(f"{i}. {row['document']}")

print("\n😞 부정 리뷰 샘플 5개:")
print("="*70)
for i, (idx, row) in enumerate(train_clean[train_clean['label']==0].head(5).iterrows(), 1):
    print(f"{i}. {row['document']}")

# ============================================================
# 8. 텍스트 전처리
# ============================================================
print("\n[8단계] 텍스트 전처리")

def clean_text(text):
    """텍스트 전처리 함수"""
    if not isinstance(text, str):
        return ""
    # 여러 공백을 하나로
    text = re.sub(r'\s+', ' ', text)
    # 앞뒤 공백 제거
    text = text.strip()
    return text

print("전처리 중...")
train_clean['document_clean'] = train_clean['document'].apply(clean_text)
test_clean['document_clean'] = test_clean['document'].apply(clean_text)

# 빈 문자열 확인 및 제거
empty_train = (train_clean['document_clean'] == '').sum()
empty_test = (test_clean['document_clean'] == '').sum()

print(f"빈 문자열 - 학습: {empty_train}개, 테스트: {empty_test}개")

if empty_train > 0:
    train_clean = train_clean[train_clean['document_clean'] != ''].reset_index(drop=True)
if empty_test > 0:
    test_clean = test_clean[test_clean['document_clean'] != ''].reset_index(drop=True)

print("✅ 전처리 완료")

# ============================================================
# 9. 전처리된 데이터 저장
# ============================================================
print("\n[9단계] 전처리된 데이터 저장")

train_clean.to_csv('ratings_train_clean.csv', index=False, encoding='utf-8-sig')
test_clean.to_csv('ratings_test_clean.csv', index=False, encoding='utf-8-sig')

print("✅ 데이터 저장 완료")
print(f"  - ratings_train_clean.csv ({len(train_clean):,} rows)")
print(f"  - ratings_test_clean.csv ({len(test_clean):,} rows)")

# ============================================================
# 10. 최종 요약
# ============================================================
print("\n" + "="*70)
print("📊 최종 데이터 요약")
print("="*70)

print(f"\n✅ 학습 데이터:")
print(f"  - 총 개수: {len(train_clean):,}개")
print(f"  - 긍정: {(train_clean['label']==1).sum():,}개 ({(train_clean['label']==1).sum()/len(train_clean)*100:.2f}%)")
print(f"  - 부정: {(train_clean['label']==0).sum():,}개 ({(train_clean['label']==0).sum()/len(train_clean)*100:.2f}%)")
print(f"  - 평균 리뷰 길이: {train_clean['review_length'].mean():.2f}자")

print(f"\n✅ 테스트 데이터:")
print(f"  - 총 개수: {len(test_clean):,}개")
print(f"  - 긍정: {(test_clean['label']==1).sum():,}개 ({(test_clean['label']==1).sum()/len(test_clean)*100:.2f}%)")
print(f"  - 부정: {(test_clean['label']==0).sum():,}개 ({(test_clean['label']==0).sum()/len(test_clean)*100:.2f}%)")
print(f"  - 평균 리뷰 길이: {test_clean['review_length'].mean():.2f}자")

print("\n" + "="*70)
print("🎉 EDA 및 전처리 완료!")
print("다음 단계: 02_train_model.py 실행")
print("="*70)

