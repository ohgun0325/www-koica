# ************
# NLTK 자연어 처리 패키지
# ************
"""
https://datascienceschool.net/view-notebook/118731eec74b4ad3bdd2f89bab077e1b/
NLTK(Natural Language Toolkit) 패키지는 
교육용으로 개발된 자연어 처리 및 문서 분석용 파이썬 패키지다. 
다양한 기능 및 예제를 가지고 있으며 실무 및 연구에서도 많이 사용된다.
NLTK 패키지가 제공하는 주요 기능은 다음과 같다.
말뭉치
토큰 생성
형태소 분석
품사 태깅
"""

import nltk
from nltk.tokenize import sent_tokenize, word_tokenize, RegexpTokenizer
from nltk.stem import PorterStemmer, LancasterStemmer, WordNetLemmatizer
from nltk.tag import pos_tag, untag
from nltk import Text, FreqDist
from wordcloud import WordCloud
import matplotlib
matplotlib.use('Agg')  # GUI 백엔드 사용 안 함 (서버 환경)
import matplotlib.pyplot as plt


class EmmaWordCloud:
    """
    Emma 소설을 분석하여 워드클라우드를 생성하는 클래스
    
    NLTK를 사용하여 자연어 처리를 수행하고,
    워드클라우드 시각화를 제공합니다.
    """
    
    def __init__(self, corpus_name="austen-emma.txt", stopwords=None):
        """
        초기화 메서드
        
        Args:
            corpus_name: 분석할 말뭉치 파일명 (기본값: "austen-emma.txt")
            stopwords: 제외할 단어 리스트 (기본값: None)
        """
        # NLTK 데이터 다운로드
        self._ensure_nltk_data()
        
        # 말뭉치 로드
        self.corpus_name = corpus_name
        self.raw_text = nltk.corpus.gutenberg.raw(corpus_name)
        
        # 기본 stopwords 설정
        if stopwords is None:
            self.stopwords = ["Mr.", "Mrs.", "Miss", "Mr", "Mrs", "Dear"]
        else:
            self.stopwords = stopwords
        
        # 토크나이저 초기화
        self.regex_tokenizer = RegexpTokenizer("[\w]+")
        
        # 형태소 분석기 초기화
        self.porter_stemmer = PorterStemmer()
        self.lancaster_stemmer = LancasterStemmer()
        self.lemmatizer = WordNetLemmatizer()
        
        # 분석 결과 저장
        self.tokens = None
        self.tagged_tokens = None
        self.text = None
        self.freq_dist = None
    
    def get_raw_text(self, length=None):
        """
        원문 텍스트 반환
        
        Args:
            length: 반환할 텍스트 길이 (None이면 전체)
            
        Returns:
            원문 텍스트
        """
        if length:
            return self.raw_text[:length]
        return self.raw_text
    
    def tokenize_sentences(self, text=None, length=1000):
        """
        문장 단위 토큰화
        
        Args:
            text: 토큰화할 텍스트 (None이면 raw_text 사용)
            length: 사용할 텍스트 길이
            
        Returns:
            문장 리스트
        """
        if text is None:
            text = self.raw_text[:length]
        return sent_tokenize(text)
    
    def tokenize_words(self, text=None, start=50, end=100):
        """
        단어 단위 토큰화
        
        Args:
            text: 토큰화할 텍스트 (None이면 raw_text 사용)
            start: 시작 위치
            end: 끝 위치
            
        Returns:
            단어 토큰 리스트
        """
        if text is None:
            text = self.raw_text[start:end]
        return word_tokenize(text)
    
    def tokenize_regex(self, text=None, start=50, end=100):
        """
        정규표현식을 사용한 토큰화
        
        Args:
            text: 토큰화할 텍스트 (None이면 raw_text 사용)
            start: 시작 위치
            end: 끝 위치
            
        Returns:
            토큰 리스트
        """
        if text is None:
            text = self.raw_text[start:end]
        return self.regex_tokenizer.tokenize(text)
    
    def stem_porter(self, words):
        """
        Porter Stemmer를 사용한 어간 추출
        
        Args:
            words: 어간 추출할 단어 리스트
            
        Returns:
            어간 추출된 단어 리스트
        """
        return [self.porter_stemmer.stem(w) for w in words]
    
    def stem_lancaster(self, words):
        """
        Lancaster Stemmer를 사용한 어간 추출
        
        Args:
            words: 어간 추출할 단어 리스트
            
        Returns:
            어간 추출된 단어 리스트
        """
        return [self.lancaster_stemmer.stem(w) for w in words]
    
    def lemmatize(self, words, pos=None):
        """
        원형 복원 (Lemmatization)
        
        Args:
            words: 원형 복원할 단어 리스트 또는 단일 단어
            pos: 품사 태그 (예: "v", "n")
            
        Returns:
            원형 복원된 단어 리스트 또는 단일 단어
        """
        if isinstance(words, str):
            if pos:
                return self.lemmatizer.lemmatize(words, pos=pos)
            return self.lemmatizer.lemmatize(words)
        else:
            if pos:
                return [self.lemmatizer.lemmatize(w, pos=pos) for w in words]
            return [self.lemmatizer.lemmatize(w) for w in words]
    
    def _ensure_nltk_data(self):
        """필요한 NLTK 데이터가 있는지 확인하고 없으면 다운로드"""
        # 필요한 리소스 목록
        resources = [
            'book',
            'punkt',
            'wordnet',
            'averaged_perceptron_tagger_eng'
        ]
        
        for resource in resources:
            try:
                # 리소스가 이미 있는지 확인
                if resource == 'averaged_perceptron_tagger_eng':
                    nltk.data.find('taggers/averaged_perceptron_tagger_eng/averaged_perceptron_tagger_eng.pickle')
                elif resource == 'book':
                    nltk.data.find('corpora/gutenberg')
                elif resource == 'punkt':
                    nltk.data.find('tokenizers/punkt')
                elif resource == 'wordnet':
                    nltk.data.find('corpora/wordnet')
            except LookupError:
                # 리소스가 없으면 다운로드
                try:
                    nltk.download(resource, quiet=True)
                    # 다운로드 후 다시 확인 (최대 3번 시도)
                    for attempt in range(3):
                        try:
                            if resource == 'averaged_perceptron_tagger_eng':
                                nltk.data.find('taggers/averaged_perceptron_tagger_eng/averaged_perceptron_tagger_eng.pickle')
                            elif resource == 'book':
                                nltk.data.find('corpora/gutenberg')
                            elif resource == 'punkt':
                                nltk.data.find('tokenizers/punkt')
                            elif resource == 'wordnet':
                                nltk.data.find('corpora/wordnet')
                            break  # 성공하면 루프 종료
                        except LookupError:
                            if attempt < 2:  # 마지막 시도가 아니면 재다운로드
                                nltk.download(resource, quiet=True)
                            else:
                                # eng 버전이 실패하면 일반 버전 시도
                                if resource == 'averaged_perceptron_tagger_eng':
                                    try:
                                        nltk.download('averaged_perceptron_tagger', quiet=True)
                                    except:
                                        pass
                except Exception as e:
                    # eng 버전이 실패하면 일반 버전 시도
                    if resource == 'averaged_perceptron_tagger_eng':
                        try:
                            nltk.download('averaged_perceptron_tagger', quiet=True)
                        except:
                            pass
    
    def pos_tagging(self, tokens=None):
        """
        품사 태깅
        
        Args:
            tokens: 태깅할 토큰 리스트 (None이면 전체 텍스트 사용)
            
        Returns:
            (단어, 품사) 튜플 리스트
        """
        # 필요한 NLTK 데이터 확인 및 다운로드
        self._ensure_nltk_data()
        
        # pos_tag 사용 전에 반드시 리소스 확인
        try:
            nltk.data.find('taggers/averaged_perceptron_tagger_eng/averaged_perceptron_tagger_eng.pickle')
        except LookupError:
            try:
                nltk.data.find('taggers/averaged_perceptron_tagger/averaged_perceptron_tagger.pickle')
            except LookupError:
                # 리소스가 없으면 다운로드 시도
                try:
                    nltk.download('averaged_perceptron_tagger_eng', quiet=False)
                except:
                    try:
                        nltk.download('averaged_perceptron_tagger', quiet=False)
                    except Exception as e:
                        raise RuntimeError(f"NLTK tagger 리소스를 다운로드할 수 없습니다: {e}")
        
        if tokens is None:
            tokens = self.regex_tokenizer.tokenize(self.raw_text)
        self.tagged_tokens = pos_tag(tokens)
        return self.tagged_tokens
    
    def get_nouns(self, tagged_list=None):
        """
        명사만 추출
        
        Args:
            tagged_list: 태깅된 토큰 리스트 (None이면 self.tagged_tokens 사용)
            
        Returns:
            명사 리스트
        """
        if tagged_list is None:
            if self.tagged_tokens is None:
                self.pos_tagging()
            tagged_list = self.tagged_tokens
        return [t[0] for t in tagged_list if t[1] == "NN"]
    
    def remove_tags(self, tagged_list):
        """
        태그 제거
        
        Args:
            tagged_list: 태깅된 토큰 리스트
            
        Returns:
            태그가 제거된 토큰 리스트
        """
        return untag(tagged_list)
    
    def create_tokenizer(self, tagged_list):
        """
        토큰과 품사를 결합한 토크나이저 함수 생성
        
        Args:
            tagged_list: 태깅된 토큰 리스트
            
        Returns:
            토크나이저 함수
        """
        def tokenizer(doc):
            return ["/".join(p) for p in tagged_list]
        return tokenizer
    
    def create_text_object(self, name="Emma"):
        """
        NLTK Text 객체 생성
        
        Args:
            name: Text 객체 이름
            
        Returns:
            Text 객체
        """
        tokens = self.regex_tokenizer.tokenize(self.raw_text)
        self.text = Text(tokens, name=name)
        return self.text
    
    def plot_word_frequency(self, num_words=20):
        """
        단어 빈도 그래프 그리기
        
        Args:
            num_words: 표시할 단어 개수
        """
        if self.text is None:
            self.create_text_object()
        self.text.plot(num_words)
        plt.show()
    
    def plot_dispersion(self, words):
        """
        단어 분산 플롯
        
        Args:
            words: 분석할 단어 리스트
        """
        if self.text is None:
            self.create_text_object()
        self.text.dispersion_plot(words)
    
    def show_concordance(self, word, lines=5):
        """
        단어 사용 위치 표시
        
        Args:
            word: 찾을 단어
            lines: 표시할 줄 수
        """
        if self.text is None:
            self.create_text_object()
        self.text.concordance(word, lines=lines)
    
    def find_similar_words(self, word, num=10):
        """
        유사한 문맥에서 사용된 단어 찾기
        
        Args:
            word: 기준 단어
            num: 반환할 단어 개수
            
        Returns:
            유사 단어 리스트
        """
        if self.text is None:
            self.create_text_object()
        return self.text.similar(word, num)
    
    def find_collocations(self, num=10):
        """
        연어(collocation) 찾기
        
        Args:
            num: 반환할 연어 개수
        """
        if self.text is None:
            self.create_text_object()
        self.text.collocations(num)
    
    def create_freq_dist_from_text(self):
        """
        Text 객체로부터 빈도 분포 생성
        
        Returns:
            FreqDist 객체
        """
        if self.text is None:
            self.create_text_object()
        self.freq_dist = self.text.vocab()
        return self.freq_dist
    
    def create_freq_dist_from_names(self):
        """
        고유명사(NNP)로부터 빈도 분포 생성
        
        Returns:
            FreqDist 객체
        """
        if self.tagged_tokens is None:
            self.pos_tagging()
        
        names_list = [
            t[0] for t in self.tagged_tokens 
            if t[1] == "NNP" and t[0] not in self.stopwords
        ]
        self.freq_dist = FreqDist(names_list)
        return self.freq_dist
    
    def get_statistics(self, word="Emma"):
        """
        단어 통계 정보 반환
        
        Args:
            word: 분석할 단어
            
        Returns:
            (전체 단어 수, 단어 출현 횟수, 단어 출현 확률) 튜플
        """
        if self.freq_dist is None:
            self.create_freq_dist_from_names()
        return (
            self.freq_dist.N(),
            self.freq_dist[word],
            self.freq_dist.freq(word)
        )
    
    def get_most_common(self, num=5):
        """
        가장 빈번한 단어 반환
        
        Args:
            num: 반환할 단어 개수
            
        Returns:
            (단어, 빈도) 튜플 리스트
        """
        if self.freq_dist is None:
            self.create_freq_dist_from_names()
        return self.freq_dist.most_common(num)
    
    def generate_wordcloud(self, width=1000, height=600, background_color="white", 
                          random_state=0, show=True):
        """
        워드클라우드 생성 및 표시
        
        Args:
            width: 워드클라우드 너비
            height: 워드클라우드 높이
            background_color: 배경색
            random_state: 랜덤 시드
            show: 즉시 표시할지 여부
            
        Returns:
            WordCloud 객체
        """
        if self.freq_dist is None:
            self.create_freq_dist_from_names()
        
        wc = WordCloud(
            width=width,
            height=height,
            background_color=background_color,
            random_state=random_state
        )
        wc.generate_from_frequencies(self.freq_dist)
        
        if show:
            plt.imshow(wc)
            plt.axis("off")
            plt.show()
        
        return wc
    
    def analyze_full_pipeline(self):
        """
        전체 분석 파이프라인 실행
        
        Returns:
            분석 결과 딕셔너리
        """
        # 토큰화
        self.tokens = self.regex_tokenizer.tokenize(self.raw_text)
        
        # 품사 태깅
        self.pos_tagging(self.tokens)
        
        # Text 객체 생성
        self.create_text_object()
        
        # 빈도 분포 생성
        self.create_freq_dist_from_names()
        
        return {
            'total_tokens': len(self.tokens),
            'tagged_tokens': len(self.tagged_tokens),
            'freq_dist_size': self.freq_dist.N(),
            'most_common': self.get_most_common(10)
        }


