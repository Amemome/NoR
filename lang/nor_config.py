# nor_config.py

COLOR_VALUES = {
    "빨강", "파랑", "초록", "검정", "하양", "노랑", "보라", "분홍",
    "red", "blue", "green", "black", "white", "yellow", "purple", "pink"
}


MARKER_SHAPES = {"원", "사각형", "점", "엑스", "o", "s", ".", "x", "삼각형", "별"} # 마커 문양

LINE_STYLES = {"실선", "점선", "파선", "-", ":", "--", "-."} # 선 스타일

GRAPH_TYPES = {"선그래프", "막대그래프", "산점도"}

LEGEND_POSITIONS = {
    "best", "upper right", "upper left", "lower left", "lower right", "right",
    "center left", "center right", "lower center", "upper center", "center"
}

VALIDATE_RULES = {
    "GRAPH_KEYWORD": {
        "SET_TYPE_KEYWORD": GRAPH_TYPES,
        "SET_TITLE_KEYWORD": None,
        "SET_BACKGROUND_KEYWORD": COLOR_VALUES,
        "SET_LEGEND_KEYWORD": LEGEND_POSITIONS, 
        # ... (SIZE_KEYWORD, SET_COLOR_KEYWORD 등 일반 속성이 그래프 자체에 적용될 때)
    },
    "MARKER_KEYWORD": {
        "SET_TYPE_KEYWORD": MARKER_SHAPES, # 마커의 "종류" 또는 "문양"
        "SIZE_KEYWORD": None, # 마커의 "크기"
        "SET_COLOR_KEYWORD": COLOR_VALUES, # 마커의 "색"
        # "SET_BORDER_COLOR_KEYWORD": COLOR_VALUES (새로운 EBNF 터미널 필요)
    },
    "LINE_KEYWORD": {
        "SET_TYPE_KEYWORD": LINE_STYLES, # 선의 "종류" 또는 "스타일"
        "SET_THICKNESS_KEYWORD": None, # 선의 "굵기"
        "SET_COLOR_KEYWORD": COLOR_VALUES, # 선의 "색"
        # "SET_ALPHA_KEYWORD": None (새로운 EBNF 터미널 필요)
    },
    "X_AXIS_KEYWORD": {
        "SET_NAME_KEYWORD": None, # 축 "이름" (또는 SET_LABELS_KEYWORD와 연동)
        "SET_COLOR_KEYWORD": COLOR_VALUES, # 축 "색"
        "SIZE_KEYWORD": None, # 축 글꼴 "크기"

    },
    "Y_AXIS_KEYWORD": {
        "SET_NAME_KEYWORD": None,
        "SET_COLOR_KEYWORD": COLOR_VALUES,
        "SIZE_KEYWORD": None,
       
    },
}
