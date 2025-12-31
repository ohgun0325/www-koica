"""
타이타닉 데이터 서비스
판다스, 넘파이, 사이킷런을 사용한 데이터 처리 및 머신러닝 서비스
"""
import sys
import os
import logging
from pathlib import Path
from typing import List, Dict, Optional, Any, ParamSpecArgs
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from icecream import ic
from tabulate import tabulate

# Windows 터미널 인코딩 설정
if sys.platform == 'win32':
    os.system('chcp 65001 >nul 2>&1')  # UTF-8 인코딩 설정
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# print() 함수를 래핑하여 항상 flush되도록 함 (Docker 로그 즉시 표시)
_original_print = print
def print(*args, **kwargs):
    """print() 함수 래퍼: 항상 flush하여 Docker 로그에 즉시 표시"""
    kwargs.setdefault('flush', True)  # flush=True 기본값 설정
    _original_print(*args, **kwargs)

# ic() 함수도 래핑하여 출력이 즉시 표시되도록 함
_original_ic = ic
def ic(*args, **kwargs):
    """ic() 함수 래퍼: 출력 후 flush하여 Docker 로그에 즉시 표시"""
    result = _original_ic(*args, **kwargs)
    # ic() 출력 후 강제 flush
    sys.stdout.flush()
    sys.stderr.flush()
    return result

# 공통 모듈 경로 추가
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

# TitanicMethod import
from .titanic_method import TitanicMethod


