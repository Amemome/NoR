import copy
from lark import Token, Transformer, Tree, v_args
from error import RunningError
import csv
from graph.graph import graph

class Executor(Transformer):
    def __init__(self, debug_mode=False):
        super().__init__()
        self.graph_name = None # 현재 가리키고 있는 그래프 객체
        self.graph_context = dict()
        self.errors = []
        self.debug_mode = debug_mode # 실행중인 문장을 출력해주는 모드.
        self.g = graph()

    def _debug_print(self, message): # <-- 추가: 디버그 출력 헬퍼 메서드
        if self.debug_mode:
            print(f"[DEBUG - Executor] {message}")

    def _init_graph_data(self, name="제목 없는 그래프"):
        """그래프 데이터 구조를 option 포맷에 맞춰 반환"""
        self._debug_print(f"init 성공: {name}")
        return {
            '이름': name,      # NoR 스크립트에서 '그래프생성 "이름"' 으로 받은 이름
            '종류': None,      # 예: '선그래프'
            'x': [],
            'y': [],
            '옵션': {
                '제목': name, 
                'label': None, 
                '글꼴': None, 
                '범례위치': None,
                'marker': {'문양': None, '색': None, '크기': None, '투명도': None},
                'line': {'종류': None, '색': None, '굵기': None, '너비': None, '투명도': None},
                'x축': {'이름': None, '라벨': None, '색': None, '글꼴': None, '크기': None, '눈금': None},
                'y축': {'이름': None, '라벨': None, '색': None, '글꼴': None, '크기': None, '눈금': None},
                '출력': {
                    '배경색': None, '파일로 저장': None, '해상도': None, 
                    '그래프 크기': None, '투명도': None, '내부 배경색': None
                }
            }
        }
    def _get_current_graph_data_dict(self):
        """현재 그래프 컨텍스트에 있는 데이터들 반환"""
        if self.graph_name and self.graph_name in self.graph_context:
            return self.graph_context[self.graph_name]
        return None

    def _add_error(self, token_or_meta, message="메세지가 없습니다"):
        line, column = '?', '?'
        if isinstance(token_or_meta, Token):
            line, column = token_or_meta.line, token_or_meta.column
        elif hasattr(token_or_meta, 'line') and hasattr(token_or_meta, 'column'): # meta 객체
            line, column = token_or_meta.line, token_or_meta.column

        err = RunningError(line, column, message)
        self.errors.append(err)
        self._debug_print(f"런타임 오류 추가: {err}")
    # atom
    @v_args(inline=True)
    def atom(self, value): 
        return value 
    
    # 기본 타입 inlining
    @v_args(inline=True)
    def STRING(self, value):
        return value.value.strip("'\"")
    @v_args(inline=True)
    def NUMBER(self, value):
        return float(value.value)
    @v_args(inline=True)
    def TRUE(self, token):
        return True
    @v_args(inline=True)
    def FALSE(self, token):
        return False
    # 그래프 타입 에 들어갈 수 있는 값들 정형화
    @v_args(inline=True)
    def GRAPH_TYPE_VALUE(self, value):
        return value.value
        
    @v_args(inline=True)
    def LINE_PLOT(self, value):
        return "선그래프"
    @v_args(inline=True)
    def BAR_PLOT(self, value):
        return "막대그래프"
    @v_args(inline=True)
    def SCATTER_PLOT(self, value):
        return "산점도그래프"
    
    # 색깔 정형화
    @v_args(inline=True)
    def BLACK_COLOR(self, token): 
        self._debug_print(f"BLACK_COLOR 메소드 호출됨. token.value: '{token.value}'") 
        return "black"
    @v_args(inline=True)
    def BLUE_COLOR(self, token): return "blue"
    @v_args(inline=True)
    def BROWN_COLOR(self, token): return "brown"
    @v_args(inline=True)
    def GRAY_COLOR(self, token): return "gray"
    @v_args(inline=True)
    def GREEN_COLOR(self, token): return "green"
    @v_args(inline=True)
    def ORANGE_COLOR(self, token): return "orange"
    @v_args(inline=True)
    def PINK_COLOR(self, token): return "pink"
    @v_args(inline=True)
    def PURPLE_COLOR(self, token): return "purple"
    @v_args(inline=True)
    def RED_COLOR(self, token): return "red"
    @v_args(inline=True)
    def WHITE_COLOR(self, token): return "white"
    @v_args(inline=True)
    def YELLOW_COLOR(self, token): return "yellow"
    @v_args(inline=True)
    def COLOR_VALUE(self, token):
        # 디버그 메시지를 수정하여 children과 반환될 값을 명확히 확인합니다.
        self._debug_print(f"COLOR_VALUE 메소드 호출됨. children: {token}, 반환될 값: '{token.type}' {token.value}")
        # 이 문자열 값을 반환해야 property_assignment_statement에서 올바르게 사용됩니다.
        return token
    
    # 마커 종류 정형화
    @v_args(inline=True)
    def CIRCLE_MARKER(self, token): return "o"
    @v_args(inline=True)
    def SQUARE_MARKER(self, token): return "s"
    @v_args(inline=True)
    def DOT_MARKER(self, token): return "."
    @v_args(inline=True)
    def X_MARKER(self, token): return "x"
    @v_args(inline=True)
    def UP_TRIANGLE_MARKER(self, token): return "^"
    @v_args(inline=True)
    def DOWN_TRIANGLE_MARKER(self, token): return "v"
    @v_args(inline=True)
    def LEFT_TRIANGLE_MARKER(self, token): return "<"
    @v_args(inline=True)
    def RIGHT_TRIANGLE_MARKER(self, token): return ">"
    @v_args(inline=True)
    def STAR_MARKER(self, token): return "*"

    @v_args(inline=True)
    def MARKER_SHAPE_VALUE(self, value): # value는 이미 "o", "s" 등 문자열
        self._debug_print(f"MARKER_SHAPE_VALUE 규칙: 전달받은 마커 값 '{value}'")
        return value.value
    
    @v_args(inline=True)
    def BEST_POS(self, token): return "best"
    @v_args(inline=True)
    def UPPER_RIGHT_POS(self, token): return "upper right"
    @v_args(inline=True)
    def UPPER_LEFT_POS(self, token): return "upper left"
    @v_args(inline=True)
    def LOWER_LEFT_POS(self, token): return "lower left"
    @v_args(inline=True)
    def LOWER_RIGHT_POS(self, token): return "lower right"
    @v_args(inline=True)
    def RIGHT_POS(self, token): return "right"
    @v_args(inline=True)
    def CENTER_LEFT_POS(self, token): return "center left"
    @v_args(inline=True)
    def CENTER_RIGHT_POS(self, token): return "center right"
    @v_args(inline=True)
    def LOWER_CENTER_POS(self, token): return "lower center"
    @v_args(inline=True)
    def UPPER_CENTER_POS(self, token): return "upper center"
    @v_args(inline=True)
    def CENTER_POS(self, token): return "center"

    # LEGEND_POSITION_VALUE는 위 터미널들이 반환한 문자열을 받음
    @v_args(inline=True)
    def LEGEND_POSITION_VALUE(self, position_string): # position_string은 "best", "upper right" 등
        self._debug_print(f"LEGEND_POSITION_VALUE: 받은 값 '{position_string}' (타입: {type(position_string)})")
        return position_string
    
    @v_args(inline=True)
    def LEGEND_POSITION_VALUE(self, position_string): # position_string은 "best", "upper right" 등
        self._debug_print(f"LEGEND_POSITION_VALUE: 받은 값 '{position_string}' (타입: {type(position_string)})")
        return position_string

    # --- 선 스타일 값 처리 (만약 필요하다면) ---
    @v_args(inline=True)
    def SOLID_LINE(self, token): return "-"
    @v_args(inline=True)
    def DOTTED_LINE(self, token): return ":"
    @v_args(inline=True)
    def DASHED_LINE(self, token): return "--"
    @v_args(inline=True)
    def DASH_DOT_LINE(self, token): return "-."

    @v_args(inline=True)
    def LINE_STYLE_VALUE(self, style_string): # style_string은 "-", ":" 등
        self._debug_print(f"LINE_STYLE_VALUE: 받은 값 '{style_string}' (타입: {type(style_string)})")
        return style_string

    def vector(self, items):
        return items[0]
    
    def empty_vector(self, items):
        return []
    
    def non_empty_vector(self, items):
        return items[0]
    
    def elements(self, items):
        return list(items)
    
    def element(self, items):
        return items[0]
    
    # 문장 처리
    def start(self, items):
        self._debug_print("스크립트 실행 시작.")

        if self.errors:
            self._debug_print(f"실행 중 {len(self.errors)}개의 오류 발생.")
        else:
            self._debug_print("스크립트 실행 완료. 오류 없음.")
        return self.graph_context # 최종적으로 생성된 그래프 컨텍스트를 반환할 수 있음

    def statement(self, items):
        return None
    
    def object_selector(self, items):
        token = items[0]
        self._debug_print(f"객체 선택: {token.type} ('{token.value}')")
        return token 
    
    # -- 주요 문장 처리 메서드들 --
    @v_args(meta=True)
    def create_graph_statement(self, meta, items):
        graph_name_token = items[0] 
        graph_name_value = items[1] 
        self._debug_print(f"명령 실행: 그래프생성 \"{graph_name_value}\" (라인: {meta.line})")

        if graph_name_value in self.graph_context:
            self._add_error(meta, f"그래프 이름 '{graph_name_value}'은(는) 이미 사용 중입니다. 다른 이름을 지정해주세요.")
            return

        self.graph_context[graph_name_value] = self._init_graph_data(graph_name_value)
        self.graph_name = graph_name_value
        self._debug_print(f"현재 작업 그래프: '{self.graph_name}'")

    @v_args(meta=True)
    def data_statement(self, meta, items):
        # 데이터 할당문. 종류가 선택된 이후에 실행되어야 한다.
        data_keyword_token = items[0]
        current_graph_data = self._get_current_graph_data_dict()
        
        if not current_graph_data:
            self._add_error(data_keyword_token, "'데이터'를 할당할 그래프가 없습니다. '그래프생성' 명령을 먼저 사용하세요.")
            return
        
        if not current_graph_data.get('종류'):
            self._add_error(data_keyword_token, f"그래프 '{self.graph_name}'의 '종류'가 정의되지 않아 '데이터'를 할당할 수 없습니다. '종류는 ...' 명령을 먼저 사용하세요.")
            return
        
        data_list = items[2]
        self._debug_print(f"명령 실행: 데이터 할당 for '{self.graph_name}', 데이터: {data_list}")

        current_graph_data['x'] = data_list[0]
        current_graph_data['y'] = data_list[1]

    
    @v_args(meta=True)
    def property_assignment_statement(self, meta, items): 
        """
        이 메소드는 문법의 모든 property_assignment_statement 대안 규칙을 처리해야 함.
        items 리스트의 구조는 매치된 특정 대안 규칙에 따라 달라짐.
        예:
        1. (object_selector access_operator)? SET_TITLE_KEYWORD assign_operator STRING
           - items: [Token(SET_TITLE_KEYWORD), Token(ASSIGN_OPERATOR), "실제문자열"] (object_selector 없는 경우)
           - items: [obj_sel_token, Token(ACCESS_OPERATOR), Token(SET_TITLE_KEYWORD), Token(ASSIGN_OPERATOR), "실제문자열"] (object_selector 있는 경우)
        2. LINE_KEYWORD access_operator SET_TYPE_KEYWORD assign_operator LINE_STYLE_VALUE
           - items: [Token(LINE_KEYWORD), Token(ACCESS_OPERATOR), Token(SET_TYPE_KEYWORD), Token(ASSIGN_OPERATOR), "실제선스타일문자열"]"""
        
        self._debug_print(f"명령 실행: 속성 할당 (라인: {meta.line}), children: {[type(c) for c in items]} values: {items}")

        current_graph_data = self._get_current_graph_data_dict()

        if not current_graph_data:
            err_token = items[0] if items and isinstance(items[0], Token) else meta
            self._add_error(err_token, "속성을 할당할 그래프가 없습니다. '그래프생성' 명령을 먼저 사용하세요.")
            return
        
        # --- children 분석하여 객체, 속성 키, 값 추출 ---
        obj_selector_token = None 
        prop_key_token = None     
        assigned_value = None     

        # 첫 번째 요소가 object_selector의 결과(Token)인지    
        # object_selector 메소드가 Token을 반환하도록 했으므로 타입체크.
    
        first_child = items[0]

        # Case 1: "객체 의 속성 은 값" 또는 특정 객체 전용 규칙 (LINE_KEYWORD ... SET_TYPE_KEYWORD ...)
        if isinstance(first_child, Token) and first_child.type in ["LINE_KEYWORD", "MARKER_KEYWORD", "GRAPH_KEYWORD", "X_AXIS_KEYWORD", "Y_AXIS_KEYWORD"]:
            obj_selector_token = first_child # object_selector의 결과 또는 규칙의 시작 토큰
            if len(items) >= 5:
                prop_key_token = items[2]
                assigned_value = items[4]
            else: 
                self._add_error(meta, f"'{first_child.value} ...' 구문이 완전하지 않습니다.")
                return

        elif isinstance(first_child, Token): # 속성 키워드로 시작
            prop_key_token = first_child
            if len(items) >= 3:
                assigned_value = items[2]
            else: # 문법 매칭 오류 가능성
                self._add_error(meta, f"'{first_child.value} ...' 구문이 완전하지 않습니다.")
                return
        else: # 예기치 않은 children 구조
            self._add_error(meta, "속성 할당문의 구조를 이해할 수 없습니다.")
            return
        
        if not prop_key_token or assigned_value is None:
            self._add_error(meta, f"속성 할당 분석 실패: 키 또는 값 누락 (키 토큰: {prop_key_token}, 값: {assigned_value})")
            return
        
        prop_key_name_script = prop_key_token.value # 스크립트 상의 한글 속성 이름
        prop_key_type_lark = prop_key_token.type   # Lark 터미널 타입 (예: SET_TITLE_KEYWORD)

        target_object_dict = None # 값을 저장할 딕셔너리 부분 (예: current_graph_data['옵션']['marker'])
        target_key_in_dict = None   # 딕셔너리 내 실제 키 이름 (예: '종류', '색')

        obj_type_for_msg = "그래프" # 오류 메시지용

        # 객체 선택자(obj_selector_token) 유무 및 타입에 따라 target_object_dict 설정
        if obj_selector_token:
            obj_type_lark = obj_selector_token.type
            obj_type_for_msg = obj_selector_token.value # "마커", "선", "x축", "y축", "그래프"

            if obj_type_lark == "GRAPH_KEYWORD":
                # '그래프 의 종류 는 ...' 또는 '그래프 의 제목 은 ...'
                # 이 경우는 obj_selector_token이 없는 경우와 유사하게 처리 (아래에서 통합)
                pass 
            elif obj_type_lark == "MARKER_KEYWORD":
                target_object_dict = current_graph_data['옵션']['marker']
                if prop_key_type_lark == "SET_TYPE_KEYWORD": target_key_in_dict = "문양"
                elif prop_key_type_lark == "SET_COLOR_KEYWORD": target_key_in_dict = "색"
                elif prop_key_type_lark == "SIZE_KEYWORD": target_key_in_dict = "크기"
                elif prop_key_type_lark == "ALPHA_KEYWORD": target_key_in_dict = "투명도"
                else: target_key_in_dict = prop_key_name_script # 정의되지 않은 다른 속성 대비
            elif obj_type_lark == "LINE_KEYWORD":
                target_object_dict = current_graph_data['옵션']['line']
                if prop_key_type_lark == "SET_TYPE_KEYWORD": target_key_in_dict = "종류"
                elif prop_key_type_lark == "SET_COLOR_KEYWORD": target_key_in_dict = "색"
                elif prop_key_type_lark in ["SET_THICKNESS_KEYWORD", "WIDTH_KEYWORD"]: target_key_in_dict = "굵기"
                elif prop_key_type_lark == "ALPHA_KEYWORD": target_key_in_dict = "투명도"
                else: target_key_in_dict = prop_key_name_script
            elif obj_type_lark == "X_AXIS_KEYWORD":
                target_object_dict = current_graph_data['옵션']['x축']
                target_key_in_dict = prop_key_name_script # '이름', '라벨', '색', '글꼴', '크기', '눈금' 등
            elif obj_type_lark == "Y_AXIS_KEYWORD":
                target_object_dict = current_graph_data['옵션']['y축']
                target_key_in_dict = prop_key_name_script # '이름', '라벨', '색', '글꼴', '크기', '눈금' 등
            else:
                self._add_error(obj_selector_token, f"내부 오류: 알 수 없는 객체 선택자 타입 '{obj_type_lark}'")
                return

