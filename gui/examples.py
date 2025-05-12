# examples.py

def get_example_code(name):
    if name == "bar":
        return """데이터는 [
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
    return ""
