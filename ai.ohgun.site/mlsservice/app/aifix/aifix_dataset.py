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
    _dname: str = ''  # data path
    _sname: str = ''  # save path
    _train: Optional[pd.DataFrame] = None
    _test: Optional[pd.DataFrame] = None
    _id: str = ''
    _label: str = ''
    
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
    def train(self) -> Optional[pd.DataFrame]:
        """훈련 데이터프레임 반환"""
        return self._train
    
    @train.setter
    def train(self, train: Optional[pd.DataFrame]) -> None:
        """훈련 데이터프레임 설정"""
        self._train = train
    
    @property
    def test(self) -> Optional[pd.DataFrame]:
        """테스트 데이터프레임 반환"""
        return self._test
    
    @test.setter
    def test(self, test: Optional[pd.DataFrame]) -> None:
        """테스트 데이터프레임 설정"""
        self._test = test
    
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
    
    def load_train(self, file_path: Optional[str] = None) -> pd.DataFrame:
        """
        훈련 데이터 로드
        
        Args:
            file_path: 파일 경로 (기본값: aifix/grade.csv)
            
        Returns:
            훈련 데이터프레임
        """
        if file_path is None:
            # 기본 경로: aifix/grade.csv
            current_dir = Path(__file__).parent
            file_path = str(current_dir / "grade.csv")
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"파일을 찾을 수 없습니다: {file_path}")
        
        self._train = pd.read_csv(file_path, encoding='utf-8')
        self._fname = os.path.basename(file_path)
        self._dname = os.path.dirname(file_path)
        
        return self._train
    
    def load_test(self, file_path: Optional[str] = None) -> pd.DataFrame:
        """
        테스트 데이터 로드
        
        Args:
            file_path: 파일 경로 (기본값: aifix/grade.csv)
            
        Returns:
            테스트 데이터프레임
        """
        if file_path is None:
            # 기본 경로: aifix/grade.csv
            current_dir = Path(__file__).parent
            file_path = str(current_dir / "grade.csv")
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"파일을 찾을 수 없습니다: {file_path}")
        
        self._test = pd.read_csv(file_path, encoding='utf-8')
        
        return self._test
    
    def save_train(self, file_path: Optional[str] = None) -> None:
        """
        훈련 데이터 저장
        
        Args:
            file_path: 저장할 파일 경로
        """
        if self._train is None:
            raise ValueError("저장할 훈련 데이터가 없습니다.")
        
        if file_path is None:
            if self._sname:
                file_path = os.path.join(self._sname, "grade.csv")
            else:
                raise ValueError("저장 경로를 지정해주세요.")
        
        self._train.to_csv(file_path, index=False, encoding='utf-8')
        print(f"훈련 데이터가 저장되었습니다: {file_path}")
    
    def save_test(self, file_path: Optional[str] = None) -> None:
        """
        테스트 데이터 저장
        
        Args:
            file_path: 저장할 파일 경로
        """
        if self._test is None:
            raise ValueError("저장할 테스트 데이터가 없습니다.")
        
        if file_path is None:
            if self._sname:
                file_path = os.path.join(self._sname, "grade.csv")
            else:
                raise ValueError("저장 경로를 지정해주세요.")
        
        self._test.to_csv(file_path, index=False, encoding='utf-8')
        print(f"테스트 데이터가 저장되었습니다: {file_path}")
    
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
            "train_shape": self._train.shape if self._train is not None else None,
            "test_shape": self._test.shape if self._test is not None else None,
        }
        return info
    
    def __str__(self) -> str:
        """문자열 표현"""
        train_info = f"Train: {self._train.shape}" if self._train is not None else "Train: None"
        test_info = f"Test: {self._test.shape}" if self._test is not None else "Test: None"
        return f"DataSets(fname={self._fname}, {train_info}, {test_info}, id={self._id}, label={self._label})"
    
    def __repr__(self) -> str:
        """객체 표현"""
        return self.__str__()

