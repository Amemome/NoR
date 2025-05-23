from lark import Visitor, Tree, Token
from nor_config import VALID_PROPERTY_VALUES, OBJECT_SPECIFIC_VALID_PROPERTY_VALUES

class CompileError(Exception):
    def __init__(self, message, token=None):
        if token:
            line = getattr(token, 'line', '?')
            column = getattr(token, 'column', '?')
            super().__init__(f"컴파일 오류 ({line}번 줄 , {column}번 열): {message}")
        else:
            super().__init__(f"컴파일 오류: {message}")
        self.token = token

class SemanticAnalyzer(Visitor):
    def __init__(self):
        super().__init__()    
        self.graph_created = False # 어떤 그래프라도 만들어져있는가?
        self.data_defined = False # 그래프에 대해서 데이터를 정의했는가?
        self.graph_name = None # 그래프의 이름..
        self.graph_context = [] # 생성된 그래프들을 나타낸다. 현재 그래프는 [-1]위치의 그래프이다.
        self.errors = [] # 오류들을 수집하기 위한 리스트

        self.VALID_PROPERTY_VALUES = VALID_PROPERTY_VALUES
        self.OBJECT_SPECIFIC_VALID_PROPERTY_VALUES = OBJECT_SPECIFIC_VALID_PROPERTY_VALUES
    
    def _add_error(self, message, token=None):
        # 에러를 즉시 발생
        raise CompileError(message, token)
    
    def _get_element_type(self, element_node):
        """element에 대해서 어떤 타입인지 반환하는 함수."""
        # element 가 비었음.
        if not element_node.children:
            return None
        
        child = element_node.children[0]
        if child.data == 'atom':
            atom_child = child.children[0]
            if isinstance(atom_child, Token):
                return atom_child.type 
        elif child.data == 'vector':
            return "VECTOR" # 벡터임을 확인하고 반환.
        
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

    # statement: (object_selector access_operator)? property_key assign_operator STRING 
    def property_assignment_statement(self, tree: Tree):
        """속성 할당문에 대한 유효성 검사를 행한다."""
    
        object_selector_node = None
        property_key_node = None
        string_value_token = None
        
        # 토큰 추출

        children_iter = iter(tree.children)
        
        child1 = next(children_iter, None)
        if child1 and isinstance(child1, Tree) and child1.data == 'object_selector':
            object_selector_node = child1
            next(children_iter, None) # access_operator 건너뛰기
            property_key_node = next(children_iter, None)

        elif child1 and isinstance(child1, Tree) and child1.data == 'property_key':
            property_key_node = child1
        
        # 남은 자식들 중에서 STRING 찾기 (assign_operator 다음)
        for child in children_iter: 
            if isinstance(child, Token) and child.type == 'STRING':
                string_value_token = child
                break

        # 정보 추출
        prop_name_token = property_key_node.children[0] # 실제 속성 키워드 토큰 (예: '종류', '색')
        prop_name_type = prop_name_token.type      # EBNF 터미널 타입 (예: 'SET_TYPE_KEYWORD')
        assigned_value_str = string_value_token.value.strip("'\"")

        current_object_type = "GRAPH_KEYWORD" # object 생략하면 기본은 그래프
        if object_selector_node:
            current_object_type = object_selector_node.children[0].type # 예: "MARKER_KEYWORD"

        valid_values_for_prop = None

        if current_object_type in self.VALIDATION_RULES:
            object_rules = self.VALIDATION_RULES[current_object_type]
            if prop_name_type in object_rules:
                valid_values_for_prop = object_rules[prop_name_type]
            else:
                # 객체(current_object_type)에 해당 속성(prop_name_type) 규칙이 정의되지 않는 경우
                self._add_error(prop_name_token, f"{current_object_type}의 속성에 {prop_name_type}이라는 속성이 존재하지 않습니다.")
        else:
            # 객체(current_object_type)에 대한 규칙 자체가 없는 경우
            error_token = current_object_type if current_object_type else prop_name_token
            self._add_error(error_token, f"{current_object_type}이라는 속성이 존재하지 않습니다.")

        if valid_values_for_prop is None:
            pass # 규칙이 None이면 모든 값을 허용

        elif isinstance(valid_values_for_prop, set): # 유효 값이 문자열 set으로 정의된 경우
            if assigned_value_str not in valid_values_for_prop:
                error_msg = (
                    f"'{object_selector_node.children[0].value if object_selector_node else '기본 객체'}' 객체의 속성 '{prop_name_token.value}'에 유효하지 않은 값 '{assigned_value_str}'이 할당되었습니다. 허용되는 값: {', '.join(sorted(list(valid_values_for_prop)))}."
                )
                self._add_error(string_value_token, error_msg)
            pass
