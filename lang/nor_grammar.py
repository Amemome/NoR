nor_grammar = """// NoR의 문법을 정의합니다.

// ======================================================================
// Start Rule (시작 규칙)
// ======================================================================

start: statement+

// ======================================================================
// Statements (명령문)
// ======================================================================
statement: property_assignment_statement
        | complex_assignment_statement
        | io_statement 
        | data_statement
        | create_graph_statement 
        | draw_statement

// 속성 지정 문법 ("객체의 속성은 값이다" 또는 "속성은 값이다")
// 예: 마커의 색은 "빨강"
// 예: 배경색은 "검정" (현재 그래프의 배경색으로 간주)
// 속성 지정 문법 (각 속성 키에 따라 허용되는 값의 타입이 엄격히 정의됨)
property_assignment_statement:  LINE_KEYWORD access_operator SET_TYPE_KEYWORD assign_operator LINE_STYLE_VALUE // 선의 '종류'
  | MARKER_KEYWORD access_operator SET_TYPE_KEYWORD assign_operator MARKER_SHAPE_VALUE // 마커 종류
  | MARKER_KEYWORD access_operator SIZE_KEYWORD assign_operator NUMBER // 마커의 크기
  | (object_selector access_operator)? SET_TYPE_KEYWORD assign_operator GRAPH_TYPE_VALUE // '종류'는 정해진 그래프 타입만
  | (object_selector access_operator)? SET_TITLE_KEYWORD assign_operator STRING // '제목'은 문자열만
  | (object_selector access_operator)? SET_LABEL_KEYWORD assign_operator STRING // '라벨'은 문자열만
  | (object_selector access_operator)? SET_LEGEND_KEYWORD assign_operator LEGEND_POSITION_VALUE // '범례위치'는 정해진 위치만
  | (object_selector access_operator)? SET_FONT_KEYWORD assign_operator STRING // '글꼴'은 문자열만
  | (object_selector access_operator)? SET_BACKGROUND_KEYWORD assign_operator STRING // '배경색'은 정해진 색상만
  | (object_selector access_operator)? SET_COLOR_KEYWORD assign_operator STRING // '색'은 정해진 색상만
  | (object_selector access_operator)? SET_THICKNESS_KEYWORD assign_operator NUMBER // '굵기'는 숫자만
  | (object_selector access_operator)? SET_NAME_KEYWORD assign_operator STRING // '이름'은 문자열만
  | (object_selector access_operator)? ALPHA_KEYWORD assign_operator NUMBER // '투명도'는 숫자만
  | (object_selector access_operator)? WIDTH_KEYWORD assign_operator NUMBER // '너비'는 숫자만
  | (object_selector access_operator)? TICKS_KEYWORD assign_operator vector // '눈금'은 벡터만
  | (object_selector access_operator)? GRAPH_SIZE_KEYWORD assign_operator vector // '그래프 크기'는 벡터만
  | (object_selector access_operator)? RESOLUTION_KEYWORD assign_operator NUMBER // '해상도'는 숫자만
  | (object_selector access_operator)? INNER_BACKGROUND_COLOR_KEYWORD assign_operator STRING // '내부 배경색'은 정해진 색상만
  | (object_selector access_operator)? SAVE_FILE_KEYWORD assign_operator STRING // '파일로 저장'은 문자열만

// 복합 속성 지정 여러가지의 속성을 한 문장에 할당
complex_assignment_statement: set_axis_labels_statement

// "의" 또는 "." 앞에 오는, 속성을 지정할 대상 객체
object_selector: GRAPH_KEYWORD     // "그래프의 배경색은 ..."
               | X_AXIS_KEYWORD    // "x축의 색은 ..."
               | Y_AXIS_KEYWORD    // "y축의 굵기는 ..."
               | MARKER_KEYWORD    // "마커의 종류는 ..."
               | LINE_KEYWORD      // "선의 스타일은 ..."

// io 관련된 문장
io_statement: load_command 
            | save_command

load_command: LOAD_KEYWORD STRING
save_command: SAVE_KEYWORD

// 데이터 관련 문장
data_statement: DATA_KEYWORD assign_operator vector

// graph_context 를 시작하는 문장
create_graph_statement: CREATE_GRAPH_KEYWORD STRING 

// 그래프를 그리는 문장
draw_statement: DRAW_KEYWORD


// ======================================================================
// Complex Property Assignment Statement (여러 속성을 한번에 정의 가능한 복합 문장)
// ======================================================================

set_axis_labels_statement: SET_LABELS_KEYWORD assign_operator STRING STRING

// ======================================================================
// Core Components for Property Assignment (속성 할당 핵심 요소)
// ======================================================================

// 속성을 할당해주는 연산자.
assign_operator: "은" | "는" | "=" | "<-"

// 어느 객체의 속성에 접근할 것인지 지정해주는 연산자.
access_operator: "의" | "."

// ======================================================================
// Terminals: Keywords (터미널: 키워드)
// ======================================================================

// --- Command Keywords (명령 키워드) ---
CREATE_GRAPH_KEYWORD: "그래프생성"
LOAD_KEYWORD: "로드" | "불러오기" | "가져오기" | "load" | "ld" | "open"
SAVE_KEYWORD: "세이브" | "저장하기" | "저장" | "save" | "sv"
DATA_KEYWORD: "데이터"
DRAW_KEYWORD: "그리기" | "draw" | "그려줘"

// --- Selector Keywords (선택자 키워드) ---
MARKER_KEYWORD: "마커" 
LINE_KEYWORD: "선"
GRAPH_KEYWORD: "그래프" // 굳이 안 써도 되지만 명시적으로 하고 싶으면 써도 됨.
X_AXIS_KEYWORD: "x축" | "엑스축" | "xaxis" // X축은 "엑스축"
Y_AXIS_KEYWORD: "y축" | "와이축" | "ylabel" // Y축은 "와이축"

// --- Property Name Keywords (속성 이름 키워드 정의) ---
SET_TYPE_KEYWORD: "종류" | "타입" | "type" | "유형" // 유형은 "막대"
SET_TITLE_KEYWORD: "제목" | "타이틀" | "title" // 제목 "문법 정의파일"
SET_LABEL_KEYWORD: "라벨" | "label"
SET_LABELS_KEYWORD: "축이름" | "labels" // 축이름 "엑스축" "와이축"

SET_LEGEND_KEYWORD: "범례위치" | "범례" | "legend" // 범례는.. "위치"
SET_FONT_KEYWORD: "글꼴" | "폰트" | "font" // 폰트는 "맑은 고딕"
SET_BACKGROUND_KEYWORD: "배경색" | "배경" // "배경은 "초록" "

ALPHA_KEYWORD: "투명도" | "알파" | "alpha"
WIDTH_KEYWORD: "너비"
TICKS_KEYWORD: "눈금"
GRAPH_SIZE_KEYWORD: "그래프 크기"
RESOLUTION_KEYWORD: "해상도"
INNER_BACKGROUND_COLOR_KEYWORD: "내부 배경색"
SAVE_FILE_KEYWORD: "파일로 저장"

// 공통 속성 지정 키워드
SIZE_KEYWORD: "크기" | "size" // 폰트 크기 또는 그래프 크기 등에 사용될 수 있음
SET_COLOR_KEYWORD: "색" | "색상" | "색깔" | "color" | "colour" // 여기저기 색깔이 들어갈 수 있음.
SET_THICKNESS_KEYWORD: "굵기" | "thickness"
SET_NAME_KEYWORD: "이름" 

// ======================================================================
// Property Value Literal Definitions (속성 값 리터럴 정의)
// ======================================================================

// 그래프 종류 값
GRAPH_TYPE_VALUE: LINE_PLOT | BAR_PLOT | SCATTER_PLOT

LINE_PLOT: "선그래프" | "선" | "line" | "line plot"
BAR_PLOT: "막대그래프" | "막대" | "bar" | "bar plot"
SCATTER_PLOT: "산점도그래프" | "산점도" | "scatter" | "scatter plot"

// 마커 문양 값
MARKER_SHAPE_VALUE: CIRCLE_MARKER | SQUARE_MARKER | DOT_MARKER | X_MARKER | UP_TRIANGLE_MARKER | DOWN_TRIANGLE_MARKER | LEFT_TRIANGLE_MARKER | RIGHT_TRIANGLE_MARKER | STAR_MARKER

CIRCLE_MARKER: "원" | "o"
SQUARE_MARKER: "사각형" | "네모" | "s"
DOT_MARKER: "점" | "."
X_MARKER: "엑스" | "x" | "십자가"
UP_TRIANGLE_MARKER: "삼각형" | "세모" | "^" | "삼각형 위" | "위쪽 삼각형"
DOWN_TRIANGLE_MARKER: "삼각형 아래" | "아래쪽 삼각형" | "v" 
LEFT_TRIANGLE_MARKER: "삼각형 왼쪽" | "왼쪽 삼각형" | "<"
RIGHT_TRIANGLE_MARKER: "삼각형 오른쪽" | "오른쪽 삼각형" | ">"
STAR_MARKER: "별" | "*" | "별표"

// 선 스타일 값
LINE_STYLE_VALUE: SOLID_LINE | DOTTED_LINE | DASHED_LINE | DASH_DOT_LINE

SOLID_LINE: "실선" | "-"
DOTTED_LINE: "점선" | ":"
DASHED_LINE: "파선" | "--"
DASH_DOT_LINE: "점선파선" | "-."

// 범례 위치 값
LEGEND_POSITION_VALUE: BEST_POS | UPPER_RIGHT_POS | UPPER_LEFT_POS | LOWER_LEFT_POS | LOWER_RIGHT_POS
     | RIGHT_POS | CENTER_LEFT_POS | CENTER_RIGHT_POS | LOWER_CENTER_POS | UPPER_CENTER_POS | CENTER_POS

BEST_POS: "최적" | "best"
UPPER_RIGHT_POS: "우상단" | "upper right"
UPPER_LEFT_POS: "좌상단" | "upper left"
LOWER_LEFT_POS: "좌하단" | "lower left"
LOWER_RIGHT_POS: "우하단" | "lower right"
RIGHT_POS: "오른쪽" | "right"
CENTER_LEFT_POS: "좌중앙" | "center left"
CENTER_RIGHT_POS: "우중앙" | "center right"
LOWER_CENTER_POS: "하중앙" | "lower center"
UPPER_CENTER_POS: "상중앙" | "upper center"
CENTER_POS: "중앙" | "center"


// ======================================================================
// Data Types (데이터 타입) 기본 자료형
// ======================================================================
value: NUMBER | STRING | vector | BOOLEAN

atom: NUMBER | STRING
element: atom | vector
elements: element ("," element)*

vector : empty_vector | non_empty_vector

empty_vector: "[" "]"
non_empty_vector: "[" elements "]"

STRING: DQ_STRING | SQ_STRING
BOOLEAN: TRUE | FALSE 

TRUE: "true" | "True" | "참"
FALSE: "false" | "False" | "거짓"

// 쌍따옴표 문자열과 따옴표 문자열.
DQ_STRING: /"(\\"|[^"])*?"/
SQ_STRING: /'(\\'|[^'])*?'/

// ======================================================================
// Comments and Whitespace (주석 및 공백 처리)
// ======================================================================

LINE_COMMENT: /\/\/.*/
BLOCK_COMMENT: /\/\*.*?\*\//s
COMMA: ","

%import common.WS
%import common.SIGNED_NUMBER -> NUMBER
%ignore WS

%ignore LINE_COMMENT
%ignore BLOCK_COMMENT
%ignore COMMA
"""
