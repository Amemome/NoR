# gui.py

import PySimpleGUI as sg
import os
from graph_executor import execute
from examples import get_example_code
from state_manager import NorStateManager

# 상태 관리자 생성
state = NorStateManager()

# 초기 테마 설정
sg.theme(state.theme)

def make_layout():
    return [
        [
            sg.Text("NoR", font=("NanumGothic", 14), pad=(5, 10)),
            sg.Text(f"파일명: {state.filename}", key="FILENAME", font=("NanumGothic", 10), pad=(5, 10)),
            sg.Push(),
            sg.Button("New Pad"),
            sg.Button("Reset"),
            sg.Button("Run"),
            sg.Button("Samples"),
            sg.Button("🌙 Light/Dark", key="THEME")
        ],
        [sg.Text("DSL 입력", font=("NanumGothic", 11))],
        [sg.Multiline(key="INPUT", size=(70, 20), font=("Courier", 11))],
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

# 윈도우 실행
window = sg.Window("NoR 실행기", make_layout(), finalize=True)

while True:
    event, values = window.read()
    if event in (sg.WINDOW_CLOSED, "종료"):
        break

    elif event == "New Pad":
        state.reset()
        window["INPUT"].update("")
        window["GRAPH"].update(filename="")
        window["OUTPUT"].update("")
        window["FILENAME"].update(f"파일명: {state.filename}")

    elif event == "Samples":
        sample = get_example_code("bar")
        state.filename = "example_bar_chart.nor"
        window["INPUT"].update(sample)
        window["FILENAME"].update(f"파일명: {state.filename}")
        window["GRAPH"].update(filename="")
        window["OUTPUT"].update("샘플을 불러왔습니다. Run을 눌러 실행하세요")

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
        state.toggle_theme()
        sg.theme(state.theme)
        window.close()
        window = sg.Window("NoR 실행기", make_layout(), finalize=True)

window.close()
