# NoR
NoR is a Python-based mini-language designed for quickly and easily creating graphs for academic papers.
NoR은 학술 논문용 그래프를 빠르고 쉽게 만들기 위해 설계된 Python 기반 미니 스크립트 언어입니다.

# 디렉토리 구성
```
/nor/
  ├── /gui/
  ├── /lang/     # 파서 & 인터프리터
  ├── /graph/    # matplotlib 호출
  ├── /examples/ # 예시 스크립트
  ├── /docs/     # 문서 모음
  ├── pyproject.toml # 프로젝트 표준 설정 파일. 프로젝트 의존성 패키지들과 버전을 명시
  ├── uv.lock # 프로젝트에 정확한 패키지 버전명을 고정.
  └── README.md
```
# 프로젝트 실행
해당 프로젝트는 python, uv, node 를 사용하고 있습니다. 
- python3을 사용할 수 있는 환경을 만들어주세요.
- uv를 사용할 수 있는 환경을 만들어주세요.
- node를 사용할 수 있는 환경을 만들어주세요.

1. 레포지토리 클론
```bash
git clone <repo_name>
cd <dir>
```
2. `.python-version` 의 파이썬 설치

3. 가상환경 생성 및 활성화
```bash
uv venv # 가상환경 생성
activate
```

## GUI 실행

/NoR 디렉토리에서
python -m gui.api_server
/gui 디렉토리에서
npm i
npm run dev

## CLI 실행



## uv 관련 명령어
- 현재 가상환경을 프로젝트에 정의된 상태와 일치시키는 명령 
`uv sync` 

- 의존성 (패키지) 를 설치
`uv pip install`

- 가상환경을 활성화
`activate`

- 가상환경을 비활성화
`deactivate`

- 가상환경 밖에서 실행
`uv run main.py`

아니면 가상환경이 활성화 되어있는 상태에서
python main.py


## 패키지 추가 (의존성 관리)

새로운 패키지를 프로젝트에 추가하거나 기존 패키지를 업데이트/제거할 때는 다음 절차를 따르세요. **모든 패키지 관련 작업은 가상환경이 활성화된 상태에서 진행해야 합니다.**
