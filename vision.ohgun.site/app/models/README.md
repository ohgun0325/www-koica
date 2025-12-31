# 모델 관리 시스템

## 📁 구조

```
app/models/
├── __init__.py          # 패키지 초기화 및 공개 API
├── base.py              # 모델 인터페이스 (BaseLLMModel, BaseEmbeddingModel)
├── loader.py             # 모델 로더 (디스크에서 모델 로드)
├── manager.py            # 모델 매니저 (싱글톤, 생명주기 관리)
└── README.md             # 이 문서
```

## 🎯 설계 원칙

### 1. 인터페이스 기반 설계
- `BaseLLMModel`: 모든 채팅 모델의 기본 인터페이스
- `BaseEmbeddingModel`: 모든 임베딩 모델의 기본 인터페이스
- LangChain의 `BaseChatModel` 및 `Embeddings`와 호환

### 2. 관심사의 분리
- **Loader**: 모델 파일을 디스크에서 로드
- **Manager**: 모델 인스턴스의 생명주기 관리 및 캐싱
- **Base**: 모델 인터페이스 정의

### 3. 확장 가능성
- 새로운 모델 형식 추가 시 `BaseLLMModel` 구현만 하면 됨
- HuggingFace, ONNX, TensorFlow 등 다양한 형식 지원 가능

## 📦 모델 저장소 구조

```
models/                          # 프로젝트 루트의 models/ 디렉토리
├── model-name-1/               # 각 모델은 별도 디렉토리
│   ├── model.safetensors       # 모델 가중치
│   ├── tokenizer.json          # 토크나이저
│   ├── tokenizer_config.json   # 토크나이저 설정
│   ├── config.json             # 모델 설정
│   ├── generation_config.json  # 생성 설정
│   └── ...
└── model-name-2/
    └── ...
```

## 🔧 사용 방법

### 1. 모델 구현 예시

```python
# app/models/huggingface.py (예시)
from typing import List, Any
from app.models.base import BaseLLMModel
from langchain_core.messages import BaseMessage

class HuggingFaceLLM(BaseLLMModel):
    """HuggingFace 모델 구현 예시."""

    def load(self) -> None:
        from transformers import AutoModelForCausalLM, AutoTokenizer

        self._tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        self._model = AutoModelForCausalLM.from_pretrained(self.model_path)
        self._is_loaded = True

    def unload(self) -> None:
        del self._model
        del self._tokenizer
        self._model = None
        self._tokenizer = None
        self._is_loaded = False

    def invoke(self, messages: List[Any]) -> Any:
        # 메시지를 텍스트로 변환
        text = self._format_messages(messages)

        # 토크나이징
        inputs = self._tokenizer(text, return_tensors="pt")

        # 생성
        outputs = self._model.generate(**inputs)

        # 디코딩
        response = self._tokenizer.decode(outputs[0], skip_special_tokens=True)

        return response
```

### 2. 모델 매니저 사용

```python
from app.models.manager import ModelManager

# 싱글톤 인스턴스 가져오기
manager = ModelManager()

# 사용 가능한 모델 목록 확인
models = manager.list_available_models()
print(f"Available models: {models}")

# 채팅 모델 로드
chat_model = manager.get_chat_model("my-model-name")

# 임베딩 모델 로드
embedding_model = manager.get_embedding_model("my-embedding-model")

# 모델 언로드
manager.unload_all()
```

### 3. 기존 코드와 통합

```python
# app/core/chat_chain.py 수정 예시
from app.models.manager import ModelManager
from app.models.base import BaseLLMModel

def chat_with_ai(
    conn,
    user_input: str,
    dimension: int,
    chat_model: Optional[BaseLLMModel] = None  # BaseLLMModel 사용
) -> str:
    # 모델 매니저에서 모델 가져오기
    if chat_model is None:
        manager = ModelManager()
        chat_model = manager.get_chat_model()

    # 기존 로직과 동일하게 사용
    # chat_model.invoke([system_message, human_message])
    ...
```

## ⚙️ 설정

`config.py`에서 모델 관련 설정:

```python
# .env 파일
LOCAL_MODELS_DIR=models
DEFAULT_CHAT_MODEL=my-chat-model
DEFAULT_EMBEDDING_MODEL=my-embedding-model
MODEL_DEVICE=cpu  # 또는 cuda, mps
MODEL_DTYPE=float32  # 또는 float16, bfloat16
```

## 🔄 모델 주입 흐름

```
1. 모델 파일 준비
   └── models/my-model/ 디렉토리에 모델 파일 복사

2. 모델 클래스 구현
   └── BaseLLMModel 또는 BaseEmbeddingModel 상속

3. ModelManager에 등록
   └── manager.get_chat_model("my-model", MyModelClass)

4. 사용
   └── chat_chain.py에서 모델 사용
```

## 📝 TODO

- [ ] HuggingFace 모델 구현 예시 추가
- [ ] 모델 레지스트리 패턴 구현 (선택적)
- [ ] 모델 버전 관리
- [ ] 모델 메타데이터 관리
- [ ] 모델 성능 모니터링

## 🎓 참고

- [LangChain Model Integration](https://python.langchain.com/docs/modules/model_io/)
- [HuggingFace Transformers](https://huggingface.co/docs/transformers/)
- [Model Loading Best Practices](https://huggingface.co/docs/transformers/main/en/model_sharing)