# 객체 선택자가 없거나 GRAPH_KEYWORD인 경우 (그래프 전반 옵션)
        if obj_selector_token is None or (obj_selector_token and obj_selector_token.type == "GRAPH_KEYWORD"):
            if obj_selector_token and obj_selector_token.type == "GRAPH_KEYWORD":
                obj_type_for_msg = obj_selector_token.value # "그래프"
            else: # obj_selector_token is None
                obj_type_for_msg = "그래프 (기본객체)"

            # 최상위 '종류' 속성 (예: '종류는 선그래프')
            if prop_key_type_lark == "SET_TYPE_KEYWORD":
                current_graph_data['종류'] = assigned_value
                self._debug_print(f"그래프 '{current_graph_data['이름']}'의 '종류'를 '{assigned_value}'로 설정.")
                return # 처리가 완료되었으므로 반환

            # 속성 키 타입에 따라 target_object_dict와 target_key_in_dict 결정
            # 1. '옵션'.'출력' 하위 속성
            if prop_key_type_lark == "SET_BACKGROUND_KEYWORD":
                target_object_dict, target_key_in_dict = current_graph_data['옵션']['출력'], "배경색"
            elif prop_key_type_lark == "INNER_BACKGROUND_COLOR_KEYWORD":
                target_object_dict, target_key_in_dict = current_graph_data['옵션']['출력'], "내부 배경색"
            elif prop_key_type_lark == "SAVE_FILE_KEYWORD":
                target_object_dict, target_key_in_dict = current_graph_data['옵션']['출력'], "파일로 저장"
            elif prop_key_type_lark == "RESOLUTION_KEYWORD":
                target_object_dict, target_key_in_dict = current_graph_data['옵션']['출력'], "해상도"
            elif prop_key_type_lark == "GRAPH_SIZE_KEYWORD":
                target_object_dict, target_key_in_dict = current_graph_data['옵션']['출력'], "그래프 크기"
            elif prop_key_type_lark == "ALPHA_KEYWORD": # 그래프 전체 투명도 (배경 등)
                target_object_dict, target_key_in_dict = current_graph_data['옵션']['출력'], "투명도"
            # 2. '옵션' 직속 하위 속성
            #    (위의 '출력' 관련 키워드에 해당하지 않은 경우)
            elif prop_key_type_lark == "SET_TITLE_KEYWORD":
                target_object_dict, target_key_in_dict = current_graph_data['옵션'], "제목"
            elif prop_key_type_lark == "SET_LABEL_KEYWORD": # "라벨"을 나타내는 토큰의 타입 (실제 타입으로 변경)
                target_object_dict, target_key_in_dict = current_graph_data['옵션'], "label" # 내부 키는 "label"
            elif prop_key_type_lark == "SET_FONT_KEYWORD": # "글꼴"을 나타내는 토큰의 타입
                target_object_dict, target_key_in_dict = current_graph_data['옵션'], "글꼴"
            elif prop_key_type_lark == "SET_LEGEND_KEYWORD": # "범례위치"를 나타내는 토큰의 타입
                target_object_dict, target_key_in_dict = current_graph_data['옵션'], "범례위치"
 
            # else:
            #   # 처리되지 않은 prop_key_type_lark는 오류로 간주 (target_key_in_dict가 None으로 유지됨)
            #   pass

        # 최종 값 할당
        if target_object_dict is not None and target_key_in_dict is not None:
            # target_key_in_dict가 실제로 target_object_dict에 존재하는 키인지 확인 (오타 방지 및 구조 검증)
            if target_key_in_dict in target_object_dict:
                # 값 타입 변환 로직 추가 가능 (예: "크기" -> int, "투명도" -> float)
                # 지금은 문자열 그대로 할당
                target_object_dict[target_key_in_dict] = assigned_value
                self._debug_print(f"'{obj_type_for_msg}'의 '{target_key_in_dict}' 속성을 '{assigned_value}'로 설정.")
            else:
                # 이 오류는 _init_graph_data에 해당 키가 없거나, 위 로직에서 target_key_in_dict가 잘못 설정된 경우 발생 가능
                self._add_error(prop_key_token, f"[내부 오류] '{obj_type_for_msg}' 객체에 '{target_key_in_dict}' 속성이 정의되지 않았습니다 (스크립트 키: '{prop_key_token.value}').")
        elif not (prop_key_type_lark == "SET_TYPE_KEYWORD" and (obj_selector_token is None or (obj_selector_token and obj_selector_token.type == "GRAPH_KEYWORD"))):
            # SET_TYPE_KEYWORD는 위에서 이미 처리하고 return 했으므로, 여기까지 왔다면 다른 문제
            # target_object_dict 또는 target_key_in_dict가 설정되지 못한 경우
             self._add_error(prop_key_token, f"'{obj_type_for_msg}' 객체에 '{prop_key_token.value}' 속성을 설정하는 방법을 알 수 없습니다. 지원되지 않는 속성일 수 있습니다.")


    def draw_statement(self, items):
        draw_keyword_token = items[0]
        current_graph_to_draw = self._get_current_graph_data_dict()

        if not current_graph_to_draw:
            self._add_error(draw_keyword_token, "'그리기' 명령을 실행할 그래프가 없습니다. '그래프생성'을 먼저 사용하세요.")
            return
        if not current_graph_to_draw.get('종류'):
            self._add_error(draw_keyword_token, f"그래프 '{self.graph_name}'의 '종류'가 정의되지 않아 그릴 수 없습니다.")
            return
        if not current_graph_to_draw.get('x') or not current_graph_to_draw.get('y'):
             self._add_error(draw_keyword_token, f"그래프 '{self.graph_name}'의 '데이터'가 정의되지 않아 그릴 수 없습니다.")
             return

        option = remove_none_values_from_dict(copy.deepcopy(current_graph_to_draw))
        self._debug_print(f"그리기 옵션: {option}")
        try:
            self.g.draw(option)
            self._debug_print(f"그래프 '{self.graph_name}' 그리기를 성공적으로 요청했습니다.")
        except Exception as e:
            self._add_error(draw_keyword_token, f"그래프 '{self.graph_name}' 그리기에 실패했습니다: {e}")

    @v_args(meta=True)
    def set_axis_labels_statement(self, items):
        labels_keyword_token = items[0]
        current_graph_data = self._get_current_graph_data_dict()

        if not current_graph_data:
            self._add_error(labels_keyword_token, "'축이름'을 설정할 그래프가 없습니다. '그래프생성'을 먼저 사용하세요.")
            return
        
        # 이 명령은 semantic_analyzer에서 '종류' 정의 후 사용 가능한지 체크하는 것이 좋음
        if not current_graph_data.get('종류'):
             self._add_error(labels_keyword_token, f"그래프 '{self.graph_name}'의 '종류'가 정의되지 않아 '축이름'을 설정할 수 없습니다.")
             return

        x_label_val = items[2]
        y_label_val = items[3]
        current_graph_data['옵션']['x축']['이름'] = x_label_val
        current_graph_data['옵션']['y축']['이름'] = y_label_val
        self._debug_print(f"'{self.graph_name}'의 축 이름 설정: X축='{x_label_val}', Y축='{y_label_val}'")
        
    @v_args(meta=True)
    def save_command(self, items):
        save_keyword_token = items[0]
        filepath = items[1] if len(items) > 1 else None # 파일 경로가 주어졌는지 확인

        current_graph_data = self._get_current_graph_data_dict()
        if not current_graph_data:
            self._add_error(save_keyword_token, "'저장' 명령을 실행할 그래프가 없습니다. '그래프생성'을 먼저 사용하세요.")
            return
        
        if not current_graph_data.get('종류'):
            self._add_error(save_keyword_token, f"그래프 '{self.graph_name}'의 '종류'가 정의되지 않아 저장할 수 없습니다.")
            return
        
        
        option = remove_none_values_from_dict(copy.deepcopy(current_graph_data))
        # '파일로 저장' 옵션 업데이트: 명령에서 파일 경로가 주어지면 그것을 사용, 아니면 기존값 유지
        if filepath:
            option['옵션']['출력']['파일로 저장'] = filepath
        elif not option['옵션']['출력'].get('파일로 저장'): # 명령에도 없고, 기존 옵션에도 없으면 기본값 설정 또는 오류
            default_filename = f"{option.get('이름', '그래프')}.png" # 기본 파일 이름
            option['옵션']['출력']['파일로 저장'] = default_filename
            self._debug_print(f"저장 파일 경로가 지정되지 않아 기본값 '{default_filename}'으로 설정합니다.")
            # self._add_error(save_keyword_token, "저장할 파일 이름/경로가 지정되지 않았습니다. (예: 저장 \"내그래프.png\")")
            # return

        self._debug_print(f"저장 옵션: {option}")
        try:
            self.g.save(option)
            self._debug_print(f"그래프 '{self.graph_name}'을(를) '{option['옵션']['출력']['파일로 저장']}' 경로에 성공적으로 저장 요청했습니다.")
        except Exception as e:
            self._add_error(save_keyword_token, f"그래프 '{self.graph_name}' 저장에 실패했습니다: {e}")



