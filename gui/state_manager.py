# state_manager.py

class NorStateManager:
    def __init__(self):
        self.theme = "DarkGrey13"
        self.filename = "untitled.nor"

    def reset(self):
        self.filename = "untitled.nor"

    def toggle_theme(self):
        self.theme = "LightGrey1" if self.theme == "DarkGrey13" else "DarkGrey13"

    def parse_input(self, raw_text):
      if "line" in raw_text:
          return {
              "chart": "line",
              "data": [
                  ["시간", "온도"],
                  [0, 20],
                  [1, 21],
                  [2, 23],
                  [3, 22]
              ],
              "title": "시간에 따른 온도 변화",
              "xlabel": "시간(시)",
              "ylabel": "온도(℃)",
              "save": "line_chart.png"
          }
      elif "scatter" in raw_text:
          return {
              "chart": "scatter",
              "data": [
                  ["x", "y"],
                  [1, 2],
                  [2, 3.5],
                  [3, 1.5],
                  [4, 4]
              ],
              "title": "산점도 예시",
              "xlabel": "X축",
              "ylabel": "Y축",
              "save": "scatter_chart.png"
          }
      else:
          return {
              "chart": "bar",
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
