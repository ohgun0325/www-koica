import re
import logging
from pathlib import Path
from datetime import datetime
import os

from konlpy.tag import Okt
from wordcloud import WordCloud
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)

class SamsungWordCloud:
  
    def __init__(self):
        self.okt = Okt()
    
    def text_process(self):
        """전체 텍스트 처리 파이프라인"""
        self.draw_wordcloud()
        return {'전처리 결과': '완료'}

    def read_file(self):
        """텍스트 파일 읽기"""
        fname = '../data/kr-Report_2018.txt'  # 파일명 수정
        # 상대 경로를 절대 경로로 변환
        current_dir = Path(__file__).parent
        file_path = current_dir.parent / 'data' / 'kr-Report_2018.txt'
        
        if not file_path.exists():
            # 다른 가능한 경로 시도
            file_path = current_dir.parent.parent / 'data' / 'kr-Report_2018.txt'
        
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        return text

    def extract_hangeul(self, text: str):
        """한글만 추출"""
        temp = text.replace('\n', ' ')
        tokenizer = re.compile(r'[^ ㄱ-ㅣ가-힣]+')
        result = tokenizer.sub('', temp)
        return result

    def change_token(self, texts: str):
        """텍스트를 토큰으로 분리"""
        # 한국어 텍스트의 경우 공백으로 분리하는 것이 더 적합할 수 있음
        # 하지만 기존 코드 유지를 위해 word_tokenize 사용
        if isinstance(texts, str):
            return texts.split()  # 공백으로 분리 (한국어에 더 적합)
        return texts
    
    def extract_noun(self):
        """명사 추출"""
        # 삼성전자의 스마트폰은 -> 삼성전자 스마트폰
        noun_tokens = []
        text = self.read_file()
        hangeul_text = self.extract_hangeul(text)
        tokens = self.change_token(hangeul_text)
        
        for i in tokens:
            pos_result = self.okt.pos(i)
            temp = [j[0] for j in pos_result if j[1] == 'Noun']
            if len(''.join(temp)) > 1:
                noun_tokens.append(''.join(temp))
        
        texts = ' '.join(noun_tokens)
        logger.info(f"명사 추출 완료: {len(noun_tokens)}개")
        return texts

    def read_stopword(self):
        """불용어 파일 읽기"""
        # 상대 경로를 절대 경로로 변환
        current_dir = Path(__file__).parent
        file_path = current_dir.parent / 'data' / 'stopwords.txt'
        
        if not file_path.exists():
            # 다른 가능한 경로 시도
            file_path = current_dir.parent.parent / 'data' / 'stopwords.txt'
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                stopwords = f.read()
            # 공백으로 구분된 불용어를 리스트로 변환
            stopwords_list = stopwords.split()
            return stopwords_list
        except FileNotFoundError:
            logger.warning(f"불용어 파일을 찾을 수 없습니다: {file_path}")
            return []

    def remove_stopword(self):
        """불용어 제거"""
        texts = self.extract_noun()
        tokens = self.change_token(texts)
        stopwords = self.read_stopword()
        
        # 불용어 제거
        filtered_texts = [text for text in tokens if text not in stopwords]
        logger.info(f"불용어 제거 완료: {len(tokens)} -> {len(filtered_texts)}개")
        return filtered_texts

    def draw_wordcloud(self, save_path: str = None, filename: str = None):
        """
        워드클라우드 생성 및 저장
        
        Args:
            save_path: 저장할 경로 (None이면 ../save/ 사용)
            filename: 저장할 파일명 (None이면 자동 생성)
        """
        texts = self.remove_stopword()
        
        # 폰트 경로 설정
        current_dir = Path(__file__).parent
        font_path = current_dir.parent / 'data' / 'D2Coding.ttf'
        
        if not font_path.exists():
            # 다른 가능한 경로 시도
            font_path = current_dir.parent.parent / 'data' / 'D2Coding.ttf'
        
        if font_path.exists():
            font_path = str(font_path)
        else:
            font_path = None  # 시스템 기본 폰트 사용
            logger.warning("한글 폰트를 찾을 수 없습니다. 시스템 기본 폰트를 사용합니다.")
        
        wcloud = WordCloud(
            font_path=font_path,
            relative_scaling=0.2,
            background_color='white'
        ).generate(" ".join(texts))
        
        plt.figure(figsize=(12, 12))
        plt.imshow(wcloud, interpolation='bilinear')
        plt.axis('off')
        
        # save 폴더에 저장
        if save_path is None:
            # 현재 파일 위치 기준으로 save 폴더 경로 설정
            current_dir = Path(__file__).parent  # samsung 폴더
            save_dir = current_dir.parent / 'save'  # nlp/save 폴더
            save_dir.mkdir(exist_ok=True)  # 폴더가 없으면 생성
            save_path = str(save_dir)
        
        # 파일명 자동 생성
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"wordcloud_{timestamp}.png"
        
        # 전체 경로 생성
        full_path = os.path.join(save_path, filename)
        
        # 파일 저장
        plt.savefig(full_path, dpi=300, bbox_inches='tight')
        print(f"워드클라우드 저장 완료: {full_path}")
        
        # 화면에 표시
        plt.show()
        
        return full_path