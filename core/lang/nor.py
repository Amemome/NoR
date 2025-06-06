from lark import Lark
from lark.exceptions import LarkError, UnexpectedToken, UnexpectedCharacters, UnexpectedEOF
from .semantic_analyzer import SemanticAnalyzer;
from .executor import Executor;
from .nor_grammar import nor_grammar
from .nor_log import NorLog

class NoR:
    def __init__(self, debug_mode, server_mode):
        self.grammar = nor_grammar
        self.debug_mode = debug_mode
        self.server_mode = server_mode
        self.parser = None
        self.logs = []
        self.script = ""
        self.graph_props = {}

    def get_graph_props(self):
        return self.graph_props
    

    def _add_nor_log_entry(self, source: str, type: str, message: str, line: int = None, column: int = None):
        """내부에서 NorLog 객체를 생성하여 중앙 logs 리스트에 추가하는 헬퍼 메서드"""
        log_entry = NorLog(source, type, message, line, column)
        self.logs.append(log_entry)
        if self.debug_mode:
            print(str(log_entry)) # 콘솔에도 출력

    def _format_lark_error_as_nor_log(self, err_type, err, script_content):
        """Lark 예외를 NorLog 객체로 변환하여 반환"""
        line, column = getattr(err, 'line', '?'), getattr(err, 'column', '?')
        message = str(err)
        context = ""
        # expected_info = "" # 사용하지 않으므로 제거

        if hasattr(err, 'get_context'):
            context = err.get_context(script_content, 40)
        
        specific_message = ""
        if isinstance(err, UnexpectedToken):
            token_value = err.token.value
            token_type = err.token.type
            specific_message = f"문법에 맞지 않는 토큰 '{token_value}' (타입: {token_type}) 발견."
            # if err.expected:
            #     expected_info = f"예상된 토큰 타입(일부): {err.expected}"
        elif isinstance(err, UnexpectedCharacters):
            char_found = err.char
            specific_message = f"예상치 못한 문자 '{char_found}' 발견."
            # if hasattr(err, 'allowed') and err.allowed:
            #     expected_info = f"허용되는 문자(일부): {err.allowed}"
            # elif hasattr(err, 'expected') and err.expected:
            #     expected_info = f"예상된 토큰 타입(일부): {err.expected}"
        elif isinstance(err, UnexpectedEOF):
            specific_message = "스크립트가 예기치 않게 종료됨 (명령이 완전하지 않을 수 있음)."
            # if err.expected:
            #     expected_info = f"예상된 다음 토큰 타입(일부): {err.expected}"
        elif isinstance(err, LarkError):
            specific_message = f"Lark 문법 처리 오류: {message}"
        
        full_message = f"컴파일 오류 (행: {line}, 열: {column}): {specific_message}"
        if context:
            full_message += f"\n    오류 주변 내용: ...{context}..."
        # if expected_info: # 이제 사용하지 않으므로 제거
        #     full_message += f"\n    참고: {expected_info}"
            
        return NorLog(source="parser", type="error", message=full_message, line=line, column=column)
    
    def run(self, script):
        """
        NoR 스크립트를 파싱, 의미 분석, 실행하여 결과를 반환합니다.

        Args:
            script (str): 실행할 NoR 스크립트 문자열.

        Returns:
            tuple: (execution_result_data, all_errors) 튜플을 반환합니다.
                   - execution_result_data: 실행 성공 시 Executor가 반환한 최종 데이터 (예: 그래프 객체),
                                            실패 시 None.
                   - all_errors: 발생한 모든 오류 메시지(문자열)의 리스트.
        """
        parse_tree = None
        self.logs = []
        execution_result_data = None

        # 1. 파서 초기화
        try:
            self.parser = Lark(grammar=self.grammar, propagate_positions=True)
            if self.debug_mode:
                print("Lark 파서 초기화 완료.")
        except Exception as e:
            self._add_nor_log_entry(source="parser", type="error", message=f"Lark 파서 초기화 오류: {e}\n  문법 정의(nor_grammar.py)에 문제가 없는지 확인하세요.")
            if self.debug_mode:
                import traceback
                traceback.print_exc()
            return [log.to_dict() if self.server_mode else str(log) for log in self.logs]
        
        # 2. 파싱 (Syntactic Analysis)
        if self.debug_mode:
            print("\n--- 파싱 단계 시작 ---")
            self._add_nor_log_entry(source="parser", type="info", message="파싱 단계 시작.")
        try:
            parse_tree = self.parser.parse(script)
            if self.debug_mode:
                print("파싱 성공.")
                self._add_nor_log_entry(source="parser", type="success", message="파싱 성공. 추상 구문 트리 생성 완료.")
        except UnexpectedToken as e:
            self.logs.append(self._format_lark_error_as_nor_log("UnexpectedToken", e, script))
        except UnexpectedCharacters as e:
            self.logs.append(self._format_lark_error_as_nor_log("UnexpectedCharacters", e, script))
        except UnexpectedEOF as e:
            self.logs.append(self._format_lark_error_as_nor_log("UnexpectedEOF", e, script))
        except LarkError as e:
            self.logs.append(self._format_lark_error_as_nor_log("LarkError", e, script))
        except Exception as e:
            line = getattr(e, 'line', '?') 
            col = getattr(e, 'column', '?')
            self._add_nor_log_entry(source="parser", type="error", message=f"파싱 중 예상치 못한 내부 오류 발생: (행: {line}, 열: {col}): {e}", line=line, column=col)
            if self.debug_mode:
                import traceback
                traceback.print_exc()

        # 파싱 오류가 있으면 이후 단계 진행하지 않음
        if any(log.type == "error" and log.source == "parser" for log in self.logs):
                self._add_nor_log_entry(source="system", type="info", message=f"파싱 오류 발견. 의미 분석 및 실행 건너뜀.")
                return [log.to_dict() if self.server_mode else str(log) for log in self.logs]
        
        # 3. 의미 분석 (Semantic Analysis)
        if self.debug_mode:
            print("\n--- 의미 분석 단계 시작 ---")
            self._add_nor_log_entry(source="semantic_analyzer", type="info", message="의미 분석 단계 시작.")
        
        analyzer = SemanticAnalyzer()
        try:
            analyzer.visit(parse_tree)
           # SemanticAnalyzer가 수집한 CompileError 객체들을 직접 logs 리스트에 추가
            if analyzer.errors:
                self.logs.extend(analyzer.errors) # CompileError 객체는 이미 NorLog를 상속받음
                self._add_nor_log_entry(source="semantic_analyzer", type="error", message=f"의미 오류 {len(analyzer.errors)}개 발견.")
            else:
                self._add_nor_log_entry(source="semantic_analyzer", type="success", message="의미 분석 성공. 의미 오류 없음.")
            
            if self.debug_mode and not analyzer.errors:
                 print("의미 분석 성공. 의미 오류 없음.")
            elif self.debug_mode and analyzer.errors:
                 print(f"의미 오류 {len(analyzer.errors)}개 (SemanticAnalyzer.errors에서) 발견. all_errors에 추가됨.")
        except Exception as e:
            self._add_nor_log_entry(source="semantic_analyzer", type="error", message=f"의미 분석 중 예상치 못한 내부 오류 발생: {e}")
            if self.debug_mode:
                import traceback
                traceback.print_exc()
            return [log.to_dict() if self.server_mode else str(log) for log in self.logs]

        # 의미 오류가 있으면 실행 단계로 넘어가지 않음
        if any(log.type == "error" and log.source == "semantic_analyzer" for log in self.logs):
            self._add_nor_log_entry(source="system", type="info", message="의미 오류로 인해 실행 건너뜀.")
            return [log.to_dict() if self.server_mode else str(log) for log in self.logs]

        # 4. 실행 (Execution / Code Generation)
        if self.debug_mode:
            print("\n--- 실행 단계 시작 ---")
            self._add_nor_log_entry(source="executor", type="info", message="실행 단계 시작.")
        executor = Executor(debug_mode=self.debug_mode, is_server=self.server_mode)
        try:
            execution_result_data = executor.transform(parse_tree)
            self.graph_props = executor.graph_context[executor.graph_name]
            # Executor가 수집한 RunningError 객체들을 직접 logs 리스트에 추가
            if executor.errors:
                self.logs.extend(executor.errors) # RunningError 객체는 이미 NorLog를 상속받음
                self._add_nor_log_entry(source="executor", type="error", message=f"런타임 오류 {len(executor.errors)}개 발견.")
            else:
                self._add_nor_log_entry(source="executor", type="success", message="실행 성공. 런타임 오류 없음.")
            
            if self.debug_mode and not executor.errors:
                print("실행 성공. 런타임 오류 없음.")
            elif self.debug_mode and executor.errors:
                print(f"런타임 오류 {len(executor.errors)}개 (Executor.errors에서) 발견. all_errors에 추가됨.")

        except Exception as e:
            line = getattr(e, 'line', '?')
            col = getattr(e, 'column', '?')
            self._add_nor_log_entry(source="executor", type="error", message=f"실행 중 예상치 못한 내부 오류 발생: (행: {line}, 열: {col}): {e}", line=line, column=col)
            if self.debug_mode:
                import traceback
                traceback.print_exc()
            return [log.to_dict() if self.server_mode else str(log) for log in self.logs]
        
        # 모든 단계가 오류 없이 완료되었고, 특정 실행 결과(그래프 저장 등)도 있다면 성공 메시지 추가
        if not any(log.type == "error" for log in self.logs):
            if execution_result_data:
                action_msg = ""
                if execution_result_data.get('action') == 'save':
                    action_msg = f"'{execution_result_data.get('filename', '그래프')}' 파일 저장 요청 완료."
                elif execution_result_data.get('action') == 'display':
                    action_msg = "그래프 화면 표시 요청 완료."
                self._add_nor_log_entry(source="system", type="success", message=f"모든 단계 성공적으로 완료. {action_msg}")
            else:
                self._add_nor_log_entry(source="system", type="success", message="모든 단계 성공적으로 완료. 추가 실행 결과는 없습니다.")

        # 최종 반환 형식: 딕셔너리로 `execution_result`와 `logs`를 포함
        return [log.to_dict() if self.server_mode else str(log) for log in self.logs]


