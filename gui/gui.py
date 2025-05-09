# gui/gui.py

import PySimpleGUI as sg
import os

sg.theme("DarkGrey13")  # 다크모드 (라이트모드로 바꾸려면 theme 선택만 바꾸면 됨)

layout = [
    [sg.Text("NoR DSL 입력", font=("NanumGothic", 12))],
    [sg.Multiline(key="INPUT", size=(70, 20), font=("Courier", 11))],
    [sg.Button("예제 불러오기"), sg.Button("실행 (⌘+Enter)"), sg.Button("종료")],
    [
        sg.Column([
            [sg.Text("그래프 출력", font=("NanumGothic", 12))],
            [sg.Image(filename="", key="GRAPH", size=(400, 300))]
        ]),
        sg.VSeparator(),
        sg.Column([
            [sg.Text("변환된 명령어", font=("NanumGothic", 12))],
            [sg.Multiline(key="OUTPUT", size=(45, 18), font=("Courier", 10))]
        ])
    ]

]

window = sg.Window("NoR 실행기", layout, finalize=True)
window.bind("<Command_L>+Return", "실행 (⌘+Enter)")

while True:
    event, values = window.read()
    if event in (sg.WINDOW_CLOSED, "종료"):
        break

    elif event == "예제 불러오기":
        example_code = """데이터는 [
  ["카테고리", "값"],
  ["A", 10],
  ["B", 15],
  ["C", 7]
]
카테고리와 값을 그리기
그래프종류는 "막대"
제목은 "범주별 값 비교"
축이름은 "카테고리", "값"
저장은 "bar_chart.png"
"""
        window["INPUT"].update(example_code)

    elif event == "실행 (⌘+Enter)":
        # 아직 parser는 없으므로 dict 직접 사용
        from graph.graph_executor import execute
        import pandas as pd

        command = {
            "chart": "bar",
            "x": "카테고리",
            "y": ["값"],
            "data": [
                ["카테고리", "값"],
                ["A", 10],
                ["B", 15],
                ["C", 7]
            ],
            "title": "범주별 값 비교",
            "xlabel": "카테고리",
            "ylabel": "값",
            "save": "bar_chart.png"
        }

        try:
            execute(command)  # 그래프 생성
            if os.path.exists("bar_chart.png"):
                window["GRAPH"].update(filename="bar_chart.png")
            window["OUTPUT"].update(str(command))  # 변환된 명령어 출력
        except Exception as e:
            window["OUTPUT"].update(f"경고: 오류 발생: {str(e)}")

window.close()
