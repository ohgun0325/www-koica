"""
타이타닉 전처리 실행 스크립트
터미널에서 직접 실행하여 전처리 결과를 확인할 수 있습니다.
"""
import sys
from pathlib import Path

# 프로젝트 루트 경로 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 서비스 import 및 실행
from app.titanic.titanic_service import TitanicService

if __name__ == "__main__":
    print("="*80)
    print("타이타닉 전처리 실행")
    print("="*80)
    
    service = TitanicService()
    service.preprogress()
    
    print("\n✅ 실행 완료!")