# grammar_file_path = 'nor.lark'
# grammar = None

# with open(grammar_file_path, 'r', encoding='utf-8') as f:
#     grammar = f.read()

# parser = Lark(grammar, propagate_positions=True)

# parse_tree = None


# // Test 3: 객체 선택자 없는 속성 및 기본값
# 그래프생성 "기본 설정 테스트"
# 종류는 산점도그래프 
# 마커의 종류는 ^
# 라벨은 "범레123"
# 범례는 우상단

# 데이터는 [[1,2,3,4,5], [5,4,3,2,1]]

# 제목은 "산점도 기본 테스트" 
# 그래프 크기는 [5, 6]  
# x축의 색은 "black"
# x축의 이름은 "엑스축"
# y축의 이름은 "와이"
# x축의 라벨은 "하이"
# 그리기


# try:
#     parse_tree = parser.parse(script)
#     print(parse_tree.pretty())

#     analyzer = SemanticAnalyzer()
#     analyzer.visit(parse_tree)

#     if analyzer.errors:
#         print("\nSemantic Errors Found:")
#         for error in analyzer.errors:
#             print(f"- {error}")
#         exit(0)
#     else:
#         print("\nNo semantic errors found.")
        

#     executor = Executor(debug_mode=True)
#     executor.transform(parse_tree)

