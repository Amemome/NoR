from lark import Lark, Transformer, v_args, Token


class AstBuilder(Transformer):
    # --- 터미널 변환 (위에서 정의한 STRING, NUMBER, TRUE, FALSE) ---

    # @v_args 는 무엇인가?
    # 메소드가 인자를 받는 형식을 변경해준다.
    # 사용하지 않으면 기본으로 items 라는 단일 인자를 받는다.
    # items 는 해당 규칙의 자식 노드들의 변환된 결과를 담고 있는 리스트.
    # v_args 를 사용하면 items 리스트 대신, 자식 노드들의 변환된 결과를 개별 인자로 받는다.
    # 예를 들어, 규칙이 rule: child1 child2 child3 이고 각 자식이 res1, res2, res3로 변환되었다면, @v_args를 사용한 메소드는 method(self, res1, res2, res3) 형태로 호출된다.
    # inline=True 옵션은 뭐냐? 해당 규칙이 단 하나의 자식노듬나 가지고 있고, 비터미널 규칙에 의해 생성된것이 아니라면 리스트가 아니라 그냥 그 자식을 반환.
    
    # 터미널규칙: 더 이상 다른 규칙으로 분해되지 않음.
    # 비터미너규칙: 다른 규칙으로 분해 간으.
    @v_args(inline=True)
    def STRING(self, token):
        # 추후에 생각해보기 \" 이 " 으로 해석될 수 있기 때문.
        # 파이썬 문자열 리터럴에서는 저렇게 변환되지만 스크립트를 따로 받아와서 할 떄는 어떻게 될지 모름.
        return token.value[1:-1].replace('\\"', '"').replace("\\'", "'").replace('\\\\', '\\')
    
    @v_args(inline=True)
    def NUMBER(self, token):
        s = token.value
        return float(s)
    
    @v_args(inline=True)
    def TRUE(self, token):
        return True
    
    @v_args(inline=True)
    def FALSE(self, token):
        return False    
    
    # --- 기본 데이터 타입 관련 규칙 ---
    
    @v_args(inline=True)
    def atom(self, value):
        return value
    
    def BOOLEAN(self, items):
        return items[0]
    
    @v_args(inline=True) # vector는 empty_vector 또는 non_empty_vector의 결과를 받음
    def vector(self, value): # value는 Python 리스트
        return value
    
    def empty_vector(self, items):
        return []
    
    def non_empty_vector(self, items):
        # 문법: element ("," element)*
        # items는 [element_결과, Token(','), element_결과, ...] 형태가 됨.
        # 또는 Lark가 쉼표를 무시하고 [element_결과, element_결과, ...] 로 줄 수도 있음 (%ignore COMMA 설정에 따라)
        # 만약 COMMA를 무시하도록 설정했다면, items는 이미 element_결과들의 리스트임.
        # 여기서는 COMMA가 무시되었다고 가정 (또는 명시적으로 필터링)
        return items
    
    @v_args(inline=True)
    def element(self, value):
        return value
    

    @v_args(inline=True)
    def assign_operator(self, token): return token.value

    @v_args(inline=True)
    def access_operator(self, token): return token.value

    # object_selector와 property_key는 여러 터미널 중 하나이므로,
    # 각 터미널 Token의 value를 반환.
    def object_selector(self, items): return items[0].value # 예: Token('MARKER_KEYWORD', '마커') -> "마커"
    def property_key(self, items): return items[0].value    # 예: Token('SET_TITLE_KEYWORD', '제목') -> "제목"

    