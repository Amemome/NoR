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
python -m cli.nor_cli <script_file>
```

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

