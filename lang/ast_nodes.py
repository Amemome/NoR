# lark 파서가 생성한 파스 트리를 추상화

class AstNode:
    """
    모든 AST노드의 기본 클래스
    """
    def __init__(self, meta=None):
        """
        meta: Lark 토큰/규칙의 위치 정보 (line, column, end_line, end_column 등).
        """
        self.meta = meta
    
    def accept(self, visitor):
        """
        자식 클래스에서 이 메소드를 오버라이드하여,
        visitor.visit_NodeTypeName(self)를 호출
        """
        # 방문할 메서드 이름 생성. visit_클래스이름 - 노드
        # getattr 함수는 객체에서,  값을 얻을 속설명
        method_name = 'visit_' + self.__class__.__name__.lower().replace('node', '')
        visitor_method = getattr(visitor, method_name, visitor.generic_visit_node)
        return visitor_method(self)


# --- 문장 노드들 ---

class StartNode(AstNode):
    """스크립트 전체를 나타내는 루트 노드."""
    def __init__(self, statements, meta=None):
        super().__init__(meta)
        self.statements = statements # statement 노드들의 리스트

    def accept(self, visitor):
        return visitor.visit_start(self)

class CreateGraphNode(AstNode):
    """'그래프생성' 명령을 나타내는 노드."""
    def __init__(self, graph_name_str, meta=None): # 값은 항상 문자열
        super().__init__(meta)
        self.graph_name_str = graph_name_str # 생성할 그래프의 이름 (문자열)

    def accept(self, visitor):
        return visitor.visit_creategraph(self)

class PropertyAssignmentNode(AstNode):
    """속성 할당 명령을 나타내는 노드."""
    def __init__(self, property_key_str, value_str, object_selector_str=None, assign_operator_str=None, access_operator_str=None, meta=None):
        super().__init__(meta)
        self.object_selector_str = object_selector_str # 대상 객체 이름 (문자열) 또는 None
        self.access_operator_str = access_operator_str # 접근 연산자 (문자열) 또는 None
        self.property_key_str = property_key_str       # 속성 이름 (문자열)
        self.assign_operator_str = assign_operator_str # 할당 연산자 (문자열)
        self.value_str = value_str                     # 할당할 값 (항상 문자열)

    def accept(self, visitor):
        return visitor.visit_propertyassignment(self)

class SetAxisLabelsNode(AstNode): # complex_assignment_statement의 한 종류
    """'축이름 "X축이름" "Y축이름"' 명령을 나타내는 노드."""
    def __init__(self, x_label_str, y_label_str, meta=None):
        super().__init__(meta)
        self.x_label_str = x_label_str # 문자열
        self.y_label_str = y_label_str # 문자열

    def accept(self, visitor):
        return visitor.visit_setaxislabels(self)

class DataStatementNode(AstNode):
    """'데이터는 [값1, 값2, ...]' 명령을 나타내는 노드."""
    def __init__(self, data_vector, assign_operator_str=None, meta=None): # data_vector는 AstBuilder에서 처리된 Python 리스트
        super().__init__(meta)
        self.assign_operator_str = assign_operator_str
        self.data_vector = data_vector # Python 리스트 (내부 요소들은 atom 또는 vector의 결과)

    def accept(self, visitor):
        return visitor.visit_datastatement(self)

class DrawStatementNode(AstNode):
    """'그리기' 명령을 나타내는 노드."""
    def __init__(self, meta=None):
        super().__init__(meta)

    def accept(self, visitor):
        return visitor.visit_drawstatement(self)

class LoadCommandNode(AstNode):
    """'로드 "파일명"' 명령을 나타내는 노드."""
    def __init__(self, filename_str, meta=None):
        super().__init__(meta)
        self.filename_str = filename_str # 문자열

    def accept(self, visitor):
        return visitor.visit_loadcommand(self)

class SaveCommandNode(AstNode):
    """'저장 "파일명"' 명령을 나타내는 노드."""
    def __init__(self, filename_str, meta=None):
        super().__init__(meta)
        self.filename_str = filename_str # 문자열

    def accept(self, visitor):
        return visitor.visit_savecommand(self)
