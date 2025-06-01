import matplotlib
matplotlib.use("Agg")  # GUI 백엔드 비활성화 (세그폴트 방지)

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import io

# 한글 폰트 설정
plt.rcParams['font.family'] = 'AppleGothic'  # 또는 AppleGothic, Malgun Gothic 등

# 경고 끄기 (선택)
plt.rcParams['axes.unicode_minus'] = False

def execute(command, scale=1.0):
    chart_type = command.get("chart")
    if chart_type == "bar":
        draw_bar_chart(command, scale)

def draw_bar_chart(command, scale=1.0):
    data = command["data"]
    headers = data[0]
    rows = data[1:]

    x_values = [row[0] for row in rows]
    y_values = [row[1] for row in rows]

    plt.figure(figsize=(6*scale, 4*scale))
    plt.bar(x_values, y_values)
    plt.title(command.get("title", ""))
    plt.xlabel(command.get("xlabel", headers[0]))
    plt.ylabel(command.get("ylabel", headers[1]))
    plt.tight_layout()
    plt.savefig(command["save"])
    plt.close()

def draw_bar_chart_bytes(command, scale=1.0):
    data = command["data"]
    headers = data[0]
    rows = data[1:]
    x_values = [row[0] for row in rows]
    y_values = [row[1] for row in rows]
    plt.figure(figsize=(6*scale, 4*scale))
    plt.bar(x_values, y_values)
    plt.title(command.get("title", ""))
    plt.xlabel(command.get("xlabel", headers[0]))
    plt.ylabel(command.get("ylabel", headers[1]))
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return buf.read() 