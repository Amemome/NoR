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
        self._add_error("그래프가 컨텍스트에 없습니다")
        return None

    def _add_error(self, token=None, message="메세지가 없습니다"):
        line = '?'
        column = '?'
        if isinstance(token, Token):
            line = token.line
            column = token.column
        elif hasattr(token, 'line') and hasattr(token, 'column'): # meta 객체인 경우
            line = token.line
            column = token.column

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
            self._add_error(meta, f"그래프 이름 '{graph_name_value}'이(가) 이미 사용 중입니다. 다른 이름을 사용해주세요.")
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
            self._add_error(message="현재 작업중인 그래프가 없습니다")
            return
        
        if not current_graph_data.get('종류'):
            self._add_error(data_keyword_token, f"그래프 '{self.graph_name}'의 '종류'가 정의되지 않아 데이터를 할당할 수 없습니다.")
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
            error_token_location = items[0] if items else meta
            self._add_error(error_token_location, "속성을 할당할 현재 작업 그래프가 없습니다. '그래프생성'을 먼저 실행하세요.")
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

        if obj_selector_token: # 객체 선택자가 명시된 경우
            obj_type_lark = obj_selector_token.type
            obj_type_for_msg = obj_selector_token.value # "마커", "x축" 등

            if obj_type_lark == "GRAPH_KEYWORD":
                target_object_dict = current_graph_data['옵션'] # 기본
                if prop_key_type_lark == "SET_TYPE_KEYWORD":
                    current_graph_data['종류'] = assigned_value
                    self._debug_print(f"그래프 '{self.graph_name}'의 '종류'를 '{assigned_value}'로 설정.")
                    return
                elif prop_key_type_lark == "SET_BACKGROUND_KEYWORD": target_object_dict, target_key_in_dict = current_graph_data['옵션']['출력'], "배경색"
                elif prop_key_type_lark == "INNER_BACKGROUND_COLOR_KEYWORD": target_object_dict, target_key_in_dict = current_graph_data['옵션']['출력'], "내부 배경색"
                elif prop_key_type_lark == "SAVE_FILE_KEYWORD": target_object_dict, target_key_in_dict = current_graph_data['옵션']['출력'], "파일로 저장"
                elif prop_key_type_lark == "RESOLUTION_KEYWORD": target_object_dict, target_key_in_dict = current_graph_data['옵션']['출력'], "해상도"
                elif prop_key_type_lark == "GRAPH_SIZE_KEYWORD": target_object_dict, target_key_in_dict = current_graph_data['옵션']['출력'], "그래프 크기"
                elif prop_key_type_lark == "ALPHA_KEYWORD": target_object_dict, target_key_in_dict = current_graph_data['옵션']['출력'], "투명도"
                else: target_key_in_dict = prop_key_name_script # 옵션 바로 밑 (제목, 글꼴, 범례위치)
            
            elif obj_type_lark == "MARKER_KEYWORD":
                target_object_dict = current_graph_data['옵션']['marker']
                if prop_key_type_lark == "SET_TYPE_KEYWORD": target_key_in_dict = "문양"
                elif prop_key_type_lark == "SET_COLOR_KEYWORD": target_key_in_dict = "색"
                elif prop_key_type_lark == "SIZE_KEYWORD": target_key_in_dict = "크기"
                elif prop_key_type_lark == "ALPHA_KEYWORD": target_key_in_dict = "투명도"
                else: target_key_in_dict = prop_key_name_script # 혹시 모를 다른 속성
            
            elif obj_type_lark == "LINE_KEYWORD":
                target_object_dict = current_graph_data['옵션']['line']
                if prop_key_type_lark == "SET_TYPE_KEYWORD": target_key_in_dict = "종류"
                elif prop_key_type_lark == "SET_COLOR_KEYWORD": target_key_in_dict = "색"
                elif prop_key_type_lark in ["SET_THICKNESS_KEYWORD", "WIDTH_KEYWORD"]: target_key_in_dict = "굵기" # 너비도 굵기로 통일
                elif prop_key_type_lark == "ALPHA_KEYWORD": target_key_in_dict = "투명도"
                else: target_key_in_dict = prop_key_name_script
            
            elif obj_type_lark == "X_AXIS_KEYWORD":
                target_object_dict = current_graph_data['옵션']['x축']
                # 이름, 라벨, 색, 글꼴, 크기, 눈금 등은 스크립트 이름과 내부 키 동일 가정
                target_key_in_dict = prop_key_name_script
            
            elif obj_type_lark == "Y_AXIS_KEYWORD":
                target_object_dict = current_graph_data['옵션']['y축']
                target_key_in_dict = prop_key_name_script
            
            else: # 처리되지 않은 객체 타입
                self._add_error(obj_selector_token, f"내부 오류: 알 수 없는 객체 선택자 타입 '{obj_type_lark}'")
                return
        
        else: # 객체 선택자 없이 바로 속성 지정 (예: 제목은 "값", 종류는 선그래프)
            obj_type_for_msg = "그래프 (기본객체)"
            target_object_dict = current_graph_data['옵션'] # 기본은 옵션 바로 아래
            
            if prop_key_type_lark == "SET_TYPE_KEYWORD":
                current_graph_data['종류'] = assigned_value
                self._debug_print(f"그래프 '{self.graph_name}'의 '종류'를 '{assigned_value}'로 설정.")
                return
            elif prop_key_type_lark == "SET_BACKGROUND_KEYWORD": target_object_dict, target_key_in_dict = current_graph_data['옵션']['출력'], "배경색"
            elif prop_key_type_lark == "INNER_BACKGROUND_COLOR_KEYWORD": target_object_dict, target_key_in_dict = current_graph_data['옵션']['출력'], "내부 배경색"
            elif prop_key_type_lark == "SAVE_FILE_KEYWORD": target_object_dict, target_key_in_dict = current_graph_data['옵션']['출력'], "파일로 저장"
            elif prop_key_type_lark == "RESOLUTION_KEYWORD": target_object_dict, target_key_in_dict = current_graph_data['옵션']['출력'], "해상도"
            elif prop_key_type_lark == "GRAPH_SIZE_KEYWORD": target_object_dict, target_key_in_dict = current_graph_data['옵션']['출력'], "그래프 크기"
            elif prop_key_type_lark == "ALPHA_KEYWORD": target_object_dict, target_key_in_dict = current_graph_data['옵션']['출력'], "투명도"
            else: # 제목, 글꼴, 범례위치 등은 옵션 바로 아래
                target_key_in_dict = prop_key_name_script 

        # 최종 값 할당
        if target_object_dict is not None and target_key_in_dict is not None:
            if target_key_in_dict in target_object_dict:
                target_object_dict[target_key_in_dict] = assigned_value
                self._debug_print(f"'{obj_type_for_msg}'의 '{target_key_in_dict}' 속성을 '{assigned_value}'로 설정.")
            else:
                # 이 오류는 SemanticAnalyzer에서 VALIDATION_RULES로 잡히거나, _init_graph_data에 해당 키가 없다면 발생
                self._add_error(prop_key_token, f"'{obj_type_for_msg}' 객체에 '{target_key_in_dict}' 속성은 내부적으로 정의되지 않았습니다.")
        else:
            self._add_error(prop_key_token, f"속성 '{prop_key_name_script}'을(를) '{obj_type_for_msg}' 객체에 설정하는 로직을 찾을 수 없습니다.")


    def draw_statement(self, items):
        current_graph_to_draw = self._get_current_graph_data_dict()
        option = remove_none_values_from_dict(current_graph_to_draw)
        print(option)
        if option:
            self.g.draw(option)
            pass
        else:
            self._add_error("그래프 그릴 수 없는 상황")

    def set_axis_labels_statement(self, items):
        set_labels_token = items[0]
        current_graph_data = self._get_current_graph_data_dict()
        if not current_graph_data:
            self._add_error(set_labels_token, "축 이름 설정 전 그래프가 먼저 생성되어야 합니다.")
            return
        x_label_val = items[2]
        y_label_val = items[3]
        current_graph_data['옵션']['x축']['이름'] = x_label_val
        current_graph_data['옵션']['y축']['이름'] = y_label_val
        
    # def load_command(self, items):
    #     load_token = items[0]
    #     filepath = items[1]

    #     current_graph_to_draw = self._get_current_graph_data_dict()
    #     if not current_graph_to_draw:
    #         self._add_error(load_token, "현재 작업 그래프를 찾을 수 없습니다.")
    #         return  
        
    #     csv_data = ""
    #     x_data = []
    #     y_data = []
    #     header = None
    #     has_header = None
    #     encoding = 'utf-8'

    #     try:
    #         with open(filepath, mode='r', encoding=encoding, newline='') as file:
    #             csv_reader = csv.reader(file)
    #             if has_header:
    #                 try:
    #                     header = next(csv_reader)
    #                 except StopIteration:
    #                     pass
                
    #             for row in csv_reader:
    #                 processed_row = []
    #                 for item in row:
    #                     processed_row.append(float(item))
                    
    #                 data.append(processed_row)

    #     except FileNotFoundError:
    #         print(f"오류: 파일 '{filepath}'를 찾을 수 없습니다.")
    #         raise
    #     except UnicodeDecodeError:
    #         print(f"오류: '{filepath}' 파일을 '{encoding}'으로 읽는 중 에러 발생. 인코딩을 확인하세요 (예: cp949).")
    #         raise
    #     except Exception as e:
    #         print(f"오류: CSV 파일 처리 중 예외 발생 - {e}")
    #         raise

    #     print("읽기 시작")
    #     pass

    def save_command(self, items):
        """그래프 저장하는 함수 호출"""
        pass

    def object_selector(self, items):
        return items[0].type

    def property_key(self, items):
        return items[0]
    
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
            error_token_location = items[0] if items else meta
            self._add_error(error_token_location, "속성을 할당할 현재 작업 그래프가 없습니다. '그래프생성'을 먼저 실행하세요.")
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

        if obj_selector_token: # 객체 선택자가 명시된 경우
            obj_type_lark = obj_selector_token.type
            obj_type_for_msg = obj_selector_token.value # "마커", "x축" 등

            if obj_type_lark == "GRAPH_KEYWORD":
                target_object_dict = current_graph_data['옵션'] # 기본
                if prop_key_type_lark == "SET_TYPE_KEYWORD":
                    current_graph_data['종류'] = assigned_value
                    self._debug_print(f"그래프 '{self.graph_name}'의 '종류'를 '{assigned_value}'로 설정.")
                    return
                elif prop_key_type_lark == "SET_BACKGROUND_KEYWORD": target_object_dict, target_key_in_dict = current_graph_data['옵션']['출력'], "배경색"
                elif prop_key_type_lark == "INNER_BACKGROUND_COLOR_KEYWORD": target_object_dict, target_key_in_dict = current_graph_data['옵션']['출력'], "내부 배경색"
                elif prop_key_type_lark == "SAVE_FILE_KEYWORD": target_object_dict, target_key_in_dict = current_graph_data['옵션']['출력'], "파일로 저장"
                elif prop_key_type_lark == "RESOLUTION_KEYWORD": target_object_dict, target_key_in_dict = current_graph_data['옵션']['출력'], "해상도"
                elif prop_key_type_lark == "GRAPH_SIZE_KEYWORD": target_object_dict, target_key_in_dict = current_graph_data['옵션']['출력'], "그래프 크기"
                elif prop_key_type_lark == "ALPHA_KEYWORD": target_object_dict, target_key_in_dict = current_graph_data['옵션']['출력'], "투명도"
                else: target_key_in_dict = prop_key_name_script # 옵션 바로 밑 (제목, 글꼴, 범례위치)
            
            elif obj_type_lark == "MARKER_KEYWORD":
                target_object_dict = current_graph_data['옵션']['marker']
                if prop_key_type_lark == "SET_TYPE_KEYWORD": target_key_in_dict = "종류"
                elif prop_key_type_lark == "SET_COLOR_KEYWORD": target_key_in_dict = "색"
                elif prop_key_type_lark == "SIZE_KEYWORD": target_key_in_dict = "크기"
                elif prop_key_type_lark == "ALPHA_KEYWORD": target_key_in_dict = "투명도"
                else: target_key_in_dict = prop_key_name_script # 혹시 모를 다른 속성
            
            elif obj_type_lark == "LINE_KEYWORD":
                target_object_dict = current_graph_data['옵션']['line']
                if prop_key_type_lark == "SET_TYPE_KEYWORD": target_key_in_dict = "종류"
                elif prop_key_type_lark == "SET_COLOR_KEYWORD": target_key_in_dict = "색"
                elif prop_key_type_lark in ["SET_THICKNESS_KEYWORD", "WIDTH_KEYWORD"]: target_key_in_dict = "굵기" # 너비도 굵기로 통일
                elif prop_key_type_lark == "ALPHA_KEYWORD": target_key_in_dict = "투명도"
                else: target_key_in_dict = prop_key_name_script
            
            elif obj_type_lark == "X_AXIS_KEYWORD":
                target_object_dict = current_graph_data['옵션']['x축']
                # 이름, 라벨, 색, 글꼴, 크기, 눈금 등은 스크립트 이름과 내부 키 동일 가정
                target_key_in_dict = prop_key_name_script
            
            elif obj_type_lark == "Y_AXIS_KEYWORD":
                target_object_dict = current_graph_data['옵션']['y축']
                target_key_in_dict = prop_key_name_script
            
            else: # 처리되지 않은 객체 타입
                self._add_error(obj_selector_token, f"내부 오류: 알 수 없는 객체 선택자 타입 '{obj_type_lark}'")
                return
        
        else: # 객체 선택자 없이 바로 속성 지정 (예: 제목은 "값", 종류는 선그래프)
            obj_type_for_msg = "그래프 (기본객체)"
            target_object_dict = current_graph_data['옵션'] # 기본은 옵션 바로 아래
            
            if prop_key_type_lark == "SET_TYPE_KEYWORD":
                current_graph_data['종류'] = assigned_value
                self._debug_print(f"그래프 '{self.graph_name}'의 '종류'를 '{assigned_value}'로 설정.")
                return
            elif prop_key_type_lark == "SET_BACKGROUND_KEYWORD": target_object_dict, target_key_in_dict = current_graph_data['옵션']['출력'], "배경색"
            elif prop_key_type_lark == "INNER_BACKGROUND_COLOR_KEYWORD": target_object_dict, target_key_in_dict = current_graph_data['옵션']['출력'], "내부 배경색"
            elif prop_key_type_lark == "SAVE_FILE_KEYWORD": target_object_dict, target_key_in_dict = current_graph_data['옵션']['출력'], "파일로 저장"
            elif prop_key_type_lark == "RESOLUTION_KEYWORD": target_object_dict, target_key_in_dict = current_graph_data['옵션']['출력'], "해상도"
            elif prop_key_type_lark == "GRAPH_SIZE_KEYWORD": target_object_dict, target_key_in_dict = current_graph_data['옵션']['출력'], "그래프 크기"
            elif prop_key_type_lark == "ALPHA_KEYWORD": target_object_dict, target_key_in_dict = current_graph_data['옵션']['출력'], "투명도"
            else: # 제목, 글꼴, 범례위치 등은 옵션 바로 아래
                target_key_in_dict = prop_key_name_script 

        # 최종 값 할당
        if target_object_dict is not None and target_key_in_dict is not None:
            if target_key_in_dict in target_object_dict:
                target_object_dict[target_key_in_dict] = assigned_value
                self._debug_print(f"'{obj_type_for_msg}'의 '{target_key_in_dict}' 속성을 '{assigned_value}'로 설정.")
            else:
                # 이 오류는 SemanticAnalyzer에서 VALIDATION_RULES로 잡히거나, _init_graph_data에 해당 키가 없다면 발생
                self._add_error(prop_key_token, f"'{obj_type_for_msg}' 객체에 '{target_key_in_dict}' 속성은 내부적으로 정의되지 않았습니다.")
        else:
            self._add_error(prop_key_token, f"속성 '{prop_key_name_script}'을(를) '{obj_type_for_msg}' 객체에 설정하는 로직을 찾을 수 없습니다.")


    def draw_statement(self, items):
        current_graph_to_draw = self._get_current_graph_data_dict()
        print(current_graph_to_draw)

        if current_graph_to_draw:
            # 실제 함수 호출
            pass
        else:
            self._add_error("그래프 그릴 수 없는 상황")

    def set_axis_labels_statement(self, items):
        set_labels_token = items[0]
        current_graph_data = self._get_current_graph_data_dict()
        if not current_graph_data:
            self._add_error(set_labels_token, "축 이름 설정 전 그래프가 먼저 생성되어야 합니다.")
            return
        x_label_val = items[2]
        y_label_val = items[3]
        current_graph_data['옵션']['x축']['이름'] = x_label_val
        current_graph_data['옵션']['y축']['이름'] = y_label_val
        
    # def load_command(self, items):
    #     load_token = items[0]
    #     filepath = items[1]

    #     current_graph_to_draw = self._get_current_graph_data_dict()
    #     if not current_graph_to_draw:
    #         self._add_error(load_token, "현재 작업 그래프를 찾을 수 없습니다.")
    #         return  
        
    #     csv_data = ""
    #     x_data = []
    #     y_data = []
    #     header = None
    #     has_header = None
    #     encoding = 'utf-8'

    #     try:
    #         with open(filepath, mode='r', encoding=encoding, newline='') as file:
    #             csv_reader = csv.reader(file)
    #             if has_header:
    #                 try:
    #                     header = next(csv_reader)
    #                 except StopIteration:
    #                     pass
                
    #             for row in csv_reader:
    #                 processed_row = []
    #                 for item in row:
    #                     processed_row.append(float(item))
                    
    #                 data.append(processed_row)

    #     except FileNotFoundError:
    #         print(f"오류: 파일 '{filepath}'를 찾을 수 없습니다.")
    #         raise
    #     except UnicodeDecodeError:
    #         print(f"오류: '{filepath}' 파일을 '{encoding}'으로 읽는 중 에러 발생. 인코딩을 확인하세요 (예: cp949).")
    #         raise
    #     except Exception as e:
    #         print(f"오류: CSV 파일 처리 중 예외 발생 - {e}")
    #         raise

    #     print("읽기 시작")
    #     pass

    def save_command(self, items):
        """그래프 저장하는 함수 호출"""
        pass






