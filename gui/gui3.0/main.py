import PySimpleGUI as sg
import customtkinter as ctk
from PIL import Image, ImageTk
import os

# 테마 설정
sg.theme('DarkBlue3')
sg.set_options(font=('Helvetica', 10))

def create_layout():
    # 메뉴바 레이아웃
    menu_layout = [
        [sg.Button('파일', key='-FILE-', button_color=('white', '#232733')), 
         sg.Button('편집', key='-EDIT-', button_color=('white', '#232733')),
         sg.Button('보기', key='-VIEW-', button_color=('white', '#232733')),
         sg.Button('도움말', key='-HELP-', button_color=('white', '#232733'))]
    ]

    # 에디터 패널 레이아웃
    editor_layout = [
        [sg.Multiline(size=(50, 20), key='-EDITOR-', font=('Courier', 12), background_color='#181c24', text_color='white')]
    ]

    # 결과 패널 레이아웃
    result_layout = [
        [sg.Multiline(size=(50, 20), key='-RESULT-', font=('Courier', 12), disabled=True, background_color='#181c24', text_color='white')]
    ]

    # 메인 레이아웃
    layout = [
        [sg.Column(menu_layout, background_color='#232733', pad=(0, 0))],
        [sg.Column(editor_layout, background_color='#181c24', pad=(0, 0)),
         sg.Column(result_layout, background_color='#181c24', pad=(0, 0))]
    ]

    return layout

def main():
    window = sg.Window('NoR GUI 3.0', 
                      create_layout(),
                      resizable=True,
                      finalize=True,
                      background_color='#181c24',
                      margins=(0, 0))

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break

        # 메뉴 이벤트 처리
        if event == '-FILE-':
            pass
        elif event == '-EDIT-':
            pass
        elif event == '-VIEW-':
            pass
        elif event == '-HELP-':
            pass

    window.close()

if __name__ == '__main__':
    main() 