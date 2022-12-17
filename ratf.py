import sys
import argparse
from lexer import Lexer
from syntax_analyzer import parser
from parse import SymbolTable,Assembly

if __name__ == "__main__":
    argp = argparse.ArgumentParser(
        prog='ratf.py',
        description=""
    )
    argp.add_argument(
        'file',
        type=str,
        default='none',
    )
    argp.add_argument(
        '-o', '-output',
        type=str,
        default='none',
    )
    options = argp.parse_args()
    try:
        if options.file == '':
            print('Missing input file, proper syntax <ratf inputfile -o outputfile>')
            quit()
        code = open(options.file, "r")
        lex = Lexer(code)
        lex.Tokenize()
        syntax = parser(lex.tokens)
        syntax.parse()
        symbol = SymbolTable(syntax.tokens)
        symbol.parse()
        instructions = Assembly(syntax.tokens,symbol.table)
        instructions.parse()
        for item in instructions.instructions:
            print(item[0],'     ',item[1],'     ','' if item[2] == 'nil' else item[2],'     ')
    except:
        print('invalid input file')
        quit()
    try:
        if (options.o != 'none'):
            f = open(options.o, "w")
            f.write('         Symbol Table\n')
            f.write('Identifier   Type   Memory\n')
            for item in symbol.table:
                f.write(item['token'] + '      ' + item['lexeme'] + '      '+ str(item['memory']) + '\n')
            f.write('\n')
            for item in instructions.instructions:
                f.write(str(item[0]) + '   ' + item[1] + '   ')
                if item[2] == 'nil':
                    f.write('\n')
                else:
                    f.write(str(item[2]) + '\n')
            f.close()
    except:
        print('invalid output file')
        quit()