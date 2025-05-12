import PySimpleGUI as sg
import os
from graph_executor import execute
from examples import get_example_code
from state_manager import NorStateManager

# 상태 관리 객체 생성 (테마, 파일명, 입력 내용 등을 관리)
state = NorStateManager()

# 초기 테마 설정 (다크/라이트 등)
sg.theme(state.theme)

def make_layout():
  theme_icon = "img/icon_light.png" if state.theme == "DarkGrey13" else "img/icon_dark.png"
  """GUI 레이아웃을 생성하는 함수"""
  return [
    [
      sg.Text("NoR", font=("NanumGothic", 14), pad=(5, 10)),
      sg.Text(f"파일명: {state.filename}", key="FILENAME", font=("NanumGothic", 10), pad=(5, 10)),
      sg.Push(),  # 오른쪽 정렬용 공간 채우기
      sg.Button("New Pad"),
      sg.Button("Reset"),
      sg.Button("Run"),
      sg.Button("Samples"),
      sg.Button("", key="THEME", image_filename=theme_icon, image_size=(24, 24), tooltip="테마 전환", border_width=0)
    ],
    [sg.Text("DSL 입력", font=("NanumGothic", 11))],
    [sg.Multiline(key="INPUT", size=(70, 20), font=("Courier", 11))],
    [
      sg.Column([
        [sg.Text("그래프 출력", font=("NanumGothic", 11))],
        [sg.Image(filename="", key="GRAPH", size=(400, 300))]
      ]),
      sg.VSeparator(),  # 수직 구분선
      sg.Column([
        [sg.Text("명령어 결과 (dict)", font=("NanumGothic", 11))],
        [sg.Multiline(key="OUTPUT", size=(45, 18), font=("Courier", 10))]
      ])
    ]
  ]

# 메인 윈도우 생성 및 초기화
window = sg.Window("NoR 실행기", make_layout(), finalize=True)

# 이벤트 루프 시작
while True:
  event, values = window.read()
  if event in (sg.WINDOW_CLOSED, "종료"):
    # 창 닫기 또는 종료 버튼 클릭 시 루프 탈출
    break

  elif event == "New Pad":
    # 새 입력창 초기화: 상태 초기화, 모든 필드 클리어
    state.reset()
    window["INPUT"].update("")
    window["GRAPH"].update(filename="")
    window["OUTPUT"].update("")
    window["FILENAME"].update(f"파일명: {state.filename}")

  elif event == "Samples":
    # 샘플 코드 불러오기 ("bar" 예제)
    sample = get_example_code("bar")
    state.filename = "example_bar_chart.nor"
    window["INPUT"].update(sample)
    window["FILENAME"].update(f"파일명: {state.filename}")
    window["GRAPH"].update(filename="")
    window["OUTPUT"].update("샘플을 불러왔습니다. Run을 눌러 실행하세요")

  elif event == "Run":
    # 현재 입력된 DSL 코드를 실행하고 결과 반영
    try:
      command = state.parse_input(values["INPUT"])  # 입력 파싱
      execute(command)  # 그래프 실행
      if os.path.exists(command["save"]):  # 저장된 이미지가 존재하면 갱신
        window["GRAPH"].update(filename=command["save"])
      window["OUTPUT"].update(str(command))  # 명령어 dict 출력
    except Exception as e:
      # 실행 중 예외 발생 시 오류 메시지 출력
      window["OUTPUT"].update(f"⚠️ 실행 오류: {str(e)}")

  elif event == "THEME":
    # 현재 상태 백업
    input_text = values["INPUT"]
    output_text = values["OUTPUT"]
    graph_filename = None
    if "command" in locals() and isinstance(command, dict):
        graph_filename = command.get("save")

    # 테마 변경
    state.toggle_theme()
    sg.theme(state.theme)

     # 아이콘 결정
    theme_icon = "img/icon_light.png" if state.theme == "DarkGrey13" else "img/icon_dark.png"

    # 기존 창 닫고 새 창 열기
    window.close()
    window = sg.Window("NoR 실행기", make_layout(), finalize=True)

    # 상태 복원
    window["INPUT"].update(input_text)
    window["OUTPUT"].update(output_text)
    if graph_filename and os.path.exists(graph_filename):
        window["GRAPH"].update(filename=graph_filename)
    window["FILENAME"].update(f"파일명: {state.filename}")


# 프로그램 종료 시 윈도우 닫기
window.close()
