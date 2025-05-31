from lark import Visitor, Tree, Token
from nor_config import VALIDATION_RULES, GRAPH_TYPES, MARKER_SHAPES, LINE_STYLES 
from error import CompileError

class SemanticAnalyzer(Visitor):
    def __init__(self):
        super().__init__()    
        self.type_defined = False
        self.graph_created = False # 어떤 그래프라도 만들어져있는가?
        self.data_defined = False # 그래프에 대해서 데이터를 정의했는가?
        self.graph_name = None # 그래프의 이름..
        self.graph_context = [] # 생성된 그래프들을 나타낸다. 현재 그래프는 [-1]위치의 그래프이다.
        self.errors = [] # 오류들을 수집하기 위한 리스트

        self.VALIDATION_RULES = VALIDATION_RULES
    
    def _add_error(self, token, message):
        line = getattr(token, 'line', '?')
        column = getattr(token, 'column', '?')

        self.errors.append(CompileError(line, column, message)) 
    
    def _get_element_type(self, element_node):
        """element에 대해서 어떤 타입인지 반환하는 함수."""
        # element 가 비었음.
        if not element_node.children:
            return None
        
        child = element_node.children[0]
        if child.data == 'atom':
            atom_child = child.children[0]
            if isinstance(atom_child, Token):
                if atom_child.type == 'NUMBER':
                    return 'NUMBER'
                elif atom_child.type == 'STRING':
                    return 'STRING'
                elif atom_child.type == 'BOOLEAN': 
                    return 'BOOLEAN'
        elif child.data == 'vector':
            return "VECTOR"
        return None
    
    def vector(self, tree: Tree):
        """vector 의 요소들의 타입이 전부 같은지 확인한다"""
        # 비어있으면 볼 게 없다.
        if tree.children[0].data == 'empty_vector':
            return
        # vector.children[0]은 'non_empty_vector'
        non_empty_vector_node = tree.children[0]
        # non_empty_vector_node.children[0]은 'elements'
        elements_node = non_empty_vector_node.children[0]

        element_nodes = elements_node.children # element 노드의 리스트

        first_element_type = None           # 벡터의 첫 번째 요소 타입 저장
        first_element_token_for_error = None  # 첫 번째 요소의 위치 정보 (에러 메시지용)
        
        for i, element_node in enumerate(element_nodes):
            current_element_type = self._get_element_type(element_node)
                
            # 위치 정보를 위해 첫 번째 atom/vector 토큰을 찾습니다.
            # element -> atom -> TOKEN 또는 element -> vector
            actual_value_node = element_node.children[0]
            error_token = actual_value_node.children[0] if actual_value_node.children and isinstance(actual_value_node.children[0], Token) else actual_value_node
            
            # token_for_loc은 NUMBER/STRING Token이거나 elements Tree(vector의 경우)

            if i == 0:
                first_element_type = current_element_type
                first_element_token_for_error = error_token

            elif current_element_type != first_element_type:
                # 에러 위치는 현재 요소의 시작 부분으로 잡습니다.
                token_for_report = error_token
                
                # 만약 token_for_loc이 Tree (e.g. elements)면, 그 첫 번째 토큰에서 line/col 가져오기 시도
                final_error_token = token_for_report
                if isinstance(final_error_token, Tree) and final_error_token.children:
                    temp_token = final_error_token.children[0]
                    if isinstance(temp_token, Tree) and temp_token.children: # element -> atom -> TOKEN
                        temp_token = temp_token.children[0] # element
                        if isinstance(temp_token, Tree) and temp_token.children:
                            temp_token = temp_token.children[0] # atom
                            if isinstance(temp_token, Tree) and error_token.children:
                                temp_token = temp_token.children[0] # NUMBER/STRING
                    final_error_token = temp_token
                error_msg = (
                    f"벡터의 내부 요소들의 일관성이 없습니다. "
                    f"'{first_element_type}' 타입을 예상했지만  ({getattr(first_element_token_for_error, 'line', '?')}), "
                    f"'{current_element_type}' 타입이 발견되었습니다."
                )
                # 타입 불일치 발견. 에러에 추가하고. 검사중단.
                self._add_error(final_error_token, error_msg)
                break 

    def create_graph_statement(self, tree: Tree):
        graph_name_token = tree.children[1]
        self.graph_name = graph_name_token.value.strip("'\"")
        self.graph_created = True
        self.type_defined = False
        self.data_defined = False

    def data_statement(self, tree: Tree):
        data_keyword_token = tree.children[0]

        if not self.graph_created:
            self._add_error(data_keyword_token, "데이터를 정의하기 전에 '그래프생성' 명령으로 그래프를 먼저 만들어야 합니다.")
            return
        if not self.type_defined:
            self._add_error(data_keyword_token, f"그래프 '{self.graph_name}'의 '종류'가 정의되지 않아 데이터를 할당할 수 없습니다.")
            return
        
        self.data_defined = True
    
    def draw_statement(self, tree: Tree):
        draw_keyword_token = tree.children[0] # 위치 정보용
        if not self.graph_created:
            self._add_error(draw_keyword_token, "'그리기' 명령 전에 '그래프생성'으로 그래프를 먼저 만들어야 합니다.")
        elif not self.type_defined:
            self._add_error(draw_keyword_token, f"그래프 '{self.graph_name}'의 '종류'가 정의되지 않아 그릴 수 없습니다.")

    def property_assignment_statement(self, tree: Tree):
        obj_selector_node = None
        prop_key_token = None
        value_node = None
        object_keyword_token_from_selector = None
        
        # `c`는 `tree.children`을 가리킴
        c = tree.children 
        
        # --- 파스 트리 구조 분석 및 요소 추출 ---
        # 케이스 1: MARKER_KEYWORD/LINE_KEYWORD로 시작하고 SET_TYPE_KEYWORD를 사용하는 특정 규칙
        # 문법 예: marker_type_prop: MARKER_KEYWORD access_operator SET_TYPE_KEYWORD assign_operator MARKER_SHAPE_VALUE
        # c의 예상 구조: [Token(MARKER_KEYWORD), Token(access_operator), Token(SET_TYPE_KEYWORD), Token(assign_operator), value_node]
        if (len(c) >= 5 and isinstance(c[0], Token) and 
            c[0].type in ["MARKER_KEYWORD", "LINE_KEYWORD"] and 
            isinstance(c[2], Token) and c[2].type == "SET_TYPE_KEYWORD"):
            object_keyword_token_from_selector = c[0]
            # c[1] is access_operator
            prop_key_token = c[2]
            # c[3] is assign_operator
            value_node = c[4]
        
        # 케이스 2: 그 외 (object_selector가 있거나 없거나, SET_TYPE_KEYWORD 또는 일반 속성)
        # 문법 예 (object_selector 없는 SET_TYPE): graph_type_prop: SET_TYPE_KEYWORD assign_operator GRAPH_TYPE_VALUE
        #   c의 예상 구조: [Token(SET_TYPE_KEYWORD), Token(assign_operator), value_node] (만약 (GRAPH_KEYWORD ...)? 부분이 매치 안됐다면)
        # 문법 예 (object_selector 있는 일반 속성): general_prop: object_selector access_operator ...
        #   c의 예상 구조: [Tree(object_selector), Token(access_operator), Token(KEYWORD), Token(assign_operator), value_node]
        # 문법 예 (object_selector 없는 일반 속성): general_prop: KEYWORD assign_operator ...
        #   c의 예상 구조: [Token(KEYWORD), Token(assign_operator), value_node]
        else:
            idx = 0
            # object_selector (Tree) 확인
            if idx < len(c) and isinstance(c[idx], Tree) and c[idx].data == 'object_selector':
                obj_selector_node = c[idx]
                if obj_selector_node.children: # object_selector가 비어있지 않은지 확인
                    object_keyword_token_from_selector = obj_selector_node.children[0]
                idx += 1 # object_selector 건너뛰기
                if idx < len(c): # access_operator 건너뛰기 (존재한다면)
                    idx += 1 
            
            # 속성 키 토큰
            if idx < len(c) and isinstance(c[idx], Token):
                prop_key_token = c[idx]
                idx += 1 # prop_key_token 건너뛰기
                if idx < len(c): # assign_operator 건너뛰기 (존재한다면)
                    idx += 1
                    if idx < len(c): # value_node 할당
                        value_node = c[idx]
                    else:
                        self._add_error(prop_key_token or (c[0] if c else tree), "속성에 할당할 값이 누락되었습니다.")
                        return
                else:
                    self._add_error(prop_key_token or (c[0] if c else tree), "할당 연산자 또는 값이 누락되었습니다.")
                    return
            else:
                err_token = c[0] if c else tree
                self._add_error(err_token, "속성 키를 분석할 수 없습니다.")
                return
        
        # --- 컨텍스트 검사 ---
        if not prop_key_token: # 위 로직에서 prop_key_token이 할당되지 않은 경우 방지
             self._add_error(tree, "속성 할당문의 분석에 실패했습니다 (속성 키 누락).")
             return

        if not self.graph_created:
            self._add_error(prop_key_token, "속성을 설정하기 전에 '그래프생성' 명령으로 그래프를 먼저 만들어야 합니다.")
            return
        
        current_object_type_name = "GRAPH_KEYWORD" 
        if object_keyword_token_from_selector:
            current_object_type_name = object_keyword_token_from_selector.type
        
        prop_key_type_name = prop_key_token.type

        is_defining_graph_main_type = (current_object_type_name == "GRAPH_KEYWORD" and 
                                       prop_key_type_name == "SET_TYPE_KEYWORD")

        if is_defining_graph_main_type:
            if self.type_defined:
                self._add_error(prop_key_token, f"그래프 '{self.current_graph_name}'의 종류는 한 번만 정의할 수 있습니다.")
            self.type_defined = True
        else:
            if not self.type_defined:
                self._add_error(prop_key_token, f"그래프 '{self.current_graph_name}'의 '종류'가 정의되지 않아 '{prop_key_token.value}' 속성을 설정할 수 없습니다.")
                return 
            
        # --- 적용 가능성 검사 (객체-속성 조합) ---
        if current_object_type_name not in self.VALIDATION_RULES:
            error_token_for_object = object_keyword_token_from_selector or \
                                     (obj_selector_node.children[0] if obj_selector_node and obj_selector_node.children else prop_key_token)
            self._add_error(error_token_for_object, f"알 수 없는 객체 타입 '{current_object_type_name}'에 속성을 지정할 수 없습니다.")
            return

        object_specific_rules = self.VALIDATION_RULES[current_object_type_name]
        object_name_for_msg = (object_keyword_token_from_selector.value if object_keyword_token_from_selector 
                               else (obj_selector_node.children[0].value if obj_selector_node and obj_selector_node.children else "그래프"))

        if prop_key_type_name not in object_specific_rules:
            self._add_error(prop_key_token, f"'{object_name_for_msg}' 객체에는 '{prop_key_token.value}' 속성을 설정할 수 없습니다.")
            return
        
        # --- SET_TYPE_KEYWORD에 대한 값 유효성 검사 (분기) ---
        if prop_key_type_name == "SET_TYPE_KEYWORD":
            actual_value_str = ""
            value_token_for_error = value_node 

            # value_node가 Token인지, 아니면 특정 값 규칙(예: MARKER_SHAPE_VALUE)의 Tree인지 확인 필요
            # 문법에서 MARKER_SHAPE_VALUE 등이 규칙(rule)이므로, value_node는 Tree일 가능성이 높음
            # Tree('marker_shape_value', [Token(CIRCLE_MARKER, '원')])
            if isinstance(value_node, Tree) and value_node.children and isinstance(value_node.children[0], Token):
                actual_value_str = value_node.children[0].value
                value_token_for_error = value_node.children[0]
            elif isinstance(value_node, Token): # 만약 value_node가 바로 최종 값 토큰이라면
                actual_value_str = value_node.value
            else:
                self._add_error(value_node or prop_key_token, f"'{prop_key_token.value}' 속성의 값을 분석할 수 없습니다 (예상치 못한 값 노드 구조).")
                return

            valid_types_set = None
            expected_value_description = ""

            if current_object_type_name == "GRAPH_KEYWORD":
                valid_types_set = GRAPH_TYPES # nor_config.py에서 임포트한 GRAPH_TYPES 변수 (세트 형태여야 함)
                expected_value_description = "그래프 종류 (예: 선그래프, 막대그래프)"
            elif current_object_type_name == "MARKER_KEYWORD":
                valid_types_set = MARKER_SHAPES # nor_config.py의 MARKER_SHAPES 변수
                expected_value_description = "마커 종류 (예: 원, 사각형)"
            elif current_object_type_name == "LINE_KEYWORD":
                valid_types_set = LINE_STYLES # nor_config.py의 LINE_STYLES 변수
                expected_value_description = "선 종류 (예: 실선, 점선)"
            # 다른 객체 타입에 SET_TYPE_KEYWORD가 적용된다면 여기에 'elif' 블록 추가

            if valid_types_set is not None: # valid_types_set이 정상적으로 할당된 경우에만 검사
                if actual_value_str not in valid_types_set:
                    # 허용되는 값 목록을 조금만 보여주거나, 대표적인 예시를 보여주는 것이 좋음
                    example_values = list(valid_types_set)[:3] # 처음 3개 예시
                    self._add_error(value_token_for_error, 
                                    f"'{object_name_for_msg}' 객체의 '{prop_key_token.value}' 속성에 유효하지 않은 값 '{actual_value_str}'이(가) 할당되었습니다. "
                                    f"허용되는 값은 {expected_value_description} 중 하나여야 합니다 (예: {', '.join(example_values)}).")
                    return
            else: # 이 객체 타입에 대해 SET_TYPE_KEYWORD에 대한 유효 값 세트가 정의되지 않은 경우
                  # (이 경우는 VALIDATION_RULES에서 prop_key_type_name 검사 시 이미 걸러졌어야 함)
                 self._add_error(prop_key_token, f"내부 오류: '{object_name_for_msg}' 객체의 '{prop_key_token.value}' 속성에 대한 유효 값 규칙이 정의되지 않았습니다.")
                 return
        
        # --- 값이 벡터인 경우 내부 유효성 검사 ---
        if isinstance(value_node, Tree) and value_node.data == 'vector':
            self.visit(value_node)