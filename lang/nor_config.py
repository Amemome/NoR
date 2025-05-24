# nor의 설정들을 관리하는 파일입니다.


# 각 속성들에 대해서 가능한 값들을 STRING으로 관리합니다.

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

# 가능한 값 집합을 통해서 딕셔너리를 구성합니다.

VALIDATION_RULES = {
    # "그래프" 속성 지정자
    "GRAPH_KEYWORD": {
        "SET_TYPE_KEYWORD": GRAPH_TYPES,
        "SET_TITLE_KEYWORD": None,
        "SET_BACKGROUND_KEYWORD": COLOR_VALUES,
        "SET_LEGEND_KEYWORD": LEGEND_POSITIONS, 
        
    },
    # "마커" 속성 지정자
    "MARKER_KEYWORD": {
        "SET_TYPE_KEYWORD": MARKER_SHAPES,
        "SIZE_KEYWORD": None, 
        "SET_COLOR_KEYWORD": COLOR_VALUES, 
    },
    # "선" 속성 지정자
    "LINE_KEYWORD": {
        "SET_TYPE_KEYWORD": LINE_STYLES, 
        "SET_THICKNESS_KEYWORD": None,
        "SET_COLOR_KEYWORD": COLOR_VALUES,

    },
    # "X축" 속성 지정자
    "X_AXIS_KEYWORD": {
        "SET_NAME_KEYWORD": None, 
        "SET_COLOR_KEYWORD": COLOR_VALUES, 
        "SIZE_KEYWORD": None,

    },
    # "Y축" 속성 지정자
    "Y_AXIS_KEYWORD": {
        "SET_NAME_KEYWORD": None,
        "SET_COLOR_KEYWORD": COLOR_VALUES,
        "SIZE_KEYWORD": None,
    },
}
