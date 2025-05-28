import copy
from lark import Token, Transformer, Tree, v_args
from error import RunningError
import csv

class Executor(Transformer):
    def __init__(self, debug_mode=False):
        super().__init__()
        self.current_graph = None # 현재 가리키고 있는 그래프 객체
        self.graph_context = dict()
        self.errors = []
        self.debug_mode = debug_mode # 실행중인 문장을 출력해주는 모드.

    def _debug_print(self, message): # <-- 추가: 디버그 출력 헬퍼 메서드
        if self.debug_mode:
            print(f"[DEBUG - Executor] {message}")

    def _init_graph_data(self, name="제목 없는 그래프"):
        """그래프 데이터 구조를 option 포맷에 맞춰 반환"""
        self._debug_print("init 성공")
        return {
            '이름': name,      # NoR 스크립트에서 '그래프생성 "이름"' 으로 받은 이름
            '종류': None,      # 예: '선그래프'
            'x': [],
            'y': [],
            '옵션': {          # '옵션' 키 사용
                '제목': name,  # 기본적으로 그래프 이름과 동일하게 시작
                'label': None,

                'marker': {},
                'line': {},
                'x축': {},     # 'x축' 키 사용
                'y축': {},     # 'y축' 키 사용
                '출력': {}
            }
        }
    def _get_current_graph_data_dict(self):
        """현재 그래프 컨텍스트에 있는 데이터들 반환"""
        
        if self.current_graph and self.current_graph in self.graph_context:
            return self.graph_context[self.current_graph]
        self._add_error("그래프가 컨텍스트에 없습니다")
        return None

    def _add_error(self, token=None, message="메세지가 없습니다"):
        line = getattr(token, 'line', '?')
        column = getattr(token, 'column', '?')

        self.errors.append(RunningError(line, column, message)) 

    @v_args(inline=True)
    def atom(self, value_token):
        if value_token.type == 'NUMBER':
            return float(value_token.value)
        elif value_token.type == 'STRING':
            return value_token.value.strip("'\"")
    
    def vector(self, items):
        if items and items[0] == "EMPTY_VECTOR":
            return []
        return items[0]
    
    def empty_vector(self, items):
        return "EMPTY_VECTOR"
    
    def non_empty_vector(self, items):
        return items[0]
    
    def elements(self, items):
        return list(items)
    
    def element(self, items):
        return items[0]
    
    # 문장 처리
    def start(self, items):
        self._debug_print("start")
        return None

    def statement(self, items):
        return None
    
    def create_graph_statement(self, items):
        graph_name = items[1].value.strip("'\"")
        self.graph_context[graph_name] = self._init_graph_data(graph_name)
        self.current_graph = graph_name

    
    def data_statement(self, items):
        # 데이터 할당문. 종류가 선택된 이후에 실행되어야 한다.
        data_keyword_token = items[0]
        current_graph_data = self._get_current_graph_data_dict()
        
        if not current_graph_data:
            self._add_error(message="현재 작업중인 그래프가 없습니다")
            return
        
        if not current_graph_data.get('종류'):
            self._add_error(data_keyword_token, f"그래프 '{self.current_graph}'의 '종류'가 정의되지 않아 데이터를 할당할 수 없습니다.")
            return
        
        data_list = copy.deepcopy(items[2])
        
        current_graph_data['x'] = data_list[0]
        current_graph_data['y'] = data_list[1]


    def object_selector(self, items):
        return items[0].type

    def property_key(self, items):
        return items[0]
    
    def property_assignment_statement(self, items): 
        current_graph_data = self._get_current_graph_data_dict()

        if not current_graph_data:
            first_token_in_statement = items[0] if isinstance(items[0], Token) else (items[0].children[0] if isinstance(items[0], Tree) and items[0].children else None)
            self._add_error(first_token_in_statement, "속성 할당 중 현재 작업 그래프를 찾을 수 없습니다.")
            return
        
        prop_key_token = None
        assigned_value = None
        object_selector = "GRAPH_KEYWORD"

        idx = 0
        if isinstance(items[0], str) and items[0].startswith(("GRAPH_", "X_AXIS_", "Y_AXIS_", "MARKER_", "LINE_")):
            object_selector = items[idx]
            idx += 2
        
        prop_key_token = items[idx]
        assigned_value = items[idx+2]   

        prop_name = prop_key_token.value

        target_dict = None

        if object_selector == "GRAPH_KEYWORD":
            if prop_name == "종류":
                current_graph_data['종류'] = assigned_value
                target_dict = current_graph_data
            elif prop_name in ["배경색", "파일로 저장", "해상도", "그래프 크기", "범례 위치"]:
                target_dict = current_graph_data['옵션']['출력']
                target_dict[prop_name] = assigned_value
            else:
                target_dict = current_graph_data['옵션']
                target_dict[prop_name] = assigned_value

        elif object_selector == "MARKER_KEYWORD":
            target_dict = current_graph_data['옵션']['marker']
            target_dict[prop_name] = assigned_value
        elif object_selector == "LINE_KEYWORD":
            target_dict = current_graph_data['옵션']['line']
            target_dict[prop_name] = assigned_value
        elif object_selector == "X_AXIS_KEYWORD":
            target_dict = current_graph_data['옵션']['x축']
            target_dict[prop_name] = assigned_value
        elif object_selector == "Y_AXIS_KEYWORD":
            target_dict = current_graph_data['옵션']['y축']
            target_dict[prop_name] = assigned_value
        else:
            self._add_error(prop_key_token, f"내부 오류: 처리할 수 없는 객체 선택자 타입 '{object_selector}'")
            return

        if target_dict is None:
            return


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






