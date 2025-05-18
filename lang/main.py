from lark import Lark
from lark.exceptions import LarkError, UnexpectedToken, UnexpectedCharacters, UnexpectedEOF

grammar_file_path = 'nor.lark'
grammar = None

with open(grammar_file_path, 'r', encoding='utf-8') as f:
    grammar = f.read()

parser = Lark(grammar)

parse_tree = None

script = """
        그래프생성 "하이"
        그려줘
        //this is line comment
        데이터는 [1,2,3,4]
        """
try:
    parse_tree = parser.parse(script)
    print(parse_tree.pretty())
    
except UnexpectedCharacters as err:
    print(f"파싱 오류 {UnexpectedCharacters}: 행 {err.line}, 열 {err.column}, 토큰 '{err.token}'")
    print(f"  예상 토큰: {err.expected}")
    print(f"  컨텍스트: {err.get_context(script, 20)}")
except UnexpectedCharacters as err:
    print(f"파싱 오류 (UnexpectedCharacters): 행 {err.line}, 열 {err.column}, 문자 '{err.char}'")
    print(f"  컨텍스트: {err.get_context(script, 20)}")
except UnexpectedEOF as err:
    print(f"파싱 오류 (UnexpectedEOF): 입력이 예기치 않게 종료되었습니다.")
    print(f"  예상 토큰: {err.expected}")
except LarkError as le: # 기타 Lark 파싱 오류
    print(f"파싱 오류: {le}")

    
