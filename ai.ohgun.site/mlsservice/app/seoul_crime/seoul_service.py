"""
서울 범죄 데이터 서비스
판다스, 넘파이를 사용한 데이터 처리 서비스
"""
import sys
import os
import logging
from pathlib import Path
from typing import List, Dict, Optional, Any
import pandas as pd
import numpy as np
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

# SeoulMethod import
from .seoul_method import SeoulMethod
from .kakao_map_singleton import KakaoMapSingleton


class SeoulService:
    """
    서울 범죄 데이터 서비스 클래스
    Java 스타일의 서비스 레이어 패턴 구현
    """
    def __init__(self):
        self.method = SeoulMethod()
        self.crime_rate_columns = ['살인검거율', '강도검거율', '강간검거율', '절도검거율', '폭력검거율']
        self.crime_columns = ['살인', '강도', '강간', '절도', '폭력']
        self.kakao_map = KakaoMapSingleton()  # 카카오맵 싱글턴 인스턴스

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
    
    def show_data_preview(self):
        """
        3개 데이터(CCTV, Crime, Population)의 상위 5개 목록을 화면에 출력
        """
        print("\n" + "="*80)
        print("🚀 서울 범죄 데이터 미리보기 시작")
        print("="*80)
        ic("😊😊 데이터 미리보기 시작")
        
        try:
            # 1. CCTV 데이터 로드 및 출력
            print("\n" + "="*80)
            print("📹 CCTV 데이터 로딩 중...")
            print("="*80)
            df_cctv = self.method.load_cctv()
            
            # 년도 컬럼 drop (2013년도 이전, 2014년, 2015년, 2016년)
            year_columns = ['2013년도 이전', '2014년', '2015년', '2016년']
            columns_to_drop = [col for col in year_columns if col in df_cctv.columns]
            if columns_to_drop:
                df_cctv = df_cctv.drop(columns=columns_to_drop)
            
            self._print_dataframe_info("CCTV", df_cctv)
            
            # API/로그 출력 (icecream)
            print(f'[IC] CCTV 데이터 타입\n {df_cctv.dtypes}')
            ic(f'CCTV 데이터 타입\n {df_cctv.dtypes}')
            print(f'[IC] CCTV 컬럼 목록\n {df_cctv.columns.tolist()}')
            ic(f'CCTV 컬럼 목록\n {df_cctv.columns.tolist()}')
            print(f'[IC] CCTV 상위 5개 행\n {df_cctv.head(5).to_dict(orient="records")}')
            ic(f'CCTV 상위 5개 행\n {df_cctv.head(5).to_dict(orient="records")}')
            print(f'[IC] CCTV Null 값 개수\n {df_cctv.isnull().sum().to_dict()}')
            ic(f'CCTV Null 값 개수\n {df_cctv.isnull().sum().to_dict()}')
            
            # 2. Crime 데이터 로드 및 출력
            print("\n" + "="*80)
            print("🚨 범죄 데이터 로딩 중...")
            print("="*80)
            df_crime = self.method.load_crime()
            self._print_dataframe_info("Crime", df_crime)
            
            # API/로그 출력 (icecream)
            print(f'[IC] Crime 데이터 타입\n {df_crime.dtypes}')
            ic(f'Crime 데이터 타입\n {df_crime.dtypes}')
            print(f'[IC] Crime 컬럼 목록\n {df_crime.columns.tolist()}')
            ic(f'Crime 컬럼 목록\n {df_crime.columns.tolist()}')
            print(f'[IC] Crime 상위 5개 행\n {df_crime.head(5).to_dict(orient="records")}')
            ic(f'Crime 상위 5개 행\n {df_crime.head(5).to_dict(orient="records")}')
            print(f'[IC] Crime Null 값 개수\n {df_crime.isnull().sum().to_dict()}')
            ic(f'Crime Null 값 개수\n {df_crime.isnull().sum().to_dict()}')
            
            # 3. Population 데이터 로드 및 출력
            print("\n" + "="*80)
            print("👥 인구 데이터 로딩 중...")
            print("="*80)
            df_population = self.method.load_population()
            self._print_dataframe_info("Population", df_population)
            
            # API/로그 출력 (icecream)
            print(f'[IC] Population 데이터 타입\n {df_population.dtypes}')
            ic(f'Population 데이터 타입\n {df_population.dtypes}')
            print(f'[IC] Population 컬럼 목록\n {df_population.columns.tolist()}')
            ic(f'Population 컬럼 목록\n {df_population.columns.tolist()}')
            print(f'[IC] Population 상위 5개 행\n {df_population.head(5).to_dict(orient="records")}')
            ic(f'Population 상위 5개 행\n {df_population.head(5).to_dict(orient="records")}')
            print(f'[IC] Population Null 값 개수\n {df_population.isnull().sum().to_dict()}')
            ic(f'Population Null 값 개수\n {df_population.isnull().sum().to_dict()}')
            
            print("\n" + "="*80)
            print("🎉 데이터 미리보기 완료!")
            print("="*80 + "\n")
            ic("😊😊 데이터 미리보기 완료")
            
            return {
                "status": "success",
                "cctv_shape": df_cctv.shape,
                "crime_shape": df_crime.shape,
                "population_shape": df_population.shape,
                "cctv_head": df_cctv.head(5).to_dict(orient='records'),
                "crime_head": df_crime.head(5).to_dict(orient='records'),
                "population_head": df_population.head(5).to_dict(orient='records')
            }
            
        except Exception as e:
            error_msg = f"데이터 로딩 중 오류 발생: {str(e)}"
            logger.error(error_msg)
            ic(error_msg)
            print(f"\n❌ {error_msg}")
            raise
    
    def get_police_stations_with_geocoding(self):
        """
        경찰서별 지오코딩 정보 조회
        - 범죄 데이터에서 관서명 추출
        - 카카오 로컬 API를 통해 각 경찰서의 좌표 정보 가져오기
        
        Returns:
            경찰서 개수와 지오코딩 정보
        """
        print("\n" + "="*80)
        print("🚔 경찰서 지오코딩 시작")
        print("="*80)
        
        try:
            # 범죄 데이터 로드
            df_crime = self.method.load_crime()
            police_stations = df_crime['관서명'].tolist()
            
            print(f"\n📍 총 {len(police_stations)}개 경찰서 발견")
            print(f"경찰서 목록: {', '.join(police_stations[:5])}...")
            
            # 각 경찰서의 지오코딩 정보 수집
            geocoding_results = []
            success_count = 0
            fail_count = 0
            # 키워드 검색 실패 시 사용할 주소/정확 명칭 매핑 (fallback)
            fallback_map = {
                # 축약형 → 주소
                "중랑서": "서울 중랑구 신내로 153",
                "도봉서": "서울 도봉구 노해로 403",
                "중부서": "서울 중구 수표로 27",
                "혜화서": "서울 종로구 율곡로 42",
                # 경찰서 풀네임 → 주소
                "중랑경찰서": "서울 중랑구 신내로 153",
                "도봉경찰서": "서울 도봉구 노해로 403",
                "중부경찰서": "서울 중구 수표로 27",
                "혜화경찰서": "서울 종로구 율곡로 42"
            }
            # 모든 검색이 실패했을 때 최종 좌표 하드코딩 (검증된 좌표)
            fallback_coords = {
                "중랑서": {"주소": "서울 중랑구 신내동 810", "경도": 127.10454224897, "위도": 37.6182390801576},
                "중랑경찰서": {"주소": "서울 중랑구 신내동 810", "경도": 127.10454224897, "위도": 37.6182390801576},
                "도봉서": {"주소": "서울 도봉구 창동 17", "경도": 127.05270598499145, "위도": 37.65339041848567},
                "도봉경찰서": {"주소": "서울 도봉구 창동 17", "경도": 127.05270598499145, "위도": 37.65339041848567},
            }
            
            for idx, station in enumerate(police_stations, 1):
                print(f"\n[{idx}/{len(police_stations)}] {station} 지오코딩 중...")
                
                try:
                    # 특정 관서는 바로 하드코딩 좌표 사용 (안정성 확보)
                    if station in fallback_coords:
                        fc = fallback_coords[station]
                        geocoding_info = {
                            '관서명': station,
                            '주소': fc['주소'],
                            '경도': fc['경도'],
                            '위도': fc['위도'],
                            '성공': True,
                            'fallback': 'hardcoded'
                        }
                        geocoding_results.append(geocoding_info)
                        success_count += 1
                        print(f"✅ 성공(하드코딩 우선): {fc['주소']}")
                        ic(f"{station} 좌표(하드코딩): ({fc['경도']}, {fc['위도']})")
                        continue
                    
                    tried = []
                    # 후보 키워드/주소 리스트 (순서대로 시도)
                    candidates = [
                        ("keyword", f"서울 {station}"),
                        ("keyword", f"서울 {station.replace('서','경찰서')}") if station.endswith("서") else None,
                        ("keyword", f"서울 {station} 경찰서"),
                        ("keyword", f"{station} 경찰서"),
                        ("keyword", station.replace("서","경찰서")) if station.endswith("서") else None,
                        ("address", fallback_map.get(station)) if station in fallback_map else None,
                    ]
                    candidates = [c for c in candidates if c and c[1]]
                    
                    result = {"documents": []}
                    for typ, query in candidates:
                        tried.append((typ, query))
                        print(f"🔎 시도({typ}): {query}")
                        result = self.kakao_map.search_keyword(query) if typ == "keyword" else self.kakao_map.geocode(query)
                        if result.get('documents'):
                            break
                    
                    # 최종 fallback: 좌표 하드코딩
                    if not result.get('documents') and station in fallback_coords:
                        fc = fallback_coords[station]
                        geocoding_info = {
                            '관서명': station,
                            '주소': fc['주소'],
                            '경도': fc['경도'],
                            '위도': fc['위도'],
                            '성공': True,
                            'fallback': 'hardcoded'
                        }
                        geocoding_results.append(geocoding_info)
                        success_count += 1
                        print(f"✅ 성공(하드코딩): {fc['주소']}")
                        ic(f"{station} 좌표(하드코딩): ({fc['경도']}, {fc['위도']})")
                        continue
                    
                    if result.get('documents'):
                        doc = result['documents'][0]
                        geocoding_info = {
                            '관서명': station,
                            '주소': doc.get('address_name', ''),
                            '경도': float(doc.get('x', 0)),
                            '위도': float(doc.get('y', 0)),
                            '성공': True
                        }
                        geocoding_results.append(geocoding_info)
                        success_count += 1
                        print(f"✅ 성공: {doc.get('address_name', '')}")
                        ic(f"{station} 좌표: ({geocoding_info['경도']}, {geocoding_info['위도']})")
                    else:
                        geocoding_results.append({
                            '관서명': station,
                            '주소': 'N/A',
                            '경도': 0,
                            '위도': 0,
                            '성공': False,
                            '오류': f"검색 결과 없음 | 시도: {tried}"
                        })
                        fail_count += 1
                        print(f"❌ 실패: 검색 결과 없음 | 시도: {tried}")
                        
                except Exception as e:
                    geocoding_results.append({
                        '관서명': station,
                        '주소': 'N/A',
                        '경도': 0,
                        '위도': 0,
                        '성공': False,
                        '오류': str(e)
                    })
                    fail_count += 1
                    print(f"❌ 오류: {str(e)}")
            
            print("\n" + "="*80)
            print(f"🎉 지오코딩 완료!")
            print(f"총 경찰서: {len(police_stations)}개")
            print(f"성공: {success_count}개 | 실패: {fail_count}개")
            print("="*80 + "\n")
            
            return {
                "status": "success",
                "total_count": len(police_stations),
                "success_count": success_count,
                "fail_count": fail_count,
                "police_stations": police_stations,
                "geocoding_results": geocoding_results
            }
            
        except Exception as e:
            error_msg = f"경찰서 지오코딩 중 오류 발생: {str(e)}"
            logger.error(error_msg)
            ic(error_msg)
            print(f"\n❌ {error_msg}")
            raise

    def merge_all_and_save(self):
        """
        1) CCTV+인구 머지
        2) 범죄+CCTV 머지
        3) 경찰서 지오코딩
        를 하나로 합쳐 save 폴더에 CSV 저장
        """
        # 1. CCTV+인구 (인구만 사용)
        df_cctv_pop = self.method.merge_cctv_pop()
        pop_part = df_cctv_pop.rename(columns={"구": "기관명"})
        pop_part = pop_part[["기관명"] + [c for c in pop_part.columns if c.startswith("인구_")]]

        # 2. 범죄+CCTV
        df_crime_cctv = self.method.merge_crime_cctv()

        # 키 컬럼 공백 제거
        pop_part["기관명"] = pop_part["기관명"].astype(str).str.strip()
        df_crime_cctv["기관명"] = df_crime_cctv["기관명"].astype(str).str.strip()

        # 3. 병합 (기관명 기준으로 인구 붙이기)
        merged = df_crime_cctv.merge(pop_part, on="기관명", how="left")

        # CCTV 연도별 컬럼 제거 요청 반영
        drop_cols = ["CCTV_2013년도 이전", "CCTV_2014년", "CCTV_2015년", "CCTV_2016년"]
        merged = merged.drop(columns=[c for c in drop_cols if c in merged.columns])

        # 4. 지오코딩 정보
        geo_result = self.get_police_stations_with_geocoding()
        df_geo = pd.DataFrame(geo_result.get("geocoding_results", []))
        if not df_geo.empty:
            merged = merged.merge(
                df_geo[["관서명", "주소", "경도", "위도"]],
                on="관서명",
                how="left"
            )

        # 5. 저장 경로
        save_dir = Path(self.method.dataset.sname)
        save_dir.mkdir(parents=True, exist_ok=True)
        save_path = save_dir / "seoul_merged_all.csv"
        # Excel 호환을 위해 BOM 포함 UTF-8로 저장
        merged.to_csv(save_path, index=False, encoding="utf-8-sig")

        print(f"✅ 통합 CSV 저장 완료: {save_path}")
        return {
            "status": "success",
            "save_path": str(save_path),
            "rows": len(merged),
            "cols": len(merged.columns),
            "columns": merged.columns.tolist()
        }

