class Error():
    def __init__(self, line, column):
        self.line = 0
        self.column = 0

    def __str__(self):
        return f"에러 ({self.line}번째 줄 {self.column}번째): "
    
class CompileError(Error):
    def __init__(self, line, column, message):
        super().__init__(line, column)
        self.message = message

    def __str__(self):
        return f"컴파일" + super().__str__() + self.message

class RuntimeError(Error):
    def __init__(self, line, column):
        super().__init__(line, column)

    def __str__(self):
        return f"런타임" + super().__str__() + self.message