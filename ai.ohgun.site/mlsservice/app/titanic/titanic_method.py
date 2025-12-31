import pandas as pd
import numpy as np
import re
from pathlib import Path
from .titanic_dataset import DataSets


class TitanicMethod(object): 

    def __init__(self):
        #데이터셋 객체 생성
        self.dataset = DataSets()

    def new_model(self, file_name: str) -> pd.DataFrame:
        return pd.read_csv(Path(__file__).parent / file_name)

    def create_df(self, df: pd.DataFrame, label: str) -> pd.DataFrame:
        return df.drop(columns=[label])

    def create_label(self, df: pd.DataFrame, label: str) -> pd.DataFrame:
        return df[[label]] 

    def drop_feature(self, train_df, test_df, *features):
        [df.drop(list(features), axis=1, inplace=True) for df in (train_df, test_df)]
        return train_df, test_df

    def check_null(self, df: pd.DataFrame) -> int:
        return int(df.isnull().sum())

    # nominal, ordinal, interval, ratio

    def pclass_ordinal(self, train_df, test_df):
        """
        Pclass는 순서가 있는 Ordinal 데이터이므로 그대로 숫자 1,2,3을 유지
        필요시 (3,2,1)로 재정렬 가능하지만 기본적으로는 그대로 유지
        """
        # Pclass는 이미 1,2,3으로 되어 있으므로 그대로 유지
        # 필요시 역순으로 재정렬: df['Pclass'] = 4 - df['Pclass']
        return train_df, test_df

    def title_nominal(self, train_df, test_df):
        """
        Name 컬럼에서 Title 추출
        Name에서 Mr, Mrs, Miss, Master 등 호칭을 정규표현식으로 추출하여 Title 컬럼 생성
        """
        title_mapping = {
            'Mr': 'Mr', 'Miss': 'Miss', 'Mrs': 'Mrs', 'Master': 'Master',
            'Don': 'Rare', 'Rev': 'Rare', 'Dr': 'Rare', 'Mme': 'Mrs',
            'Ms': 'Miss', 'Major': 'Rare', 'Lady': 'Rare', 'Sir': 'Rare',
            'Mlle': 'Miss', 'Col': 'Rare', 'Capt': 'Rare', 'Countess': 'Rare', 'Jonkheer': 'Rare'
        }
        # Title을 숫자로 매핑: Mr=0, Miss=1, Mrs=2, Master=3, Rare=4
        title_to_num = {'Mr': 0, 'Miss': 1, 'Mrs': 2, 'Master': 3, 'Rare': 4}
        
        for df in (train_df, test_df):
            title_text = df['Name'].str.extract(r',\s*([A-Za-z]+)\.', expand=False).map(title_mapping).fillna('Rare')
            df['Title'] = title_text.map(title_to_num)
        return train_df, test_df
    
    def gender_nominal(self, train_df, test_df):
        """
        Gender(Sex) Nominal 처리
        male, female → LabelEncoding 또는 one-hot encoding
        male=0, female=1로 인코딩
        """
        for df in (train_df, test_df):
            if 'Sex' in df.columns:
                df.rename(columns={'Sex': 'Gender'}, inplace=True)
            # Gender 컬럼을 0(male), 1(female)로 변환
            df['Gender'] = df['Gender'].map({'male': 0, 'female': 1})
            df['Gender_encoded'] = df['Gender']
            # 원본 값 기준으로 더미 변수 생성 (백업용)
            df['Gender_male'] = (df['Gender'] == 0).astype(int)
            df['Gender_female'] = (df['Gender'] == 1).astype(int)
        return train_df, test_df

    def age_ratio(self, train_df, test_df):
        """
        Age Ratio 처리
        Age 결측치는 중앙값으로 채우거나 Title 기반 예측치로 대체
        AgeGroup 생성
        """
        bins = [-1, 0, 5, 12, 18, 24, 35, 60, np.inf]
        labels = [0, 1, 2, 3, 4, 5, 6, 7]  # 숫자로 변경: Unknown=0, Baby=1, ..., Senior=7
        
        for df in (train_df, test_df):
            if 'Title' in df.columns:
                df['Age'].fillna(df['Title'].map(df.groupby('Title')['Age'].median()), inplace=True)
            if df['Age'].isnull().any():
                df['Age'].fillna(df['Age'].median(), inplace=True)
            # Age를 정수로 변환 (소수점 제거)
            df['Age'] = df['Age'].round().astype(int)
            df['AgeGroup'] = pd.cut(df['Age'], bins=bins, labels=labels, right=False).astype(int)
        return train_df, test_df
    
    def sibsp_ratio(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        SibSp Ratio 처리
        FamilySize = SibSp + Parch + 1 추가
        """
        df = df.copy()
        # FamilySize 추가
        if 'Parch' in df.columns:
            df['FamilySize'] = df['SibSp'] + df['Parch'] + 1
        else:
            df['FamilySize'] = df['SibSp'] + 1
        return df
    
    def parch_ratio(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Parch Ratio 처리
        FamilySize는 sibsp_ratio에서 이미 추가됨
        """
        df = df.copy()
        # FamilySize가 없으면 추가
        if 'FamilySize' not in df.columns:
            if 'SibSp' in df.columns:
                df['FamilySize'] = df['SibSp'] + df['Parch'] + 1
            else:
                df['FamilySize'] = df['Parch'] + 1
        return df
    
    def ticket_nominal(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Ticket Nominal 처리
        Ticket 문자열에서 앞부분의 문자구간만 추출
        예: "PC 17599" → "PC"
        """
        df = df.copy()
        # Ticket에서 앞부분 문자 추출
        df['TicketPrefix'] = df['Ticket'].str.extract(r'^([A-Za-z]+)', expand=False)
        df['TicketPrefix'] = df['TicketPrefix'].fillna('NUMERIC')
        
        # 너무 많은 unique value를 줄이기 위해 그룹화
        # 빈도가 낮은 prefix는 'OTHER'로 통합
        ticket_counts = df['TicketPrefix'].value_counts()
        rare_tickets = ticket_counts[ticket_counts < 10].index
        df['TicketPrefix'] = df['TicketPrefix'].replace(rare_tickets, 'OTHER')
        
        return df
    
    def fare_ratio(self, train_df, test_df):
        """
        Fare Ratio 처리
        결측치는 중앙값으로 채우기
        Fare의 분포가 치우쳤으므로 log1p 변환 권장
        """
        [df['Fare'].fillna(df['Fare'].median(), inplace=True) for df in (train_df, test_df)]
        [df.__setitem__('Fare_log', np.log1p(df['Fare'])) for df in (train_df, test_df)]
        return train_df, test_df
    
    def cabin_nominal(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Cabin Nominal 처리
        Cabin의 첫 문자만 추출하여 Deck을 생성
        예: "C85" → "C"
        결측치는 "Unknown"으로 처리
        """
        df = df.copy()
        # Cabin의 첫 문자만 추출
        df['Deck'] = df['Cabin'].str[0] if 'Cabin' in df.columns else None
        df['Deck'] = df['Deck'].fillna('Unknown')
        return df
    
    def embarked_nominal(self, train_df, test_df):
        """
        Embarked Nominal 처리
        S, C, Q → 숫자로 인코딩 (C=0, Q=1, S=2)
        """
        embarked_to_num = {'C': 0, 'Q': 1, 'S': 2}
        
        for df in (train_df, test_df):
            if df['Embarked'].isnull().any():
                df['Embarked'].fillna(df['Embarked'].mode()[0], inplace=True)
            # Embarked를 숫자로 변환
            df['Embarked'] = df['Embarked'].map(embarked_to_num)
            # 더미 변수도 생성
            df['Embarked_C'] = (df['Embarked'] == 0).astype(int)
            df['Embarked_Q'] = (df['Embarked'] == 1).astype(int)
            df['Embarked_S'] = (df['Embarked'] == 2).astype(int)
        return train_df, test_df
    
    def apply_all_preprocessing(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        전체 전처리 파이프라인 실행
        요청된 순서대로 모든 전처리 단계를 수행
        """
        df = df.copy()
        
        # 1. Pclass_ordinal 처리
        df = self.pclass_ordinal(df)
        
        # 2. Name 컬럼에서 Title 추출
        df = self.title_nominal(df)
        
        # 3. Name 컬럼 삭제
        if 'Name' in df.columns:
            df = df.drop(columns=["Name"])
        
        # 4. Gender(Sex) Nominal 처리
        df = self.gender_nominal(df)
        
        # 5. Age Ratio 처리
        df = self.age_ratio(df)
        
        # 6. SibSp, Parch Ratio 처리 (FamilySize 추가)
        df = self.sibsp_ratio(df)
        df = self.parch_ratio(df)
        
        # 7. Ticket Nominal 처리
        df = self.ticket_nominal(df)
        
        # 8. Fare Ratio 처리
        df = self.fare_ratio(df)
        
        # 9. Cabin Nominal 처리
        df = self.cabin_nominal(df)
        
        # 10. Embarked Nominal 처리
        df = self.embarked_nominal(df)
        
        # 11. 모든 Nominal 컬럼에 대해 One-Hot Encoding 수행
        nominal_columns = []
        if 'Title' in df.columns:
            nominal_columns.append('Title')
        if 'AgeGroup' in df.columns:
            nominal_columns.append('AgeGroup')
        if 'TicketPrefix' in df.columns:
            nominal_columns.append('TicketPrefix')
        if 'Deck' in df.columns:
            nominal_columns.append('Deck')
        
        for col in nominal_columns:
            if col in df.columns:
                dummies = pd.get_dummies(df[col], prefix=col)
                df = pd.concat([df, dummies], axis=1)
        
        return df
    