# 사용 예제
if __name__ == "__main__":
    # 클래스 인스턴스 생성
    emma = EmmaWordCloud()
    
    # 원문 확인
    print("원문 미리보기:")
    print(emma.get_raw_text(1302))
    print("\n" + "="*50 + "\n")
    
    # 문장 토큰화 예제
    sentences = emma.tokenize_sentences(length=1000)
    print(f"문장 토큰화 결과 (첫 1000자): {len(sentences)}개 문장")
    if len(sentences) > 3:
        print(f"4번째 문장: {sentences[3]}")
    print("\n" + "="*50 + "\n")
    
    # 형태소 분석 예제
    words = ['lives', 'crying', 'flies', 'dying']
    print("형태소 분석 예제:")
    print(f"원본: {words}")
    print(f"Porter Stemmer: {emma.stem_porter(words)}")
    print(f"Lancaster Stemmer: {emma.stem_lancaster(words)}")
    print(f"Lemmatizer: {emma.lemmatize(words)}")
    print(f"Lemmatizer (동사): {emma.lemmatize('dying', pos='v')}")
    print("\n" + "="*50 + "\n")
    
    # POS 태깅 예제
    sentence = "Emma refused to permit us to obtain the refuse permit"
    tagged = emma.pos_tagging(word_tokenize(sentence))
    print("POS 태깅 예제:")
    print(tagged)
    print(f"명사만 추출: {emma.get_nouns(tagged)}")
    print("\n" + "="*50 + "\n")
    
    # 전체 분석 파이프라인 실행
    print("전체 분석 파이프라인 실행:")
    results = emma.analyze_full_pipeline()
    print(results)
    print("\n" + "="*50 + "\n")
    
    # 통계 정보
    print("통계 정보:")
    stats = emma.get_statistics("Emma")
    print(f"전체 단어 수: {stats[0]}")
    print(f"'Emma' 출현 횟수: {stats[1]}")
    print(f"'Emma' 출현 확률: {stats[2]:.4f}")
    print("\n" + "="*50 + "\n")
    
    # 가장 빈번한 단어
    print("가장 빈번한 단어 Top 5:")
    print(emma.get_most_common(5))
    print("\n" + "="*50 + "\n")
    
    # 워드클라우드 생성
    print("워드클라우드 생성 중...")
    emma.generate_wordcloud()
