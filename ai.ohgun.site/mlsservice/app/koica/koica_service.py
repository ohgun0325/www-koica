"""
KOICA 데이터 서비스
판다스, 넘파이, 사이킷런을 사용한 데이터 처리 및 머신러닝 서비스
"""
import sys
from pathlib import Path
from typing import List, Dict, Optional, Any, ParamSpecArgs
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from icecream import ic

# 공통 모듈 경로 추가
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))


class KoicaService:
    """
    KOICA 국제기구사업 데이터 CRUD 서비스 클래스
    Java 스타일의 서비스 레이어 패턴 구현
    """
    def __init__(self):
        pass

    def preprogress(self):
        ic("😊😊 전처리 시작")
        ic("😊😊 전처리 완료")

    def modeling(self):
        ic("😊😊 모델링 시작")
        ic("😊😊 모델링 완료")

    def learning(self):
        ic("😊😊 학습 시작")
        ic("😊😊 학습 완료")

    def evaluating(self):
        ic("😊😊 평가 시작")
        ic("😊😊 평가 완료")

    def submit(self):
        ic("😊😊 제출 시작")
        ic("😊😊 제출 완료")

