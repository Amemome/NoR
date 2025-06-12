# NoR (Node of Reasoning)

<div align="center">
  <img src="assets/nor-logo.png" alt="NoR Logo" width="200"/>
  
  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
  [![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
  [![React](https://img.shields.io/badge/React-18.0+-61DAFB.svg)](https://reactjs.org/)
</div>

## 📝 프로젝트 소개

NoR은 학술 논문용 그래프를 빠르고 쉽게 만들기 위해 설계된 Python 기반 미니 스크립트 언어입니다.

기존의 그래프 생성 도구들은 두 가지 극단에 있었습니다:
- Excel: GUI 기반으로 쉽지만 자동화와 반복 작업에 취약
- Matplotlib: 강력하지만 진입 장벽이 높고 문법이 복잡

NoR은 이 두 가지 사이의 중간점을 찾고자 하였습니다. 누구나 쉽게 접근할 수 있으면서도, 코드 기반으로 유연하게 그래프를 생성할 수 있는 간단하고 직관적인 한국어 스크립트 언어를 제공합니다.

## 👥 팀 소개

- **팀명**: NoR Team
- **멤버**:
  - [류지성](https://github.com/Amemome) - 언어 처리 엔진 개발 및 연동, 문법 정의
  - [최현경](https://github.com/broccoli-cake) - 프론트엔드 개발 및 연동, 문법 정의
  - [이운길](https://github.com/ungil0414) - 그래프 시각화 엔진 개발

## ✨ 주요 기능

- **직관적인 한국어 문법**
  - `그래프생성 "내 그래프"`와 같은 직관적인 명령어로 쉽게 그래프 생성
  - 복잡한 설정 없이도 원하는 결과를 얻을 수 있습니다

- **다양한 그래프 지원**
  - Line, Bar, Scatter 등 주요 그래프 유형 지원
  - 각 그래프마다 전용 함수를 통해 쉽게 생성 가능

- **쉬운 옵션 조정**
  - 제목, 글꼴, 크기 등을 명령어로 자유롭게 설정
  - 한글 색상 이름 지원 (예: "빨강", "파랑")

- **실시간 결과 확인**
  - 명령어 실행 즉시 결과를 확인할 수 있는 구조
  - 디버그 모드로 상세한 로그 확인 가능

## 🎥 데모 영상

[데모 영상 보기](https://example.com/demo)

## 🏗️ 시스템 아키텍처

NoR 시스템은 크게 세 가지 축으로 구성되어 있습니다:

1. **GUI (React + Tailwind)**
   - 코드 에디터: NoRScript 명령어 입력
   - 실행 결과 창: 그래프 시각화
   - 로그 및 출력 화면: 언어 처리 관련 로그

2. **언어 처리 (Lang)**
   - 구문 분석 (Parsing)
   - 의미 분석 (Semantic Analysis)
   - 실행 (Execution)

3. **그래프 생성 (Graph)**
   - Matplotlib 기반 시각화
   - 다양한 그래프 유형 지원
   - 한글 색상 및 스타일 지원

## 🚀 향후 발전 방향

- CSV 데이터 자동 파싱 및 변수명 자동 등록
- 명령어 자동완성 및 추천 기능
- 실행 이력 저장 및 즐겨찾기
- 그래프 이미지 다운로드 및 공유 기능
- 웹 배포 및 접근성 개선

## 📦 설치 및 사용법

```bash
# 저장소 클론
git clone https://github.com/your-username/nor.git

# 의존성 설치
pip install -r requirements.txt

# 실행
python main.py
```

## 🤝 기여 방법

1. 이슈를 생성하거나 기존 이슈를 확인합니다.
2. 브랜치를 생성하고 작업합니다.
3. PR을 생성하여 기여합니다.

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

# NoR
NoR is a Python-based mini-language designed for quickly and easily creating graphs for academic papers.
NoR은 학술 논문용 그래프를 빠르고 쉽게 만들기 위해 설계된 Python 기반 미니 스크립트 언어입니다.

# 디렉토리 구조
```
/NoR
├── cli/        # CLI 실행기 (커맨드라인)
├── core/       # 공통 인터프리터/분석 로직
├── docs/       # 프로젝트 문서
├── gui/        # GUI (프론트 + FastAPI 서버)
├── lang/       # 어휘 분석, 파서, 문법 정의
├── pyproject.toml
├── uv.lock
└── README.md

- `core/`: CLI와 GUI 모두에서 공유하는 **해석기 로직**이 들어 있습니다. 구조가 확장되면서 생긴 핵심 디렉토리입니다.
- `lang/`: 파서, 문법, 토큰 정의 등 언어의 핵심 구성 요소가 있습니다.
- `gui/`: 백엔드 (`FastAPI`)와 프론트엔드 (`React.js`)가 함께 있는 디렉토리입니다. `api_server.py`가 HTTP API를 제공합니다.
- `cli/`: CLI 진입점입니다. GUI 없이 실행 시 사용합니다.

# 프로젝트 실행

> 해당 프로젝트는 python3, uv, Node.js 환경이 필요합니다.  
- python3을 사용할 수 있는 환경을 만들어주세요.
- uv를 사용할 수 있는 환경을 만들어주세요.
- node를 사용할 수 있는 환경을 만들어주세요.

1. 레포지토리 클론 및 환경 준비

```bash
git clone <repo_url>
cd NoR
```

2. `.python-version`에 명시된 파이썬 설치 또는 pyenv로 설치

3. 가상환경 생성 및 활성화
```bash
uv venv   # 가상환경 생성
activate  # PowerShell or Bash 등에서 활성화
```

## GUI 실행

```bash
# 백엔드 실행 (루트 디렉토리에서)
python -m gui.api_server

# 프론트엔드 실행 (gui 디렉토리에서)
cd gui
npm install
npm run dev
```
---

## CLI 실행

루트 디렉토리에서

```bash
python -m cli.nor_cli <script_file> --debug
```

debug 옵션은 더 많은 정보를 로그에 제공합니다.

예시:

```bash
python -m cli.nor_cli test_scripts/dot_plot.nor
```


## 패키지 관리 (uv)

새로운 패키지를 프로젝트에 추가하거나 기존 패키지를 업데이트/제거할 때는 다음 절차를 따르세요. **모든 패키지 관련 작업은 가상환경이 활성화된 상태에서 진행해야 합니다.**

새로운 패키지를 추가하거나 기존 패키지를 수정할 때는 다음 명령어를 사용하세요:

```bash
uv pip install <패키지명>
uv pip uninstall <패키지명>
```

```bash
uv sync
```
를 사용하면 모든 변경 사항은 `pyproject.toml`과 `uv.lock`에 반영됩니다.

## 프로젝트 소개 영상

[![NoR 프로젝트 소개](https://img.youtube.com/vi/75B6PjQrmLo/0.jpg)](https://youtu.be/75B6PjQrmLo)

## 프로젝트 문서

자세한 프로젝트 문서는 [노션 페이지](https://open-cotton-965.notion.site/7-2065752e2f2380929194f40a427da5d1?source=copy_link)에서 확인하실 수 있습니다.

## 주요 기능

- 한글 기반의 직관적인 문법
- 복잡한 설정 없이 고품질 그래프 생성
- matplotlib, seaborn 등 강력한 시각화 라이브러리 활용

## 설치 방법

```bash
# 저장소 클론
git clone https://github.com/your-username/nor.git

# 의존성 설치
uv venv
uv pip install -r requirements.txt
```

## 사용 예시

```python
# 한글 스크립트로 그래프 생성
그리기([1, 2, 3, 4], [1, 4, 9, 16])
제목설정("제곱 함수")
축이름설정("x축", "y축")
저장("그래프.png")
```

## 라이선스

MIT License

## 기여 방법

1. 이슈 생성
2. 브랜치 생성 (`git checkout -b feature/amazing-feature`)
3. 변경사항 커밋 (`git commit -m 'Add some amazing feature'`)
4. 브랜치 푸시 (`git push origin feature/amazing-feature`)
5. Pull Request 생성

## 팀원

- 최현경 (32224802) - GUI 설계 및 프로젝트 문서화
- 이운길 (32237627) - 그래프 엔진 구현 및 테스트
- 류지성 (32241484) - 파서 및 언어 설계, GitHub 초기 세팅
