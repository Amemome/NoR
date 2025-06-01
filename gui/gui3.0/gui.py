import PySimpleGUI as sg
import os
from graph_executor import execute
from examples import get_example_code
from state_manager import NorStateManager

state = NorStateManager()
sg.theme(state.theme)

def get_colors():
    if state.theme == "LightGrey1":
        return {"bg": "#f5f5f5", "fg": "#222", "outbg": "#f5f5f5", "outfg": "#d32f2f"}
    else:
        return {"bg": "#181c24", "fg": "#e6e6e6", "outbg": "#181c24", "outfg": "#f87171"}

def make_layout(input_text="", output_text="", filename=None, graph_path="", scale=1.0):
    colors = get_colors()
    fname = filename if filename is not None else state.filename
    graph_width = int(400 * scale)
    graph_height = int(300 * scale)
    return [
        [
            sg.Text("NoR", font=("NanumGothic", 14), pad=(5, 10)),
            sg.Text(f"파일명: {fname}", key="FILENAME", font=("NanumGothic", 10), pad=(5, 10)),
            sg.Push(),
            sg.Button("New Pad", key="NEW"),
            sg.Button("Reset", key="RESET"),
            sg.Button("Samples", key="SAMPLE"),
            sg.Button("Run", key="RUN", bind_return_key=True),
            sg.Button("🌙 Theme", key="THEME"),
            sg.Button("Help/Docs", key="HELP")
        ],
        [sg.Text("명령어 입력", font=("NanumGothic", 11))],
        [sg.Multiline(
            key="INPUT", size=(70, 20), font=("Courier", 11),
            background_color=colors["bg"], text_color=colors["fg"], border_width=1, default_text=input_text
        )],
        [
            sg.Column([
                [sg.Text("그래프 출력", font=("NanumGothic", 11)),
                 sg.Button("＋", key="ZOOM_IN", size=(2,1)), sg.Button("－", key="ZOOM_OUT", size=(2,1))],
                [sg.Image(filename=graph_path, key="GRAPH", size=(graph_width, graph_height), right_click_menu=['', ['복사', '저장']])]
            ], pad=(0, 0)),
            sg.VSeparator(),
            sg.Column([
                [sg.Text("명령어 결과 (dict)", font=("NanumGothic", 11))],
                [sg.Multiline(
                    key="OUTPUT", size=(45, 18), font=("Courier", 10),
                    background_color=colors["outbg"], text_color=colors["outfg"], disabled=True, border_width=1, default_text=output_text
                )]
            ], pad=(0, 0))
        ]
    ]

graph_scale = 1.0
input_text, output_text, graph_path, filename = "", "", "", state.filename
window = sg.Window("NoR 실행기", make_layout(scale=graph_scale), finalize=True, resizable=True, return_keyboard_events=True)

while True:
    event, values = window.read()
    if event in (sg.WINDOW_CLOSED, "종료"):
        break

    if event == "NEW":
        input_text, output_text, graph_path, filename = "", "", "", "untitled.nor"
        graph_scale = 1.0
        state.reset()
        window.close()
        window = sg.Window("NoR 실행기", make_layout(input_text, output_text, filename, graph_path, graph_scale), finalize=True, resizable=True, return_keyboard_events=True)
        continue
    elif event == "RESET":
        input_text, output_text, graph_path, filename = "", "", "", state.filename
        graph_scale = 1.0
        state.reset()
        window.close()
        window = sg.Window("NoR 실행기", make_layout(input_text, output_text, filename, graph_path, graph_scale), finalize=True, resizable=True, return_keyboard_events=True)
        sg.popup("전체 상태가 초기화되었습니다.", title="Reset")
        continue
    elif event == "SAMPLE":
        input_text = get_example_code("bar")
        filename = "example_bar_chart.nor"
        output_text = "샘플을 불러왔습니다. Run을 눌러 실행하세요"
        graph_path = ""
        graph_scale = 1.0
        state.filename = filename
        window.close()
        window = sg.Window("NoR 실행기", make_layout(input_text, output_text, filename, graph_path, graph_scale), finalize=True, resizable=True, return_keyboard_events=True)
        continue
    elif event == "RUN" or event in ("<Control-Return>", "<Command-Return>"):
        try:
            command = state.parse_input(values["INPUT"])
            execute(command)
            graph_path = command["save"] if os.path.exists(command["save"]) else ""
            output_text = str(command)
            input_text = values["INPUT"]
            filename = state.filename
            window.close()
            window = sg.Window("NoR 실행기", make_layout(input_text, output_text, filename, graph_path, graph_scale), finalize=True, resizable=True, return_keyboard_events=True)
        except Exception as e:
            output_text = f"⚠️ 실행 오류: {str(e)}"
            input_text = values["INPUT"]
            filename = state.filename
            window.close()
            window = sg.Window("NoR 실행기", make_layout(input_text, output_text, filename, graph_path, graph_scale), finalize=True, resizable=True, return_keyboard_events=True)
        continue
    elif event == "THEME":
        state.toggle_theme()
        sg.theme(state.theme)
        window.close()
        window = sg.Window("NoR 실행기", make_layout(input_text, output_text, filename, graph_path, graph_scale), finalize=True, resizable=True, return_keyboard_events=True)
        continue
    elif event == "ZOOM_IN":
        graph_scale = min(graph_scale + 0.2, 3.0)
        window.close()
        window = sg.Window("NoR 실행기", make_layout(input_text, output_text, filename, graph_path, graph_scale), finalize=True, resizable=True, return_keyboard_events=True)
        continue
    elif event == "ZOOM_OUT":
        graph_scale = max(graph_scale - 0.2, 0.4)
        window.close()
        window = sg.Window("NoR 실행기", make_layout(input_text, output_text, filename, graph_path, graph_scale), finalize=True, resizable=True, return_keyboard_events=True)
        continue
    elif event == "HELP":
        sg.popup("NoR DSL 문서 및 사용법은 ...\n(여기에 문서 링크 또는 설명 추가)", title="도움말/문서")
    elif isinstance(event, tuple) and event[0] == "GRAPH":
        if event[2] == "복사":
            sg.popup("이미지 복사 기능은 OS별로 다를 수 있습니다.\n(직접 파일을 복사해 주세요)", title="복사")
        elif event[2] == "저장":
            save_path = sg.popup_get_file("저장할 파일명", save_as=True, default_extension=".png")
            if save_path and os.path.exists(state.filename):
                import shutil
                shutil.copy(state.filename, save_path)
                sg.popup("이미지가 저장되었습니다.", title="저장 완료")

window.close() 