#     if executor.errors:
#         print("\nRuntime Errors Found:")
#         for error in executor.errors:
#             print(f"- {error}")
#         exit(0)
#     else:
#         print("\nRuntime errors found.")

# except UnexpectedToken as err:
#     line, column = err.line, err.column
#     token_value = err.token.value
#     token_type = err.token.type
#     context = err.get_context(script, 40) # 오류 주변 40글자 컨텍스트

#     print("\n[파싱 오류]: 문법에 맞지 않는 토큰 발견")
#     print(f"위치: {line}번째 줄, {column}번째 열")
#     print(f"발견된 토큰: '{token_value}' (타입: {token_type})")
#     print("-" * 30)
#     print("오류 주변 스크립트 내용:")
#     print(context)
#     print("-" * 30)
#     # err.expected는 문법 파일의 터미널/규칙 이름 리스트입니다.
#     # 이를 직접 사용자에게 보여주는 것보다, 어떤 종류의 구문이 와야 하는지 설명하는 것이 더 유용할 수 있습니다.
#     # 예: "명령어, 숫자, 문자열 등이 와야 합니다." (문법에 따라 맞춤형 메시지 필요)
#     print(f"도움말: 해당 위치에는 '{token_value}' 대신 다른 종류의 구문(예: 명령어 키워드, 값, 연산자 등)이 와야 할 수 있습니다.")
#     print(f"         (Lark가 예상한 토큰 타입: {err.expected})")


