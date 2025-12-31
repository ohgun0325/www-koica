import pandas as pd
import numpy as np
import re
from pathlib import Path
from .seoul_dataset import DataSets

class SeoulMethod(object): 

    def __init__(self):
        #데이터셋 객체 생성
        self.dataset = DataSets()

    def csv_to_df(self, file_name: str) -> pd.DataFrame:
            return pd.read_csv(file_name)
    
    def excel_to_df(self, file_name: str) -> pd.DataFrame:
            return pd.read_excel(file_name)
    
    def load_cctv(self) -> pd.DataFrame:
        """
        CCTV 데이터 로드 (CSV)
        
        Returns:
            CCTV 데이터프레임
        """
        cctv_path = Path(self.dataset.dname) / "cctv.csv"
        if not cctv_path.exists():
            raise FileNotFoundError(f"CCTV 파일을 찾을 수 없습니다: {cctv_path}")
        
        df = pd.read_csv(cctv_path)
        self.dataset.cctv = df
        return df

    
    def load_crime(self) -> pd.DataFrame:
        """
        범죄 데이터 로드
        
        Returns:
            범죄 데이터프레임
        """
        crime_path = Path(self.dataset.dname) / "crime.csv"
        if not crime_path.exists():
            raise FileNotFoundError(f"범죄 파일을 찾을 수 없습니다: {crime_path}")
        
        df = pd.read_csv(crime_path)
        self.dataset.crime = df
        return df
    
    def load_population(self) -> pd.DataFrame:
        """
        인구 데이터 로드 (XLS)
        
        Returns:
            인구 데이터프레임
        """
        pop_path = Path(self.dataset.dname) / "pop.xls"
        if not pop_path.exists():
            raise FileNotFoundError(f"인구 파일을 찾을 수 없습니다: {pop_path}")
        
        # XLS 파일 읽기 (header=2로 헤더 위치 지정)
        df = pd.read_excel(pop_path, header=2)
        
        # axis = 0 방향으로 위로부터 2, 3, 4 번째 행을 제거 (인덱스 1, 2, 3)
        # 합계 행(인덱스 0)은 유지하고, 그 다음 3개 행 제거
        df = df.drop(df.index[1:4])  # 인덱스 1, 2, 3 제거
        df = df.reset_index(drop=True)  # 인덱스 재설정
        
        # axis = 1 방향으로 자치구와 좌표(경도, 위도)부터 5번째 컬럼만 남기고 모두 삭제 (여자 컬럼까지 포함)
        # 자치구 컬럼 찾기
        if '자치구' in df.columns:
            district_idx = df.columns.get_loc('자치구')
            # 자치구부터 5개 컬럼만 선택 (자치구, 세대, 계, 남자, 여자)
            cols_to_keep = df.columns[district_idx:district_idx+5].tolist()
            df = df[cols_to_keep]
        
        self.dataset.population = df
        return df
    
    def df_merge(self, df1: pd.DataFrame, df2: pd.DataFrame, feature: str) -> pd.DataFrame:
        """
        두 데이터프레임을 지정된 feature로 머지
        
        Args:
            df1: 첫 번째 데이터프레임
            df2: 두 번째 데이터프레임
            feature: 머지할 키 컬럼명
            
        Returns:
            머지된 데이터프레임
        """
        return pd.merge(df1, df2, on=feature, how='inner')
    
    def merge_cctv_pop(self) -> pd.DataFrame:
        """
        CCTV와 인구 데이터를 머지 (추천 전략 적용)
        - Key: CCTV는 '기관명', POP는 '자치구'를 '구'로 통일
        - 중복 컬럼 방지: 접두사 사용 (CCTV_, 인구_)
        - Inner Join: 양쪽 모두 있는 구만 포함
        
        Returns:
            머지된 데이터프레임
        """
        # 1. 데이터 로드
        df_cctv = self.load_cctv()
        df_pop = self.load_population()
        
        # 2. Key 컬럼 정규화
        # CCTV: '기관명' -> '구'
        if '기관명' in df_cctv.columns:
            df_cctv = df_cctv.rename(columns={'기관명': '구'})
        
        # POP: '자치구' -> '구'
        if '자치구' in df_pop.columns:
            df_pop = df_pop.rename(columns={'자치구': '구'})
        
        # 3. 공백 제거 및 문자열 정규화
        df_cctv['구'] = df_cctv['구'].astype(str).str.strip()
        df_pop['구'] = df_pop['구'].astype(str).str.strip()
        
        # 4. 중복 방지를 위한 컬럼명 변경 (접두사 추가)
        # CCTV 컬럼명에 접두사 추가 (구 제외)
        cctv_cols = {col: f'CCTV_{col}' for col in df_cctv.columns if col != '구'}
        df_cctv = df_cctv.rename(columns=cctv_cols)
        
        # POP 컬럼명에 접두사 추가 (구 제외)
        pop_cols = {col: f'인구_{col}' for col in df_pop.columns if col != '구'}
        df_pop = df_pop.rename(columns=pop_cols)
        
        # 5. 머지 (Inner Join: 양쪽 모두 있는 구만 포함)
        df_merged = pd.merge(
            df_cctv,
            df_pop,
            on='구',
            how='inner'
        )
        
        return df_merged
    
    def merge_crime_cctv(self) -> pd.DataFrame:
        """
        범죄 데이터와 CCTV 데이터를 머지
        - 관서명(경찰서) → 기관명(행정구역) 매핑 테이블 사용
        - 관서명과 기관명을 나란히 배치
        - CCTV 데이터는 기관명으로 조인
        
        Returns:
            머지된 데이터프레임 (관서명, 기관명, CCTV_소계, 범죄 데이터...)
        """
        # 1. 관서명(경찰서) → 기관명(행정구역) 매핑 테이블
        DISTRICT_MAPPING = {
            # 직접 매칭 (경찰서명 → 행정구역명)
            '강남서': '강남구',
            '강동서': '강동구',
            '강북서': '강북구',
            '강서서': '강서구',
            '관악서': '관악구',
            '광진서': '광진구',
            '구로서': '구로구',
            '금천서': '금천구',
            '노원서': '노원구',
            '도봉서': '도봉구',
            '동대문서': '동대문구',
            '동작서': '동작구',
            '마포서': '마포구',
            '서대문서': '서대문구',
            '서초서': '서초구',
            '성동서': '성동구',
            '성북서': '성북구',
            '송파서': '송파구',
            '양천서': '양천구',
            '영등포서': '영등포구',
            '용산서': '용산구',
            '은평서': '은평구',
            '종로서': '종로구',
            '중랑서': '중랑구',
            
            # 예외 케이스 매핑
            '중부서': '중구',      # 중구 관할
            '남대문서': '중구',    # 중구 관할
            '혜화서': '종로구',    # 종로구 일부
            '서부서': '은평구',    # 은평구 일부
            '종암서': '성북구',    # 성북구 일부
            '방배서': '서초구',    # 서초구 일부
            '수서서': '강남구',    # 강남구 일부
        }
        
        # 2. 데이터 로드
        df_crime = self.load_crime()
        df_cctv = self.load_cctv()
        
        # 3. Crime 데이터에 기관명 컬럼 추가
        df_crime = df_crime.copy()
        df_crime['기관명'] = df_crime['관서명'].map(DISTRICT_MAPPING)
        
        # 4. CCTV 데이터 컬럼명에 접두사 추가 (기관명 제외)
        df_cctv = df_cctv.copy()
        cctv_cols = {col: f'CCTV_{col}' for col in df_cctv.columns if col != '기관명'}
        df_cctv = df_cctv.rename(columns=cctv_cols)
        
        # 5. Merge 수행 (Left Join: Crime 기준으로 모든 관서 유지)
        df_merged = pd.merge(
            df_crime,
            df_cctv,
            on='기관명',
            how='left',
            suffixes=('', '_CCTV')
        )
        
        # 6. 컬럼 순서 재배치: 관서명, 기관명, CCTV_소계, 범죄 데이터...
        # 먼저 주요 컬럼들 추출
        main_cols = ['관서명', '기관명']
        cctv_cols = [col for col in df_merged.columns if col.startswith('CCTV_')]
        crime_cols = [col for col in df_merged.columns if col not in main_cols + cctv_cols]
        
        # 최종 컬럼 순서: 관서명, 기관명, CCTV 컬럼들, 범죄 컬럼들
        final_cols = main_cols + cctv_cols + crime_cols
        df_merged = df_merged[final_cols]
        
        return df_merged
    

    