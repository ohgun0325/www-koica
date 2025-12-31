"""
😎😎 chat_service.py 서빙 관련 서비스

단순 채팅/대화형 LLM 인터페이스.

세션별 히스토리 관리, 요약, 토큰 절약 전략 등.
QLoRA 방식으로 모델을 로드하고 대화/학습을 지원합니다.
"""
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling,
)
from peft import (
    LoraConfig,
    get_peft_model,
    prepare_model_for_kbit_training,
    PeftModel,
    TaskType,
)
from datasets import Dataset

try:
    # Try the correct import path first
    from trl.trainer.sft_trainer import SFTTrainer  # type: ignore
    TRL_AVAILABLE = True
except ImportError:
    # If that fails, try alternative paths (for different trl versions)
    try:
        from trl.trainer import SFTTrainer  # type: ignore
        TRL_AVAILABLE = True
    except ImportError:
        try:
            from trl import SFTTrainer  # type: ignore
            TRL_AVAILABLE = True
        except ImportError:
            TRL_AVAILABLE = False
            SFTTrainer = None  # type: ignore


class QLoRAChatService:
    """QLoRA를 사용한 채팅 및 학습 서비스."""

    def __init__(
        self,
        model_name: str = "K-intelligence/Midm-2.0-Mini-Instruct",
        output_dir: str = "models/qlora_checkpoints",
        use_4bit: bool = True,
        bnb_4bit_compute_dtype: str = "float16",
        bnb_4bit_quant_type: str = "nf4",
        bnb_4bit_use_double_quant: bool = True,
        device_map: str = "auto",
    ):
        """QLoRA 채팅 서비스 초기화.

        Args:
            model_name: HuggingFace 모델 이름 또는 로컬 경로
            output_dir: 학습된 모델 저장 경로
            use_4bit: 4-bit 양자화 사용 여부
            bnb_4bit_compute_dtype: 계산 데이터 타입
            bnb_4bit_quant_type: 양자화 타입
            bnb_4bit_use_double_quant: 이중 양자화 사용 여부
            device_map: 디바이스 매핑 전략
        """
        self.model_name = model_name
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.device_map = device_map

        # BitsAndBytes 설정 (올바른 패턴)
        self.bnb_config = None
        if use_4bit and torch.cuda.is_available():
            self.bnb_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type=bnb_4bit_quant_type,
                bnb_4bit_compute_dtype=torch.float16,  # torch dtype 직접 사용
            )
            print("✅ 4-bit 양자화 설정 완료")

        self.model = None
        self.tokenizer = None
        self.peft_model = None
        self.is_loaded = False

    def load_model(self) -> None:
        """모델과 토크나이저를 로드하고 QLoRA를 적용합니다."""
        if self.is_loaded:
            print("⚠️  모델이 이미 로드되어 있습니다.")
            return

        print(f"📦 모델 로딩 중: {self.model_name}")

        # 토크나이저 로드
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name,
            trust_remote_code=True,
            padding_side="right",
        )

        # pad_token 설정
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
            self.tokenizer.pad_token_id = self.tokenizer.eos_token_id

        # 모델 로드 (올바른 패턴 적용)
        if self.bnb_config and torch.cuda.is_available():
            # QLoRA 방식: 4-bit 양자화 + cuda device_map
            print("🔧 4-bit 양자화 모드로 모델 로딩...")
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                quantization_config=self.bnb_config,
                device_map="cuda",
                trust_remote_code=True,
            )
        else:
            # 일반 모드
            print("🔧 일반 모드로 모델 로딩...")
            model_kwargs: dict = {
                "trust_remote_code": True,
                "device_map": "cuda" if torch.cuda.is_available() else "cpu",
                "torch_dtype": torch.float16 if torch.cuda.is_available() else torch.float32,
            }
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                **model_kwargs
            )

        # LoRA 설정
        lora_config = LoraConfig(
            task_type=TaskType.CAUSAL_LM,
            r=16,  # LoRA rank
            lora_alpha=32,  # LoRA alpha
            lora_dropout=0.1,
            target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],  # Midm 모델의 attention 모듈
            bias="none",
        )

        # PEFT 모델 적용 (올바른 패턴)
        print("🔧 LoRA 어댑터 적용 중...")
        self.peft_model = get_peft_model(self.model, lora_config)
        self.peft_model.print_trainable_parameters()

        self.is_loaded = True
        print("✅ QLoRA 모델 로드 완료")

    def load_peft_model(self, peft_model_path: str) -> None:
        """학습된 PEFT 모델을 로드합니다.

        Args:
            peft_model_path: PEFT 모델 경로
        """
        if not self.is_loaded:
            self.load_model()

        if self.model is None:
            raise RuntimeError("기본 모델이 로드되지 않았습니다. load_model()을 먼저 호출하세요.")

        print(f"📦 PEFT 모델 로딩 중: {peft_model_path}")
        self.peft_model = PeftModel.from_pretrained(
            self.model,
            peft_model_path,
            device_map=self.device_map,
        )
        print("✅ PEFT 모델 로드 완료")

    def chat(
        self,
        message: str,
        history: Optional[List[Dict[str, str]]] = None,
        max_new_tokens: int = 512,
        temperature: float = 0.7,
        top_p: float = 0.9,
    ) -> str:
        """대화형 채팅을 수행합니다.

        Args:
            message: 사용자 메시지
            history: 대화 히스토리 (선택사항)
            max_new_tokens: 최대 생성 토큰 수
            temperature: 생성 온도
            top_p: nucleus sampling 파라미터

        Returns:
            AI 응답
        """
        if not self.is_loaded:
            raise RuntimeError("모델이 로드되지 않았습니다. load_model()을 먼저 호출하세요.")

        if self.tokenizer is None:
            raise RuntimeError("토크나이저가 로드되지 않았습니다.")

        if self.peft_model is None:
            raise RuntimeError("PEFT 모델이 로드되지 않았습니다.")

        # 히스토리와 현재 메시지를 포맷팅
        if history is None:
            history = []

        # Midm instruction 포맷
        formatted_messages = []
        for h in history:
            if h.get("role") == "user":
                formatted_messages.append(f"질문: {h.get('content', '')}")
            elif h.get("role") == "assistant":
                formatted_messages.append(f"답변: {h.get('content', '')}")

        formatted_messages.append(f"질문: {message}")
        formatted_messages.append("답변:")

        prompt = "\n".join(formatted_messages)

        # 토크나이징 (token_type_ids 제외)
        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=2048,
            return_token_type_ids=False,  # Midm 모델은 token_type_ids를 사용하지 않음
        )

        # token_type_ids가 있으면 제거 (안전장치)
        if "token_type_ids" in inputs:
            inputs.pop("token_type_ids")

        # 디바이스로 이동
        if torch.cuda.is_available():
            inputs = {k: v.to("cuda") for k, v in inputs.items()}

        # 생성
        with torch.no_grad():
            outputs = self.peft_model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                temperature=temperature,
                top_p=top_p,
                do_sample=True,
                pad_token_id=self.tokenizer.pad_token_id,
                eos_token_id=self.tokenizer.eos_token_id,
            )

        # 디코딩
        generated_text = self.tokenizer.decode(
            outputs[0],
            skip_special_tokens=True
        )

        # 프롬프트 제거하고 답변만 추출
        if "답변:" in generated_text:
            response = generated_text.split("답변:")[-1].strip()
        else:
            response = generated_text[len(prompt):].strip()

        return response

    def train(
        self,
        training_data: List[Dict[str, str]],
        num_epochs: int = 3,
        batch_size: int = 4,
        learning_rate: float = 2e-4,
        save_steps: int = 100,
        logging_steps: int = 10,
        output_subdir: Optional[str] = None,
    ) -> str:
        """QLoRA 방식으로 모델을 학습합니다.

        Args:
            training_data: 학습 데이터 [{"instruction": "...", "input": "...", "output": "..."}]
            num_epochs: 학습 에포크 수
            batch_size: 배치 크기
            learning_rate: 학습률
            save_steps: 저장 간격
            logging_steps: 로깅 간격
            output_subdir: 출력 서브디렉토리

        Returns:
            학습된 모델 경로
        """
        if not self.is_loaded:
            raise RuntimeError("모델이 로드되지 않았습니다. load_model()을 먼저 호출하세요.")

        if self.tokenizer is None:
            raise RuntimeError("토크나이저가 로드되지 않았습니다.")

        if self.peft_model is None:
            raise RuntimeError("PEFT 모델이 로드되지 않았습니다.")

        print(f"🚀 학습 시작: {len(training_data)}개 샘플")

        # 데이터 포맷팅
        def format_prompt(example):
            instruction = example.get("instruction", "")
            input_text = example.get("input", "")
            output = example.get("output", "")

            if input_text:
                prompt = f"질문: {instruction}\n{input_text}\n답변: {output}"
            else:
                prompt = f"질문: {instruction}\n답변: {output}"

            return {"text": prompt}

        # 데이터셋 생성
        dataset = Dataset.from_list(training_data)
        dataset = dataset.map(format_prompt)

        # 출력 디렉토리 설정
        if output_subdir:
            output_path = self.output_dir / output_subdir
        else:
            output_path = self.output_dir / "latest"

        output_path.mkdir(parents=True, exist_ok=True)

        # 학습 인자 설정
        training_args = TrainingArguments(
            output_dir=str(output_path),
            num_train_epochs=num_epochs,
            per_device_train_batch_size=batch_size,
            gradient_accumulation_steps=4,
            learning_rate=learning_rate,
            fp16=torch.cuda.is_available(),
            logging_steps=logging_steps,
            save_steps=save_steps,
            save_total_limit=3,
            optim="paged_adamw_8bit" if self.bnb_config else "adamw_torch",
            warmup_steps=100,
            report_to="none",
        )

        # 데이터 콜레이터
        data_collator = DataCollatorForLanguageModeling(
            tokenizer=self.tokenizer,
            mlm=False,
        )

        # TRL의 SFTTrainer 사용 (가능한 경우)
        if TRL_AVAILABLE and SFTTrainer is not None:
            # SFTTrainer의 파라미터 확인 및 사용
            try:
                import inspect
                sig = inspect.signature(SFTTrainer.__init__)
                params = sig.parameters

                # SFTTrainer 파라미터에 따라 다르게 호출
                trainer_kwargs = {
                    "model": self.peft_model,
                    "train_dataset": dataset,
                    "args": training_args,
                }

                # tokenizer 파라미터가 있으면 추가 (SFTTrainer는 tokenizer를 받음)
                if "tokenizer" in params:
                    trainer_kwargs["tokenizer"] = self.tokenizer
                # Trainer는 tokenizer를 직접 받지 않으므로 여기서는 추가하지 않음

                # max_seq_length 파라미터가 있으면 추가
                if "max_seq_length" in params:
                    trainer_kwargs["max_seq_length"] = 2048

                # data_collator 파라미터가 있으면 추가
                if "data_collator" in params:
                    trainer_kwargs["data_collator"] = data_collator

                trainer = SFTTrainer(**trainer_kwargs)
            except Exception as e:
                print(f"⚠️  SFTTrainer 초기화 실패: {e}, 기본 Trainer 사용")
                trainer = Trainer(
                    model=self.peft_model,
                    train_dataset=dataset,
                    args=training_args,
                    data_collator=data_collator,
                )
        else:
            # 기본 Trainer 사용 (tokenizer는 data_collator에서 처리)
            trainer = Trainer(
                model=self.peft_model,
                train_dataset=dataset,
                args=training_args,
                data_collator=data_collator,
            )

        # 학습 실행
        trainer.train()

        # 모델 저장
        trainer.save_model()
        self.tokenizer.save_pretrained(str(output_path))

        print(f"✅ 학습 완료! 모델 저장 위치: {output_path}")

        return str(output_path)

    def save_model(self, save_path: Optional[str] = None) -> str:
        """현재 모델을 저장합니다.

        Args:
            save_path: 저장 경로 (None이면 기본 경로 사용)

        Returns:
            저장된 모델 경로
        """
        if not self.is_loaded:
            raise RuntimeError("모델이 로드되지 않았습니다.")

        if self.peft_model is None:
            raise RuntimeError("PEFT 모델이 로드되지 않았습니다.")

        if self.tokenizer is None:
            raise RuntimeError("토크나이저가 로드되지 않았습니다.")

        if save_path is None:
            save_path = str(self.output_dir / "latest")

        Path(save_path).mkdir(parents=True, exist_ok=True)

        self.peft_model.save_pretrained(save_path)
        self.tokenizer.save_pretrained(save_path)

        print(f"✅ 모델 저장 완료: {save_path}")
        return save_path

    def unload_model(self) -> None:
        """모델을 메모리에서 해제합니다."""
        if self.model is not None:
            del self.model
            self.model = None

        if self.peft_model is not None:
            del self.peft_model
            self.peft_model = None

        if self.tokenizer is not None:
            del self.tokenizer
            self.tokenizer = None

        if torch.cuda.is_available():
            torch.cuda.empty_cache()

        self.is_loaded = False
        print("✅ 모델 언로드 완료")


# 전역 서비스 인스턴스 (선택사항)
_global_service: Optional[QLoRAChatService] = None


def get_chat_service(
    model_name: str = "K-intelligence/Midm-2.0-Mini-Instruct",
    **kwargs
) -> QLoRAChatService:
    """전역 채팅 서비스 인스턴스를 가져오거나 생성합니다.

    Args:
        model_name: 모델 이름
        **kwargs: 추가 인자

    Returns:
        QLoRAChatService 인스턴스
    """
    global _global_service
    if _global_service is None:
        _global_service = QLoRAChatService(model_name=model_name, **kwargs)
    return _global_service
