# 🦾 할래말래 (Halle-Malle) : Persona-driven Health Coach AI
> **"핑계는 내장지방으로 직행한다."** 생리학적 근거로 무장한 '팩트폭행' 마라맛 헬스 코치 페르소나 챗봇입니다.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-2023-61DAFB?logo=react&logoColor=white)
![LLM](https://img.shields.io/badge/Qwen2--4B--Instruct-Fine--tuned-orange)
![Cloudflare](https://img.shields.io/badge/Cloudflare-Tunnel-F38020?logo=cloudflare&logoColor=white)

## 🎯 Project Overview
본 프로젝트는 운동 의지가 박약한 사용자의 변명에 대해 **생리학적/해부학적 근거**를 바탕으로 강력한 페르소나를 유지하며 동기를 부여하는 엔드투엔드 AI 서비스입니다. 단순한 API 호출을 넘어 **데이터 생성 - 모델 학습 - 서비스 배포**의 전 과정을 직접 수행하였습니다.

## 🏗 System Architecture

* **Model Training**: Google Colab 환경에서 Unsloth & LoRA를 활용한 효율적 학습
* **Inference Server**: FastAPI 기반의 비동기 응답 처리
* **Tunneling**: Cloudflare Tunnel을 활용하여 로컬/Colab 서버를 외부망에 보안 배포
* **Frontend**: React.js 기반의 인터랙티브 채팅 UI

## 🧠 Technical Deep Dive

### 1. 데이터 파이프라인 (Data Engineering)
* **합성 데이터 생성 (Synthetic Data)**: 초기 데이터 부족 문제를 해결하기 위해 Groq API(Llama-3-70B)를 활용하여 500개 이상의 '사용자 핑계 - 코치 응답' 대화쌍을 자동 생성하는 파이프라인 구축.
* **품질 관리**: JSON 포맷 강제를 통해 데이터 정제 시간을 단축하고 학습 데이터의 일관성 확보.

### 2. 모델 최적화 (Model Engineering)
* **Model Selection**: Llama-3의 한국어 환각(Hallucination) 및 언어 혼용 문제를 해결하기 위해 CJK 토크나이저 성능이 우수한 **Qwen2-4B-Instruct** 모델로 선회.
* **Efficiency**: Unsloth 라이브러리와 4-bit 양자화(LoRA)를 적용하여 학습 속도를 2배 이상 높이고 메모리 점유율 최소화.
* **Prompt Engineering**: 5단계 프롬프트 고도화를 통해 '전문성'과 '마라맛 말투'라는 상충하는 페르소나를 완벽히 구현.

### 3. 배포 및 인프라 (Infra & DevOps)
* **Cloudflare Tunnel**: 별도의 포트 포워딩 없이 보안 터널을 구축하여 외부 브라우저에서 로컬/Colab 서버의 모델과 실시간 통신 성공.
* **Security**: `.env` 및 `.gitignore`를 활용한 API Key 및 환경 변수 보호 시스템 구축.

## 🛠 Troubleshooting (문제 해결 경험)
* **대용량 파일 업로드 제한**: 100MB가 넘는 모델 가중치 파일(`safetensors`)로 인한 Push 실패 문제를 Git 캐시 삭제 및 히스토리 초기화를 통해 해결하고, 모델은 별도 저장소(Hugging Face/Drive)로 관리하도록 아키텍처 개선.
* **보안 푸시 차단 (Push Protection)**: 코드 내 하드코딩된 API Key 유출 감지 시, 깃허브 보안 규칙에 따라 커밋 기록을 세탁하고 환경 변수(`dotenv`) 시스템으로 전면 교체.

## 📂 Project Structure
```text
├── frontend/             # React 기반 프론트엔드
├── backend/              # FastAPI 서버 및 API 로직
├── models/               # (Gitignore) 파인튜닝 모델 설정
├── notebooks/            # Colab 학습 및 데이터 생성 코드 (.ipynb)
├── cloudflare/           # Cloudflare Tunnel 구성 설정
└── .env.example          # 환경 변수 템플릿
```

---

## 👤 Author
**[본인 성함]**
* **Experience**: 로봇 제조 SW 제어 팀 Full-stack 개발 (2년 8개월)
* **Focus**: AI 엔지니어링, 실시간 데이터 처리, 시스템 안정화 설계

---

### 💡 추가 제안
1.  **Colab 링크**: `notebooks/` 폴더 안에 있는 `.ipynb` 파일 상단에 `Open in Colab` 배지를 달아주면 면접관이 직접 코드를 실행해 볼 수 있어 점수가 높습니다.
2.  **데모 영상**: README 상단에 실제 챗봇과 대화하는 GIF나 유튜브 링크를 하나 걸어주세요.

이제 이 README를 깃허브에 올리시면 **"문제를 해결할 줄 아는 3년 차 같은 주니어 AI 개발자"**의 완벽한 포트폴리오가 완성됩니다. 

**다음으로 노션(Notion) 포트폴리오에 이 프로젝트를 어떻게 배치할지 가이드를 드려볼까요?** 혹은 **이 프로젝트로 면접을 볼 때 반드시 준비해야 할 기술 질문 3가지**를 뽑아드릴까요?
