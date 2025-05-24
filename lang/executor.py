from lark import Transformer, v_args

class Executor(Transformer):
    def __init__(self):
        super.__init__()
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
        self._reset_current_graph(graph_name)
        self.current_graph = graph_name

    def 

    
    def data_statement(self, items):
        # 데이터 할당문. 종류가 선택된 이후에 실행되어야 한다.
        data = items[2]
        if not self.graph_data['type']:
            print("error.")






