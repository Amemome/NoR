class AstNode:
    """
    모든 AST노드의 기본 클래스
    """
    def __init__(self, meta=None):
        self.meta = meta
    
    def accept(self, visitor):
        """
        자식 클래스에서 이 메소드를 오버라이드하여,
        visitor.visit_NodeTypeName(self)를 호출
        """
        method_name = 'visit_' + self.__class__.__name__.lower().replace('node', '')
        visitor_method = getattr(visitor, method_name, visitor.generic_visit_node)
        return visitor_method(self)
