import os
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class KoELECTRASentimentService:
    """KoELECTRA 모델을 사용한 감성 분석 서비스"""
    
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.device = None
        self.model_path = None
        
    def load_model(self, model_path: str = None):
        """모델과 토크나이저 로드"""
        if model_path is None:
            # 기본 경로: 현재 파일 기준 상대 경로
            current_dir = os.path.dirname(os.path.abspath(__file__))
            model_path = os.path.join(current_dir, "koelectra_model")
        
        self.model_path = model_path
        
        try:
            # 디바이스 설정 (GPU 사용 가능하면 GPU, 아니면 CPU)
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            logger.info(f"Using device: {self.device}")
            
            # 토크나이저 로드
            logger.info(f"Loading tokenizer from {model_path}")
            self.tokenizer = AutoTokenizer.from_pretrained(model_path)
            
            # 모델 로드
            # 주의: config.json이 ElectraForPreTraining이면 감성 분석용으로 fine-tuning이 필요할 수 있습니다
            logger.info(f"Loading model from {model_path}")
            
            # 감성 분석용 모델로 로드 시도
            try:
                self.model = AutoModelForSequenceClassification.from_pretrained(
                    model_path,
                    num_labels=2  # 긍정/부정 2개 클래스
                )
            except Exception as e:
                logger.warning(f"SequenceClassification 모델 로드 실패: {e}")
                # 기본 Electra 모델로 로드 후 분류 헤드 추가 시도
                from transformers import ElectraForSequenceClassification
                self.model = ElectraForSequenceClassification.from_pretrained(
                    model_path,
                    num_labels=2
                )
            
            self.model.to(self.device)
            self.model.eval()  # 평가 모드로 설정
            
            logger.info("Model loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise
    
    def predict(self, text: str) -> Dict[str, Any]:
        """
        텍스트의 감성을 분석합니다.
        
        Args:
            text: 분석할 텍스트
            
        Returns:
            감성 분석 결과 딕셔너리
        """
        if self.model is None or self.tokenizer is None:
            raise RuntimeError("Model is not loaded. Call load_model() first.")
        
        try:
            # 텍스트 토크나이징
            inputs = self.tokenizer(
                text,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=512
            )
            
            # 디바이스로 이동
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # 추론 (gradient 계산 비활성화)
            with torch.no_grad():
                outputs = self.model(**inputs)
                logits = outputs.logits
            
            # 확률 계산
            probabilities = torch.softmax(logits, dim=-1)
            probabilities = probabilities.cpu().numpy()[0]
            
            # 결과 해석
            # 일반적으로: 0 = 부정(negative), 1 = 긍정(positive)
            negative_score = float(probabilities[0])
            positive_score = float(probabilities[1])
            
            # 감성 결정
            if positive_score > negative_score:
                sentiment = "positive"
                confidence = positive_score
            else:
                sentiment = "negative"
                confidence = negative_score
            
            return {
                "text": text,
                "sentiment": sentiment,
                "confidence": round(confidence, 4),
                "positive_score": round(positive_score, 4),
                "negative_score": round(negative_score, 4)
            }
            
        except Exception as e:
            logger.error(f"Error during prediction: {e}")
            raise


# 싱글톤 인스턴스
_sentiment_service = None


def get_sentiment_service() -> KoELECTRASentimentService:
    """싱글톤 패턴으로 서비스 인스턴스 반환"""
    global _sentiment_service
    if _sentiment_service is None:
        _sentiment_service = KoELECTRASentimentService()
    return _sentiment_service