def remove_none_values_from_dict(data):
    """
    딕셔너리 (및 중첩된 딕셔너리/리스트 안의 딕셔너리)에서
    값이 None인 키-값 쌍을 재귀적으로 제거합니다.
    원본 딕셔너리는 변경하지 않고 복사본을 사용합니다.
    """
    if isinstance(data, dict):
        # 새 딕셔너리를 만들어 None이 아닌 값만 추가
        # 이렇게 하면 반복 중 딕셔너리 크기 변경 문제를 피할 수 있음
        cleaned_dict = {}
        for k, v in data.items():
            cleaned_value = remove_none_values_from_dict(v) # 재귀 호출
            if cleaned_value is not None: # 여기서도 None 체크
                cleaned_dict[k] = cleaned_value
        # 만약 딕셔너리가 비어있다면, 상황에 따라 None을 반환하거나 빈 딕셔너리 그대로 반환
        # 여기서는 비어있더라도 구조 유지를 위해 빈 딕셔너리 반환
        return cleaned_dict
    elif isinstance(data, list):
        cleaned_list = []
        for item in data:
            cleaned_item = remove_none_values_from_dict(item) # 재귀 호출
            if cleaned_item is not None: # 리스트의 요소가 None이 된 경우 (예: 딕셔너리가 통째로 None이 됨)
                                        # 여기서는 None 요소도 일단 유지하거나, 필요시 제거
                cleaned_list.append(cleaned_item)
        return cleaned_list
    else:
        # 딕셔너리나 리스트가 아닌 다른 타입은 그대로 반환
        return data