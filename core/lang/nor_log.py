class NorLog:
    """
    NoR 엔진에서 발생하는 로그 메시지를 나타내는 클래스.
    GUI로 전송될 때 사용되는 형식과 일치하게 한다.
    """
    def __init__(self, source: str, type: str, message: str, line: int = None, column: int = None):
        self.source = source # 예: "parser", "semantic_analyzer", "executor", "system"
        self.type = type     # "success", "info", "error"
        self.message = message
        self.line = line     # 오류/정보가 발생한 라인 번호 (선택 사항)
        self.column = column # 오류/정보가 발생한 컬럼 번호 (선택 사항)

    def to_dict(self):
        """JS 객체 형식으로 변환하기 위한 딕셔너리 반환"""
        log_dict = {
            "source": self.source,
            "type": self.type,
            "message": self.message,
        }
        if self.line is not None:
            log_dict["line"] = self.line
        if self.column is not None:
            log_dict["column"] = self.column
        return log_dict

    def __str__(self):
        """디버그용 문자열 표현"""
        loc_str = f" ({self.line}번째 줄, {self.column}번째 열)" if self.line is not None else ""
        return f"[{self.source.upper()}][{self.type.upper()}]{loc_str}: {self.message}"