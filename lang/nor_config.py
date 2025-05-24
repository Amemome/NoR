# nor의 설정들을 관리하는 파일입니다.

# 각 속성들에 대해서 가능한 값들을 STRING으로 관리합니다.
# Lark 문법에서 *_VALUE 터미널로 대부분 검증되지만, Executor에서 매핑하거나,
# 일부 STRING 값에 대한 추가 검증이 필요할 때 사용할 수 있습니다.

# GRAPH_TYPE_VALUE
GRAPH_TYPES = {
    "선그래프", "선", "line", "line plot",
    "막대그래프", "막대", "bar", "bar plot",
    "산점도그래프", "산점도", "scatter", "scatter plot"
}

# COLOR_VALUE
COLOR_VALUES = {
    "검정", "black", "파랑", "blue", "갈색", "brown", "회색", "gray", "grey",
    "초록", "green", "주황", "orange", "분홍", "pink", "보라", "purple",
    "빨강", "red", "흰색", "white", "노랑", "yellow"
}

# MARKER_SHAPE_VALUE (grammar has more specific terminals like CIRCLE_MARKER)
# This set is for general reference or if a generic string is ever parsed.
MARKER_SHAPES = {
    "원", "o", "사각형", "네모", "s", "점", ".", "엑스", "x", "십자가",
    "삼각형", "세모", "^", "삼각형 위", "위쪽 삼각형",
    "삼각형 아래", "아래쪽 삼각형", "v",
    "삼각형 왼쪽", "왼쪽 삼각형", "<",
    "삼각형 오른쪽", "오른쪽 삼각형", ">",
    "별", "*", "별표"
}

# LINE_STYLE_VALUE
LINE_STYLES = {
    "실선", "-", "점선", ":", "파선", "--", "점선파선", "-."
}

# LEGEND_POSITION_VALUE
LEGEND_POSITIONS = {
    "최적", "best", "우상단", "upper right", "좌상단", "upper left",
    "좌하단", "lower left", "우하단", "lower right", "오른쪽", "right",
    "좌중앙", "center left", "우중앙", "center right", "하중앙", "lower center",
    "상중앙", "upper center", "중앙", "center"
}

# VALIDATION_RULES:
# Maps Object Selector Keyword Type to a dictionary of its valid Property Keyword Types.
# The value for a property keyword type can be:
#   - A specific value set (e.g., COLOR_VALUES) if further validation beyond grammar is needed (rare with new grammar).
#   - None: Indicates the grammar rule (e.g., STRING, NUMBER, VECTOR) is sufficient.
# This is primarily for SemanticAnalyzer to check if a property is applicable to an object.

VALIDATION_RULES = {
    # "그래프" 속성 지정자
    "GRAPH_KEYWORD": {
        "SET_TYPE_KEYWORD": GRAPH_TYPES, # Actually validated by GRAPH_TYPE_VALUE in grammar
        "SET_TITLE_KEYWORD": None,      # Validated as STRING by grammar
        "SET_LABEL_KEYWORD": None,      # Validated as STRING by grammar (for general graph label if ever used)
        "SET_LEGEND_KEYWORD": LEGEND_POSITIONS, # Validated by LEGEND_POSITION_VALUE
        "SET_FONT_KEYWORD": None,       # Validated as STRING
        "SET_BACKGROUND_KEYWORD": COLOR_VALUES, # Validated by COLOR_VALUE
        "ALPHA_KEYWORD": None,          # Validated as NUMBER
        "GRAPH_SIZE_KEYWORD": None,     # Validated as VECTOR
        "RESOLUTION_KEYWORD": None,     # Validated as NUMBER
        "INNER_BACKGROUND_COLOR_KEYWORD": COLOR_VALUES, # Validated by COLOR_VALUE
        "SAVE_FILE_KEYWORD": None,      # Validated as STRING
        # Note: Some keywords like SET_COLOR_KEYWORD might be too generic for GRAPH_KEYWORD
        # unless we define what "그래프의 색" means (e.g., default series color).
        # For now, let's assume it's not directly applicable or handled by more specific ones.
    },
    "X_AXIS_KEYWORD": {
        "SET_NAME_KEYWORD": None,       # Validated as STRING
        "SET_COLOR_KEYWORD": COLOR_VALUES, # Validated by COLOR_VALUE
        "SET_FONT_KEYWORD": None,       # Validated as STRING
        "SIZE_KEYWORD": None,           # (e.g., for font size) Validated as NUMBER
        "TICKS_KEYWORD": None,          # Validated as VECTOR
        "SET_LABEL_KEYWORD": None,      # For axis label, validated as STRING
    },
    # "X축" 속성 지정자
    "X_AXIS_KEYWORD": {
        "SET_NAME_KEYWORD": None, 
        "SET_COLOR_KEYWORD": COLOR_VALUES, 
        "SIZE_KEYWORD": None,

    },
    # "Y축" 속성 지정자
    "Y_AXIS_KEYWORD": {
        "SET_NAME_KEYWORD": None,       # Validated as STRING (often used for label)
        "SET_COLOR_KEYWORD": COLOR_VALUES, # Validated by COLOR_VALUE
        "SET_FONT_KEYWORD": None,       # Validated as STRING
        "SIZE_KEYWORD": None,           # (e.g., for font size) Validated as NUMBER
        "TICKS_KEYWORD": None,          # Validated as VECTOR
        "SET_LABEL_KEYWORD": None,      # For axis label, validated as STRING
    },
    "MARKER_KEYWORD": {
        "SET_TYPE_KEYWORD": MARKER_SHAPES, # Validated by MARKER_SHAPE_VALUE
        "SET_COLOR_KEYWORD": COLOR_VALUES, # Validated by COLOR_VALUE
        "SIZE_KEYWORD": None,           # Validated as NUMBER
        "ALPHA_KEYWORD": None,          # Validated as NUMBER
    },
    "LINE_KEYWORD": {
        "SET_TYPE_KEYWORD": LINE_STYLES, # Validated by LINE_STYLE_VALUE
        "SET_COLOR_KEYWORD": COLOR_VALUES, # Validated by COLOR_VALUE
        "SET_THICKNESS_KEYWORD": None,  # Validated as NUMBER
        "WIDTH_KEYWORD": None,          # (Synonym for thickness) Validated as NUMBER
        "ALPHA_KEYWORD": None,          # Validated as NUMBER
    }
}
