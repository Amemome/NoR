from lark import Transformer, v_args

class Executor(Transformer):
    def __init__(self):
        super.__init__()
        self.current_graph = None # 현재 가리키고 있는 그래프 객체
        self._reset_current_graph()

    def _reset_current_graph(self, name="제목 없는 그래프"):
        self.graph_data = {
            '이름': name, # 그래프 생성 시 받은 이름
            '종류': None,  # 예: '선그래프'
            'x': [],
            'y': [],
            '옵션': {
                '제목': name, # 그래프 제목 (그래프 이름과 같거나 다를 수 있음)
                'label': None, # 데이터셋의 레이블 (범례용)
                'marker': {},
                'line': {},
                'x축': {},
                'y축': {},
                '출력': {}
            }
        }       
    
    @v_args(inline=True)
    def atom(self, value_token):
        if value_token.type == 'NUMBER':
            return int(value_token.value)
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
    
    


