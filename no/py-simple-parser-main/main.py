from reader import Reader
from parsing import *
from interpreter import Interpreter

print("""
py-simple-parser. Parse a simple mathematical expression

examples:
    > 2+3*(4 + 5.5)
    > 6/2^2
    > 12*(15+(2*3))

You can always type 'exit' to finish execution
""")

while True:
    string = input('Type an expression to evaluate: ')
    if string == 'exit':
        break
    reader = Reader(string)
    tokens = reader.CreateTokens()
    parser = Parser(tokens)
    tree = parser.Parse()
    interpreter = Interpreter()
    res = interpreter.Calc(tree)

    print(f'''
    Tokens: {list(Reader(string).CreateTokens())}
    Tree: {tree}
    Result: {res: .2f}
    ''')

exit(1)

