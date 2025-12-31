"""
Dataset Management Class
데이터셋 관리 클래스
"""

from dataclasses import dataclass, field
from typing import Optional
import pandas as pd
import os
from pathlib import Path


@dataclass
class DataSets:
    """
    데이터셋 관리 클래스
    
    파일 경로, 데이터프레임, ID 및 레이블 컬럼을 관리합니다.
    """
    _fname: str = ''  # file name
    _dname: str = field(default_factory=lambda: str(Path(__file__).parent / "data"))  # data path
    _sname: str = field(default_factory=lambda: str(Path(__file__).parent / "save"))  # save path
    _cctv: Optional[pd.DataFrame] = None
    _crime: Optional[pd.DataFrame] = None
    _population: Optional[pd.DataFrame] = None
    
    #비지도이면 ID, Label 없음
    
    @property
    def fname(self) -> str:
        """파일명 반환"""
        return self._fname
    
    @fname.setter
    def fname(self, fname: str) -> None:
        """파일명 설정"""
        self._fname = fname
    
    @property
    def dname(self) -> str:
        """데이터 경로 반환"""
        return self._dname
    
    @dname.setter
    def dname(self, dname: str) -> None:
        """데이터 경로 설정"""
        self._dname = dname
    
    @property
    def sname(self) -> str:
        """저장 경로 반환"""
        return self._sname
    
    @sname.setter
    def sname(self, sname: str) -> None:
        """저장 경로 설정"""
        self._sname = sname
    
    @property
    def cctv(self) -> Optional[pd.DataFrame]:
        """CCTV 데이터프레임 반환"""
        return self._cctv
    
    @cctv.setter
    def cctv(self, cctv: Optional[pd.DataFrame]) -> None:
        """CCTV 데이터프레임 설정"""
        self._cctv = cctv
    
    @property
    def crime(self) -> Optional[pd.DataFrame]:
        """범죄 데이터프레임 반환"""
        return self._crime
    
    @crime.setter
    def crime(self, crime: Optional[pd.DataFrame]) -> None:
        """범죄 데이터프레임 설정"""
        self._crime = crime
    
    @property
    def population(self) -> Optional[pd.DataFrame]:
        """인구 데이터프레임 반환"""
        return self._population
    
    @population.setter
    def population(self, population: Optional[pd.DataFrame]) -> None:
        """인구 데이터프레임 설정"""
        self._population = population
    
    @property
    def id(self) -> str:
        """ID 컬럼명 반환"""
        return self._id
    
    @id.setter
    def id(self, id: str) -> None:
        """ID 컬럼명 설정"""
        self._id = id
    
    @property
    def label(self) -> str:
        """레이블 컬럼명 반환"""
        return self._label
    
    @label.setter
    def label(self, label: str) -> None:
        """레이블 컬럼명 설정"""
        self._label = label
    
    def load_cctv(self, file_path: Optional[str] = None) -> pd.DataFrame:
        """
        CCTV 데이터 로드
        
        Args:
            file_path: 파일 경로 (기본값: data/cctv.xlsx)
            
        Returns:
            CCTV 데이터프레임
        """
        if file_path is None:
            # 기본 경로: data/cctv.xlsx
            current_dir = Path(__file__).parent
            file_path = str(current_dir / "data" / "cctv.xlsx")
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"파일을 찾을 수 없습니다: {file_path}")
        
        self._cctv = pd.read_excel(file_path)
        self._fname = os.path.basename(file_path)
        self._dname = os.path.dirname(file_path)
        
        return self._cctv
    
    def load_crime(self, file_path: Optional[str] = None) -> pd.DataFrame:
        """
        범죄 데이터 로드
        
        Args:
            file_path: 파일 경로 (기본값: data/crime.csv)
            
        Returns:
            범죄 데이터프레임
        """
        if file_path is None:
            # 기본 경로: data/crime.csv
            current_dir = Path(__file__).parent
            file_path = str(current_dir / "data" / "crime.csv")
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"파일을 찾을 수 없습니다: {file_path}")
        
        self._crime = pd.read_csv(file_path)
        
        return self._crime
    
    def save_cctv(self, file_path: Optional[str] = None) -> None:
        """
        CCTV 데이터 저장
        
        Args:
            file_path: 저장할 파일 경로
        """
        if self._cctv is None:
            raise ValueError("저장할 CCTV 데이터가 없습니다.")
        
        if file_path is None:
            if self._sname:
                file_path = os.path.join(self._sname, "cctv.xlsx")
            else:
                raise ValueError("저장 경로를 지정해주세요.")
        
        self._cctv.to_excel(file_path, index=False)
        print(f"CCTV 데이터가 저장되었습니다: {file_path}")
    
    def save_crime(self, file_path: Optional[str] = None) -> None:
        """
        범죄 데이터 저장
        
        Args:
            file_path: 저장할 파일 경로
        """
        if self._crime is None:
            raise ValueError("저장할 범죄 데이터가 없습니다.")
        
        if file_path is None:
            if self._sname:
                file_path = os.path.join(self._sname, "crime.csv")
            else:
                raise ValueError("저장 경로를 지정해주세요.")
        
        self._crime.to_csv(file_path, index=False)
        print(f"범죄 데이터가 저장되었습니다: {file_path}")
    
    def get_info(self) -> dict:
        """
        데이터셋 정보 반환
        
        Returns:
            데이터셋 정보 딕셔너리
        """
        info = {
            "file_name": self._fname,
            "data_path": self._dname,
            "save_path": self._sname,
            "id_column": self._id,
            "label_column": self._label,
            "cctv_shape": self._cctv.shape if self._cctv is not None else None,
            "crime_shape": self._crime.shape if self._crime is not None else None,
            "population_shape": self._population.shape if self._population is not None else None,
        }
        return info
    
    def __str__(self) -> str:
        """문자열 표현"""
        cctv_info = f"CCTV: {self._cctv.shape}" if self._cctv is not None else "CCTV: None"
        crime_info = f"Crime: {self._crime.shape}" if self._crime is not None else "Crime: None"
        population_info = f"Population: {self._population.shape}" if self._population is not None else "Population: None"
        return f"DataSets(fname={self._fname}, {cctv_info}, {crime_info}, {population_info})"
    
    def __repr__(self) -> str:
        """객체 표현"""
        return self.__str__()

