class NorStateManager:
    def __init__(self):
        self.theme = "DarkGrey13"
        self.filename = "untitled.nor"

    def reset(self):
        self.filename = "untitled.nor"

    def toggle_theme(self):
        self.theme = "LightGrey1" if self.theme == "DarkGrey13" else "DarkGrey13"

    def parse_input(self, raw_text):
        # TODO: parser 완성 시 교체 예정
        return {
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