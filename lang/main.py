from lark import Lark
from lark.exceptions import LarkError, UnexpectedToken, UnexpectedCharacters, UnexpectedEOF
from semantic_analyzer import SemanticAnalyzer;
from executor import Executor;

grammar_file_path = 'nor.lark'
grammar = None

with open(grammar_file_path, 'r', encoding='utf-8') as f:
    grammar = f.read()

parser = Lark(grammar, propagate_positions=True)

parse_tree = None

script = """
// Test 3: 객체 선택자 없는 속성 및 기본값
그래프생성 "기본 설정 테스트"
종류는 산점도그래프 
마커의 종류는 ^
라벨은 "범레임"
범례는 우상단

데이터는 [[1,2,3,4,5], [5,4,3,2,1]]

제목은 "산점도 기본 테스트" 
그래프 크기는 [5, 6]  
x축의 색은 "black"
그리기

        """
try:
    parse_tree = parser.parse(script)
    print(parse_tree.pretty())
    analyzer = SemanticAnalyzer()
    analyzer.visit(parse_tree)

    if analyzer.errors:
        print("\nSemantic Errors Found:")
        for error in analyzer.errors:
            print(f"- {error}")
        exit(0)
    else:
        print("\nNo semantic errors found.")
        

    executor = Executor(debug_mode=True)
    executor.transform(parse_tree)

    
except UnexpectedToken as err:
    line, column = err.line, err.column
    token_value = err.token.value
    token_type = err.token.type
    context = err.get_context(script, 40) # 오류 주변 40글자 컨텍스트

    print("\n[파싱 오류]: 문법에 맞지 않는 토큰 발견")
    print(f"위치: {line}번째 줄, {column}번째 열")
    print(f"발견된 토큰: '{token_value}' (타입: {token_type})")
    print("-" * 30)
    print("오류 주변 스크립트 내용:")
    print(context)
    print("-" * 30)
    # err.expected는 문법 파일의 터미널/규칙 이름 리스트입니다.
    # 이를 직접 사용자에게 보여주는 것보다, 어떤 종류의 구문이 와야 하는지 설명하는 것이 더 유용할 수 있습니다.
    # 예: "명령어, 숫자, 문자열 등이 와야 합니다." (문법에 따라 맞춤형 메시지 필요)
    print(f"도움말: 해당 위치에는 '{token_value}' 대신 다른 종류의 구문(예: 명령어 키워드, 값, 연산자 등)이 와야 할 수 있습니다.")
    print(f"         (Lark가 예상한 토큰 타입: {err.expected})")


except UnexpectedCharacters as err:
    line, column = err.line, err.column
    char_found = err.char
    context = err.get_context(script, 40)

    print("\n[파싱 오류]: 예상치 못한 문자 발견")
    print(f"위치: {line}번째 줄, {column}번째 열")
    print(f"발견된 문자: '{char_found}'")
    print("-" * 30)
    print("오류 주변 스크립트 내용:")
    print(context)
    print("-" * 30)
    # err.allowed는 해당 위치에서 허용되는 문자들의 집합이거나,
    # err.expected는 해당 문맥에서 예상되는 토큰 타입들의 리스트일 수 있습니다.
    # Lark 버전에 따라 이 정보의 유용성이 다를 수 있습니다.
    expected_info = ""
    if hasattr(err, 'allowed') and err.allowed:
        expected_info = f"허용되는 문자(일부): {err.allowed}"
    elif hasattr(err, 'expected') and err.expected:
        expected_info = f"예상된 토큰 타입: {err.expected}"
    
    print(f"도움말: '{char_found}' 문자는 현재 위치의 문법에 맞지 않습니다. {expected_info}")
    print(f"         올바른 키워드나 값 형식을 사용했는지, 혹은 오타가 없는지 확인해 보세요.")


except UnexpectedEOF as err:
    print("\n[파싱 오류]: 스크립트가 예기치 않게 종료되었습니다.")
    print(f"도움말: 스크립트의 마지막 부분이 완전한 명령으로 끝나지 않았을 수 있습니다.")
    print(f"         예를 들어, 값을 입력해야 하는 곳에서 스크립트가 끝나거나, 괄호 등이 닫히지 않았을 수 있습니다.")
    if err.expected:
        print(f"         (Lark가 예상한 다음 토큰 타입(일부): {err.expected})")


except LarkError as le:
    print(f"\n[Lark 문법 처리 오류]: {le}")
    print("도움말: 문법 파일(nor.lark) 자체에 오류가 있거나, 스크립트가 문법과 매우 다른 방식으로 작성되었을 수 있습니다.")
    print("        Lark 오류 메시지를 참고하여 문법 파일 또는 스크립트를 확인해 주세요.")

except Exception as e:
    print(f"\n[알 수 없는 오류 발생]: {type(e).__name__} - {e}")
    import traceback
    print("--- 오류 상세 정보 ---")
    traceback.print_exc()
    print("--- ---")
    print("도움말: 프로그램 실행 중 예기치 않은 문제가 발생했습니다. 개발자에게 문의해 주세요.")

    
