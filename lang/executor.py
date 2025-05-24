from lark import Transformer, v_args
from error import RunningError

class Executor(Transformer):
    def __init__(self):
        super().__init__()
        self.current_graph = None # 현재 가리키고 있는 그래프 객체
        self.graph_context = dict()

        

    def _reset_current_graph(self, name="제목 없는 그래프"):
        self.graph_data = {
            'name': name, # 그래프 생성 시 받은 이름
            'type': None,  # 예: '선그래프'
            'x': [],
            'y': [],
            'Option': {
                'title': name, # 그래프 제목 (그래프 이름과 같거나 다를 수 있음)
                'label': None, # 데이터셋의 레이블 (범례용)
                'marker': {},
                'line': {},
                'x_axis': {},
                'y_axis': {},
                'output': {}
            }
        }       

    def _get_current_graph_options(self):
        """현재 그래프 컨텍스트에 있는 데이터들 반환"""
        if self.current_graph and self.current_graph in self.graph_context:
            return self.graph_context[self.current_graph]
        self._add_error("그래프가 컨텍스트에 없습니다")

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
        return None

    def statement(self, items):
        return None
    
    def create_graph_statement(self, items):
        graph_name = items[1].value.strip("'\"")
        self.graph_context[graph_name] = self._reset_current_graph(graph_name)
        self.current_graph = graph_name

    
    def data_statement(self, items):
        # 데이터 할당문. 종류가 선택된 이후에 실행되어야 한다.
        data = items[2]
        if not self.graph_data['type']:
            print("error.")

    def object_selector(self, items):
        return items[0].type

    def property_key(self, items):
        return items[0]
    
    def property_assignment_statement(self, items): 
        current_graph_data = self._get_current_graph_options()




    def draw_statement(self, items):
        current_graph_to_draw = self._get_current_graph_options()

        if current_graph_to_draw:
            # 실제 함수 호출
            pass
        else:
            self._add_error("그래프 그릴 수 없는 상황")

    def set_axis_labels_statement(self, items):
        pass

    def load_command(self, items):
        pass

    def save_command(self, items):
        pass






