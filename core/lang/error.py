from .nor_log import NorLog
    
class CompileError(NorLog):
    """의미 분석 단계에서 발생하는 에러 (컴파일 에러)."""
    def __init__(self, line, column, message):
        super().__init__(source="의미 분석기", type="error", message=message, line=line, column=column)

    def __str__(self):
        return super().__str__()

class RunningError(NorLog):
    """실행 단계에서 발생하는 에러 (런타임 에러)."""
    def __init__(self, line: int, column: int, message: str):
        # source를 "executor"로 고정하고 type을 "error"로 고정합니다.
        super().__init__(source="executor", type="error", message=message, line=line, column=column)

    def __str__(self):
        return super().__str__() # NorLog의 __str__을 따름