import PySimpleGUI as sg
import os
from graph_executor import execute
from examples import get_example_code
from state_manager import NorStateManager

# 상태 관리 객체 생성
state = NorStateManager()

# 초기 테마 설정
sg.theme(state.theme)

def make_layout():
  theme_icon = "img/icon_light.png" if state.theme == "DarkGrey13" else "img/icon_dark.png"
  return [
    [
      sg.Text("NoR", font=("NanumGothic", 14), pad=(5, 10)),
      sg.Text(f"파일명: {state.filename}", key="FILENAME", font=("NanumGothic", 10), pad=(5, 10)),
      sg.Push(),
      sg.Button("New Pad"),
      sg.Button("Reset"),
      sg.Button("Run"),
      sg.Button("Samples", key="TOGGLE_SAMPLES"),
      sg.Button("", key="THEME", image_filename=theme_icon, image_size=(24, 24), tooltip="테마 전환", border_width=0)
    ],
    [  # 샘플 토글 리스트 (처음엔 숨김)
      sg.pin(sg.Column([
        [sg.Button("막대 그래프", key="SAMPLE_BAR")],
        [sg.Button("선 그래프", key="SAMPLE_LINE")],
        [sg.Button("산점도", key="SAMPLE_SCATTER")]
      ], key="SAMPLE_LIST", visible=False, pad=(0, 0)))
    ],
    [sg.Text("DSL 입력", font=("NanumGothic", 11))],
    [sg.Multiline(key="INPUT", size=(70, 20), font=("Courier", 11), enter_submits=True)],
    [
      sg.Column([
        [sg.Text("그래프 출력", font=("NanumGothic", 11))],
        [sg.Image(filename="", key="GRAPH", size=(400, 300))]
      ]),
      sg.VSeparator(),
      sg.Column([
        [sg.Text("명령어 결과 (dict)", font=("NanumGothic", 11))],
        [sg.Multiline(key="OUTPUT", size=(45, 18), font=("Courier", 10))]
      ])
    ]
  ]

# 메인 윈도우 생성
window = sg.Window("NoR 실행기", make_layout(), finalize=True, return_keyboard_events=True)

while True:
  event, values = window.read()

  # 단축키 처리
  if event in ("Control-Return", "Command-Return"):
    event = "Run"

  if event in (sg.WINDOW_CLOSED, "종료"):
    break

  elif event == "New Pad":
    state.reset()
    window["INPUT"].update("")
    window["GRAPH"].update(filename="")
    window["OUTPUT"].update("")
    window["FILENAME"].update(f"파일명: {state.filename}")

  elif event == "TOGGLE_SAMPLES":
    # 리스트 토글
    current = window["SAMPLE_LIST"].visible
    window["SAMPLE_LIST"].update(visible=not current)

  elif event.startswith("SAMPLE_"):
    sample_map = {
      "SAMPLE_BAR": "bar",
      "SAMPLE_LINE": "line",
      "SAMPLE_SCATTER": "scatter"
    }
    sample_type = sample_map[event]
    sample = get_example_code(sample_type)
    state.filename = f"example_{sample_type}_chart.nor"
    window["INPUT"].update(sample)
    window["FILENAME"].update(f"파일명: {state.filename}")
    window["GRAPH"].update(filename="")
    window["OUTPUT"].update(f"{sample_type} 샘플을 불러왔습니다. Run을 눌러 실행하세요")
    # 샘플 목록 자동 숨기기
    window["SAMPLE_LIST"].update(visible=False)

  elif event == "Run":
    try:
      command = state.parse_input(values["INPUT"])
      execute(command)
      if os.path.exists(command["save"]):
        window["GRAPH"].update(filename=command["save"])
      window["OUTPUT"].update(str(command))
    except Exception as e:
      window["OUTPUT"].update(f"⚠️ 실행 오류: {str(e)}")

  elif event == "THEME":
    input_text = values["INPUT"]
    output_text = values["OUTPUT"]
    graph_filename = None
    if "command" in locals() and isinstance(command, dict):
        graph_filename = command.get("save")

    state.toggle_theme()
    sg.theme(state.theme)

    theme_icon = "img/icon_light.png" if state.theme == "DarkGrey13" else "img/icon_dark.png"
    window.close()
    window = sg.Window("NoR 실행기", make_layout(), finalize=True, return_keyboard_events=True)

    window["INPUT"].update(input_text)
    window["OUTPUT"].update(output_text)
    if graph_filename and os.path.exists(graph_filename):
        window["GRAPH"].update(filename=graph_filename)
    window["FILENAME"].update(f"파일명: {state.filename}")

window.close()
