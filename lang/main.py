from lark import Lark

grammar_file_path = 'nor.lark'
grammar = None

with open(grammar_file_path, 'r', encoding='utf-8') as f:
    grammar = f.read()

parser = Lark(grammar)

tree = parser.parse("10")
print(tree.pretty())

tree = parser.parse("10 + 20 + 30 + 40")
print(tree.pretty())

tree = parser.parse("""123
                    //this is line comment
                    10 + 20 + 30
                    /* this is block 
                    co
                    mm
                    ent
                    */
                    """)
print(tree.pretty())