class TitanicService:
    """
    타이타닉 승객 데이터 CRUD 서비스 클래스
    Java 스타일의 서비스 레이어 패턴 구현
    """
    def __init__(self):
        pass
    
    def _print_dataframe_info(self, name: str, df: pd.DataFrame, stage: str = ""):
        """
        DataFrame 정보를 터미널에 표 형식으로 출력
        """
        print(f"\n{'='*80}")
        if stage:
            print(f"📊 [{stage}] {name} 데이터 상태")
        else:
            print(f"📊 {name} 데이터 상태")
        print(f"{'='*80}")
        
        # 1. 데이터 타입 출력
        print(f"\n[1] 데이터 타입 (dtypes)")
        print("-" * 80)
        dtype_df = pd.DataFrame({
            'Column': df.dtypes.index,
            'Type': df.dtypes.values.astype(str)
        })
        print(tabulate(dtype_df, headers='keys', tablefmt='grid', showindex=False))
        
        # 2. 컬럼 목록 출력
        print(f"\n[2] 컬럼 목록 (columns)")
        print("-" * 80)
        print(f"총 {len(df.columns)}개 컬럼: {', '.join(df.columns.tolist())}")
        
        # 3. 상위 5개 행 출력
        print(f"\n[3] 상위 5개 행")
        print("-" * 80)
        print(tabulate(df.head(5), headers='keys', tablefmt='grid', showindex=True))
        
        # 4. Null 값 개수 출력
        print(f"\n[4] Null 값 개수")
        print("-" * 80)
        null_series = df.isnull().sum()
        null_df = pd.DataFrame({
            'Column': null_series.index,
            'Null Count': null_series.values
        })
        null_df = null_df[null_df['Null Count'] > 0]  # Null이 있는 컬럼만 표시
        if len(null_df) > 0:
            print(tabulate(null_df, headers='keys', tablefmt='grid', showindex=False))
        else:
            print("✅ Null 값이 없습니다!")
        
        # 5. 데이터 크기 정보
        print(f"\n[5] 데이터 크기")
        print("-" * 80)
        print(f"행(Rows): {len(df):,}개")
        print(f"열(Columns): {len(df.columns)}개")
        print(f"메모리 사용량: {df.memory_usage(deep=True).sum() / 1024:.2f} KB")
        print()

    def preprogress(self):
        print("\n" + "="*80)
        print("🚀 타이타닉 데이터 전처리 시작")
        print("="*80)
        ic("😊😊 전처리 시작")
        
        the_method = TitanicMethod()
        df_train = the_method.new_model('train.csv')
        df_test = the_method.new_model('test.csv')
        this_train = the_method.create_df(df_train, 'Survived')
        
        # test.csv에는 Survived 컬럼이 없을 수 있으므로 체크
        if 'Survived' in df_test.columns:
            this_test = the_method.create_df(df_test, 'Survived')
        else:
            this_test = df_test  # Survived 컬럼이 없으면 그대로 사용
            print("ℹ️  Test 데이터에는 Survived 컬럼이 없습니다 (예측용 데이터)")
            ic("Test 데이터에는 Survived 컬럼이 없습니다 (예측용 데이터)")
        
        # 전처리 전 상태 출력
        print("\n" + "="*80)
        print("📋 [전처리 전] 데이터 상태")
        print("="*80)
        for name, data in [('Train', this_train), ('Test', this_test)]:
            # 터미널 출력 (표 형식)
            self._print_dataframe_info(name, data, "전처리 전")
            # API/로그 출력 (icecream) - 터미널에도 출력되도록 print()도 함께 사용
            print(f'[IC] 1. {name} 의 type\n {data.dtypes} ')
            ic(f'1. {name} 의 type\n {data.dtypes} ')
            print(f'[IC] 2. {name} 의 columns\n {data.columns} ')
            ic(f'2. {name} 의 columns\n {data.columns} ')
            print(f'[IC] 3. {name} 의 상위 5개 행\n {data.head(5).to_dict(orient="records")} ')
            ic(f'3. {name} 의 상위 5개 행\n {data.head(5).to_dict(orient="records")} ')
            print(f'[IC] 4. {name} 의 null 의 갯수\n {data.isnull().sum().to_dict()}개')
            ic(f'4. {name} 의 null 의 갯수\n {data.isnull().sum().to_dict()}개')

        # Train, Test 데이터 전처리
        print("\n" + "="*80)
        print("⚙️  전처리 진행 중...")
        print("="*80)
        print("  - 피처 삭제: SibSp, Parch, Cabin, Ticket")
        drop_features = ['SibSp', 'Parch', 'Cabin', 'Ticket']
        this_train, this_test = the_method.drop_feature(this_train, this_test, *drop_features)
        
        print("  - Pclass Ordinal 처리")
        this_train, this_test = the_method.pclass_ordinal(this_train, this_test)
        
        print("  - Title Nominal 처리")
        this_train, this_test = the_method.title_nominal(this_train, this_test)
        
        print("  - Gender Nominal 처리")
        this_train, this_test = the_method.gender_nominal(this_train, this_test)
        
        print("  - Age Ratio 처리")
        this_train, this_test = the_method.age_ratio(this_train, this_test)
        
        print("  - Fare Ratio 처리")
        this_train, this_test = the_method.fare_ratio(this_train, this_test)
        
        print("  - Embarked Nominal 처리")
        this_train, this_test = the_method.embarked_nominal(this_train, this_test)
        
        print("  - Name 컬럼 삭제")
        drop_features = ['Name']
        this_train, this_test = the_method.drop_feature(this_train, this_test, *drop_features)
        
        # 전처리 후 상태 출력
        print("\n" + "="*80)
        print("✅ [전처리 완료] 데이터 상태")
        print("="*80)
        ic("😊😊 전처리 완료")
        for name, data in [('Train', this_train), ('Test', this_test)]:
            # 터미널 출력 (표 형식)
            self._print_dataframe_info(name, data, "전처리 후")
            # API/로그 출력 (icecream) - 터미널에도 출력되도록 print()도 함께 사용
            print(f'[IC] 1. {name} 의 type\n {data.dtypes} ')
            ic(f'1. {name} 의 type\n {data.dtypes} ')
            print(f'[IC] 2. {name} 의 columns\n {data.columns} ')
            ic(f'2. {name} 의 columns\n {data.columns} ')
            print(f'[IC] 3. {name} 의 상위 5개 행\n {data.head(5).to_dict(orient="records")} ')
            ic(f'3. {name} 의 상위 5개 행\n {data.head(5).to_dict(orient="records")} ')
            print(f'[IC] 4. {name} 의 null 의 갯수\n {data.isnull().sum().to_dict()}개')
            ic(f'4. {name} 의 null 의 갯수\n {data.isnull().sum().to_dict()}개')
        
        print("\n" + "="*80)
        print("🎉 전처리 완료!")
        print("="*80 + "\n")
    
    def modeling(self):
        ic("😊😊 모델링 시작")

        #로지스틱 회귀
        #NB
        #램덤 포레스트
        #LGBM
        #SVM

        ic("😊😊 모델링 완료")

    def learning(self):
        logger.info("😊😊 학습 시작")
        
        #로지스틱 회귀
        #NB
        #램덤 포레스트
        #LGBM
        #SVM

        logger.info("😊😊 학습 완료")

    def evaluating(self):
        ic("😊😊 평가 시작")

        the_method = TitanicMethod()

        # 1) 데이터 로드
        df_train = the_method.new_model('train.csv')

        # 2) 레이블 분리
        y_df = the_method.create_label(df_train, 'Survived')
        X_df = the_method.create_df(df_train, 'Survived')

        # 3) 동일 파이프라인 전처리 (train_df, test_df 형태로 처리)
        dummy = X_df.copy()

        drop_features = ['SibSp', 'Parch', 'Cabin', 'Ticket']
        X_df, dummy = the_method.drop_feature(X_df, dummy, *drop_features)
        X_df, dummy = the_method.pclass_ordinal(X_df, dummy)
        X_df, dummy = the_method.title_nominal(X_df, dummy)
        X_df, dummy = the_method.gender_nominal(X_df, dummy)
        X_df, dummy = the_method.age_ratio(X_df, dummy)
        X_df, dummy = the_method.fare_ratio(X_df, dummy)
        X_df, dummy = the_method.embarked_nominal(X_df, dummy)

        if 'Name' in X_df.columns:
            X_df, dummy = the_method.drop_feature(X_df, dummy, 'Name')

        # 4) 학습/검증 분리
        y = y_df.squeeze()
        X_train, X_val, y_train, y_val = train_test_split(
            X_df, y, test_size=0.2, random_state=42, stratify=y
        )

        # 5) 여러 모델 검증
        models = [
            ("DecisionTree", DecisionTreeClassifier(random_state=42)),
            ("RandomForest", RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1)),
            ("GaussianNB", GaussianNB()),
            ("SVM_rbf", SVC(kernel='rbf', probability=True, random_state=42)),
            ("LogisticRegression", LogisticRegression(max_iter=1000, n_jobs=-1))
        ]

        for name, model in models:
            model.fit(X_train, y_train)
            y_pred = model.predict(X_val)
            acc = accuracy_score(y_val, y_pred)
            msg = f"{name} 검증 정확도: {acc*100:.2f}%"
            logger.info(msg)
            ic(msg)

        logger.info("😊😊 평가 완료")
        ic("😊😊 평가 완료")

    def submit(self):
        """
        RandomForest 모델로 test.csv 예측 후 Kaggle 제출용 CSV 생성
        출력: submission.csv (PassengerId, Survived)
        """
        ic("😊😊 제출 시작")
        logger.info("😊😊 제출 시작")

        the_method = TitanicMethod()

        # 1) train.csv 로드 및 전처리 (전체 데이터로 학습)
        df_train = the_method.new_model('train.csv')
        y_train_full = the_method.create_label(df_train, 'Survived').squeeze()
        X_train_full = the_method.create_df(df_train, 'Survived')

        # 2) test.csv 로드 (PassengerId 저장)
        df_test = the_method.new_model('test.csv')
        test_passenger_ids = df_test['PassengerId'].copy()
        X_test = df_test.copy()

        # 3) 동일 전처리 파이프라인 적용 (train, test 함께 처리)
        drop_features = ['SibSp', 'Parch', 'Cabin', 'Ticket']
        X_train_full, X_test = the_method.drop_feature(X_train_full, X_test, *drop_features)
        X_train_full, X_test = the_method.pclass_ordinal(X_train_full, X_test)
        X_train_full, X_test = the_method.title_nominal(X_train_full, X_test)
        X_train_full, X_test = the_method.gender_nominal(X_train_full, X_test)
        X_train_full, X_test = the_method.age_ratio(X_train_full, X_test)
        X_train_full, X_test = the_method.fare_ratio(X_train_full, X_test)
        X_train_full, X_test = the_method.embarked_nominal(X_train_full, X_test)

        if 'Name' in X_train_full.columns:
            X_train_full, X_test = the_method.drop_feature(X_train_full, X_test, 'Name')

        # 4) PassengerId 제거 (모델 학습용 피처에서 제외)
        if 'PassengerId' in X_train_full.columns:
            X_train_full = X_train_full.drop(columns=['PassengerId'])
        if 'PassengerId' in X_test.columns:
            X_test = X_test.drop(columns=['PassengerId'])

        # 5) RandomForest 모델 학습 (전체 train 데이터 사용)
        model = RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1)
        model.fit(X_train_full, y_train_full)
        logger.info("RandomForest 모델 학습 완료")
        ic("RandomForest 모델 학습 완료")

        # 6) test 데이터 예측
        y_pred = model.predict(X_test)
        logger.info(f"예측 완료: {len(y_pred)}개 샘플")
        ic(f"예측 완료: {len(y_pred)}개 샘플")

        # 7) Kaggle 제출용 CSV 생성
        submission = pd.DataFrame({
            'PassengerId': test_passenger_ids,
            'Survived': y_pred
        })

        # 8) CSV 파일 저장
        output_path = Path(__file__).parent / 'submission.csv'
        submission.to_csv(output_path, index=False)
        logger.info(f"제출 파일 생성 완료: {output_path}")
        ic(f"제출 파일 생성 완료: {output_path}")

        # 9) 결과 미리보기
        logger.info(f"\n제출 파일 미리보기 (상위 10개):\n{submission.head(10).to_string(index=False)}")
        ic(submission.head(10))

        logger.info("😊😊 제출 완료")
        ic("😊😊 제출 완료")
        
        return {
            "status": "success",
            "output_file": str(output_path),
            "total_predictions": len(y_pred),
            "preview": submission.head(10).to_dict(orient='records')
        }