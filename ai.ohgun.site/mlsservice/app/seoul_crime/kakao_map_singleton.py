import os
from pathlib import Path
import requests

class KakaoMapSingleton:
    _instance = None  # 싱글턴 인스턴스를 저장할 클래스 변수
    _base_url = "https://dapi.kakao.com/v2/local"

    def __new__(cls):
        if cls._instance is None:  # 인스턴스가 없으면 생성
            cls._instance = super(KakaoMapSingleton, cls).__new__(cls)
            cls._instance._api_key = cls._instance._retrieve_api_key()  # API 키 가져오기
            cls._instance._headers = {
                "Authorization": f"KakaoAK {cls._instance._api_key}"
            }
        return cls._instance  # 기존 인스턴스 반환

    def _retrieve_api_key(self):
        """
        API 키를 가져오는 내부 메서드
        - 우선 환경변수 KAKAO_REST_API_KEY 확인
        - 없으면 루트(.env)에서 KAKAO_REST_API_KEY 읽기
        """
        # 1) 환경변수 우선
        env_key = os.getenv("KAKAO_REST_API_KEY")
        if env_key:
            return env_key

        # 2) 루트(.env) 파일에서 읽기
        # kakao_map_singleton.py -> seoul_crime -> app -> mlsservice(프로젝트 루트)
        env_path = Path(__file__).resolve().parents[3] / ".env"
        if env_path.exists():
            for line in env_path.read_text(encoding="utf-8").splitlines():
                if line.startswith("KAKAO_REST_API_KEY="):
                    key = line.split("=", 1)[1].strip().strip('"').strip("'")
                    if key:
                        return key

        raise RuntimeError("KAKAO_REST_API_KEY를 환경변수나 .env에서 찾을 수 없습니다.")

    def get_api_key(self):
        """저장된 API 키 반환"""
        return self._api_key

    def geocode(self, address, language='ko'):
        """
        주소를 위도, 경도로 변환하는 메서드 (카카오맵 API 사용)
        
        Args:
            address: 검색할 주소
            language: 응답 언어 (ko, en 등)
            
        Returns:
            카카오맵 API 응답 데이터
        """
        url = f"{self._base_url}/search/address.json"
        params = {
            "query": address
        }
        
        try:
            response = requests.get(url, headers=self._headers, params=params)
            response.raise_for_status()  # HTTP 에러 발생 시 예외 발생
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"카카오맵 API 호출 중 오류 발생: {str(e)}")
    
    def search_keyword(self, keyword, language='ko'):
        """
        키워드로 장소를 검색하는 메서드 (카카오맵 API 사용)
        - 경찰서, 병원, 학교 등 키워드 검색에 적합
        
        Args:
            keyword: 검색할 키워드 (예: "서울 강남경찰서")
            language: 응답 언어 (ko, en 등)
            
        Returns:
            카카오맵 API 응답 데이터
        """
        url = f"{self._base_url}/search/keyword.json"
        params = {
            "query": keyword
        }
        
        try:
            response = requests.get(url, headers=self._headers, params=params)
            response.raise_for_status()  # HTTP 에러 발생 시 예외 발생
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"카카오맵 API 호출 중 오류 발생: {str(e)}")