# except UnexpectedCharacters as err:
#     line, column = err.line, err.column
#     char_found = err.char
#     context = err.get_context(script, 40)

#     print("\n[파싱 오류]: 예상치 못한 문자 발견")
#     print(f"위치: {line}번째 줄, {column}번째 열")
#     print(f"발견된 문자: '{char_found}'")
#     print("-" * 30)
#     print("오류 주변 스크립트 내용:")
#     print(context)
#     print("-" * 30)
#     # err.allowed는 해당 위치에서 허용되는 문자들의 집합이거나,
#     # err.expected는 해당 문맥에서 예상되는 토큰 타입들의 리스트일 수 있습니다.
#     # Lark 버전에 따라 이 정보의 유용성이 다를 수 있습니다.
#     expected_info = ""
#     if hasattr(err, 'allowed') and err.allowed:
#         expected_info = f"허용되는 문자(일부): {err.allowed}"
#     elif hasattr(err, 'expected') and err.expected:
#         expected_info = f"예상된 토큰 타입: {err.expected}"
    
#     print(f"도움말: '{char_found}' 문자는 현재 위치의 문법에 맞지 않습니다. {expected_info}")
#     print(f"         올바른 키워드나 값 형식을 사용했는지, 혹은 오타가 없는지 확인해 보세요.")


# except UnexpectedEOF as err:
#     print("\n[파싱 오류]: 스크립트가 예기치 않게 종료되었습니다.")
#     print(f"도움말: 스크립트의 마지막 부분이 완전한 명령으로 끝나지 않았을 수 있습니다.")
#     print(f"         예를 들어, 값을 입력해야 하는 곳에서 스크립트가 끝나거나, 괄호 등이 닫히지 않았을 수 있습니다.")
#     if err.expected:
#         print(f"         (Lark가 예상한 다음 토큰 타입(일부): {err.expected})")


# except LarkError as le:
#     print(f"\n[Lark 문법 처리 오류]: {le}")
#     print("도움말: 문법 파일(nor.lark) 자체에 오류가 있거나, 스크립트가 문법과 매우 다른 방식으로 작성되었을 수 있습니다.")
#     print("        Lark 오류 메시지를 참고하여 문법 파일 또는 스크립트를 확인해 주세요.")

# except Exception as e:
#     print(f"\n[알 수 없는 오류 발생]: {type(e).__name__} - {e}")
#     import traceback
#     print("--- 오류 상세 정보 ---")
#     traceback.print_exc()
#     print("--- ---")
#     print("도움말: 프로그램 실행 중 예기치 않은 문제가 발생했습니다. 개발자에게 문의해 주세요.")

    