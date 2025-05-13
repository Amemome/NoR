from lark import Lark

grammar_file_path = 'nor.lark'
grammar = None

with open(grammar_file_path, 'r', encoding='utf-8') as f:
    grammar = f.read()

parser = Lark(grammar)



tree = parser.parse("""
                    그래프생성 "예시그래프"
                    제목은 "example"
                    종류는 "막대그래프"
                    데이터는 [[1, 2, 3, 4, 5],
                    [2,3,5,2,1],
                    [5,3,2,5,2],
                    [1,6,3,6,3],
                    [1,67,4,7,3]]
                    그리기
                    """)
print(tree.pretty())