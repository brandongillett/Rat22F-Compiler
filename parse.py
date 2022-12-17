MEMORY_ADDRESS = 5000
data_types = ['integer', 'boolean', 'float', 'real']


class SymbolTable:
    def __init__(self, tokens):
        self.table = []
        self.tokens = tokens
        self.current_memory = MEMORY_ADDRESS

    def getPreviousToken(self, token):
        index = self.tokens.index(token)
        prev_found = True
        increment = 1
        while prev_found:
            if self.tokens[index - increment]['lexeme'] != 'separator' and self.tokens[index - increment]['lexeme'] != 'operator':
                return self.tokens[index - increment]
            else:
                increment += 1

    def getNextToken(self, token):
        index = self.tokens.index(token)
        next_found = True
        increment = 1
        while next_found:
            if self.tokens[index + increment]['lexeme'] != 'separator' and self.tokens[index + increment]['lexeme'] != 'operator':
                next_found = False
                return self.tokens[index + increment]
            else:
                increment += 1

    def findType(self, token):
        check = token['productions'][len(token['productions']) - 1]
        check = check.split()
        if '<Identifier>' in check:
            type_found = False
            new_token = token
            while not type_found:
                for production in new_token['productions']:
                    if production == '<Identifier>':
                        return 'identifier', True
                    elif production == '<Expression> -> <Term>' or production == '<Assign> -> <Identifier>':
                        for item in self.table:
                            if item['token'] == new_token['token']:
                                return item['lexeme'], False
                        print("Variable " + token['token'] + ' is being used but is not declared.')
                        quit()
                    elif production == '<Parameter> -> <IDs> <Qualifier>':
                        new_token = self.getNextToken(new_token)
                        if new_token['lexeme'] == 'keyword' and new_token['token'] not in data_types:
                            for symbol in self.table:
                                if symbol['token'] == new_token[token]:
                                    return symbol['lexeme'], True
                        break
                    elif production == '<Declaration> -> <IDs>' or production == '<IDs> -> <Identifier> , <IDs>' \
                            or (production == '<IDs> -> <Identifier>' and (
                            '<IDs> -> <Identifier> , <IDs>' in self.getPreviousToken(new_token)['productions'])):
                        new_token = self.getPreviousToken(new_token)
                        if new_token['lexeme'] == 'keyword' and new_token['token'] not in data_types:
                            for symbol in self.table:
                                if symbol['token'] == token['token']:
                                    return symbol['lexeme'], False
                        break
                    elif production == '<Qualifier> -> integer' or production == '<Primary> -> <Integer>':
                        return 'integer', True
                    elif production == '<Qualifier> -> boolean' or production == '<Primary> -> true' or production == '<Primary> -> false':
                        return 'boolean', True
                    elif production == '<Qualifier> -> real' or production == '<Primary> -> <Real>':
                        return 'real', True
                    elif production == '<Identifier>' or production == '<Primary> -> <Identifier>' or production == '<IDs> -> <Identifier>':
                        for item in self.table:
                            if item['token'] == new_token['token']:
                                return item['lexeme'], False
                        return 'identifier', True
            return 'not found'
        elif '<Integer>' in check:
            return 'integer', False
        elif 'true' in check:
            return 'boolean', False
        elif 'false' in check:
            return 'boolean', False

    def doesExist(self, token):
        for item in self.table:
            if token['token'] == item['token'] and self.findType(token)[0] == item['lexeme']:
                return True
        return False

    def insertSymbol(self, token):
        self.table.append({'token': token['token'], 'lexeme': self.findType(token)[0], 'memory': self.current_memory})
        self.current_memory += 1

    def printIdentifiers(self):
        print('{:^60}'.format('Symbol Table') + '\n')
        print('{:^20}'.format('Identifier') + '{:^20}'.format('Type') + '{:^20}'.format('Memory') + '\n')
        for token in self.table:
            print('{:^20}'.format(token['token']) + '{:^20}'.format(token['lexeme']) + '{:^20}'.format(str(token['memory']) + '\n'))
        print('\n')
    def parse(self):
        for token in self.tokens:
            if token['lexeme'] == 'identifier':
                isbeingdeclared = self.findType(token)[1]
                if self.doesExist(token) and isbeingdeclared:
                    print('Error: token ' + token['token'] + ' is being declared twice.')
                    quit()
                elif isbeingdeclared:
                    self.insertSymbol(token)
        self.printIdentifiers()


class Assembly:
    def __init__(self, tokens, symbols):
        self.expressions = {'+': self.add, '-': self.sub, '*': self.mul, '/': self.div}
        self.relop = {'==': self.equ, '!=': self.neq, '>': self.grt, '<': self.les, '<=': self.leq, '=>': self.geq}
        self.instructions = []
        self.tokens = tokens
        self.symbols = symbols
        self.count = 0

    def pushi(self, iv):
        self.count += 1
        instruction = [self.count, 'PUSHI', iv]
        self.instructions.append(instruction)

    def pushm(self, ml):
        self.count += 1
        instruction = [self.count, 'PUSHM', ml]
        self.instructions.append(instruction)

    def popm(self, ml):
        self.count += 1
        instruction = [self.count, 'POPM', ml]
        self.instructions.append(instruction)

    def stdout(self):
        self.count += 1
        instruction = [self.count, 'STDOUT', 'nil']
        self.instructions.append(instruction)

    def stdin(self):
        self.count += 1
        instruction = [self.count, 'STDIN', 'nil']
        self.instructions.append(instruction)

    def add(self):
        self.count += 1
        instruction = [self.count, 'ADD', 'nil']
        self.instructions.append(instruction)

    def sub(self):
        self.count += 1
        instruction = [self.count, 'SUB', 'nil']
        self.instructions.append(instruction)

    def mul(self):
        self.count += 1
        instruction = [self.count, 'MUL', 'nil']
        self.instructions.append(instruction)

    def div(self):
        self.count += 1
        instruction = [self.count, 'DIV', 'nil']
        self.instructions.append(instruction)

    def grt(self):
        self.count += 1
        instruction = [self.count, 'GRT', 'nil']
        self.instructions.append(instruction)

    def les(self):
        self.count += 1
        instruction = [self.count, 'LES', 'nil']
        self.instructions.append(instruction)

    def equ(self):
        self.count += 1
        instruction = [self.count, 'EQU', 'nil']
        self.instructions.append(instruction)

    def neq(self):
        self.count += 1
        instruction = [self.count, 'NEQ', 'nil']
        self.instructions.append(instruction)

    def geq(self):
        self.count += 1
        instruction = [self.count, 'GEQ', 'nil']
        self.instructions.append(instruction)

    def leq(self):
        self.count += 1
        instruction = [self.count, 'LEQ', 'nil']
        self.instructions.append(instruction)

    def jumpz(self, il):
        self.count += 1
        instruction = [self.count, 'JUMPZ', il]
        self.instructions.append(instruction)

    def jump(self, il):
        self.count += 1
        instruction = [self.count, 'JUMP', il]
        self.instructions.append(instruction)

    def label(self):
        self.count += 1
        instruction = [self.count, 'LABEL', 'nil']
        self.instructions.append(instruction)

    def scan(self, pos):
        while '<Scan> -> get (<IDs>);' not in self.tokens[pos]['productions']:
            pos += 1
        while self.tokens[pos]['token'] != ')':
            if self.tokens[pos]['lexeme'] == 'identifier':
                self.stdin()
                self.popm(self.getmemloc(self.tokens[pos]['token']))
            pos += 1
        pos += 2
        return pos

    def print(self, pos):
        while '<Print> -> put (<Expression>);' not in self.tokens[pos]['productions']:
            pos += 1
        pos += 2
        pos = self.getexpr(pos)
        self.stdout()
        pos += 1
        return pos

    def ret(self, pos):
        while '<Return> -> return; | return <Expression>;' not in self.tokens[pos]['productions']:
            pos += 1
        pos += 1
        if self.tokens[pos]['token'] == ';':
            pos += 1
        else:
            pos = self.getexpr(pos)
        return pos

    def assign(self, pos):
        while '<Assign> -> <Identifier> = <Expression>;' not in self.tokens[pos]['productions']:
            pos += 1
        ident = pos
        pos += 2
        pos = self.getexpr(pos)
        self.popm(self.getmemloc(self.tokens[ident]['token']))
        return pos

    def ifstat(self, pos):
        while self.tokens[pos]['token'] != 'if':
            pos += 1
        temp = pos
        pos += 2
        pos = self.getexpr(pos)
        relop = pos - 1
        if self.tokens[pos]['token'] + self.tokens[pos-1]['token'] in self.relop:
            pos += 1
        pos = self.getexpr(pos)
        self.getrelop(relop)
        self.jumpz(0)
        jump = self.count - 1
        end = 0
        for item in self.tokens[temp]['productions']:
            if item == '<Statement> -> <Scan>':
                pos = self.scan(pos)
            elif item == '<Statement> -> <Print>':
                pos = self.print(pos)
            elif item == '<Statement> -> <Return>':
                pos = self.ret(pos)
            elif item == '<Statement> -> <Assign>':
                pos = self.assign(pos)
            elif item == '<Statement> -> <If>':
                pos = self.ifstat(pos)
            elif item == '<Statement> -> <While>':
                pos = self.whilestat(pos)
            elif item == '<If> -> if (<Condition>) <Statement> else <Statement> endif':
                self.jump(end)
                self.instructions[jump][2] = self.count + 1
                end = self.count - 1
        if self.instructions[jump][2] == 0:
            self.instructions[jump][2] = self.count + 1
        if end != 0:
            self.instructions[end][2] = self.count + 1
        pos += 1
        if self.tokens[pos]['token'] == 'endif':
            pos += 1
        if self.tokens[pos]['token'] == '$':
            self.label()
        return pos

    def whilestat(self, pos):
        while self.tokens[pos]['token'] != 'while':
            pos += 1
        self.label()
        labelpos = self.count
        temp = pos
        pos += 2
        pos = self.getexpr(pos)
        relop = pos - 1
        if self.tokens[pos]['token'] + self.tokens[pos-1]['token'] in self.relop:
            pos += 1
        pos = self.getexpr(pos)
        self.getrelop(relop)
        self.jumpz(0)
        jump = self.count - 1
        for item in self.tokens[temp]['productions']:
            if item == '<Statement> -> <Scan>':
                pos = self.scan(pos)
            elif item == '<Statement> -> <Print>':
                pos = self.print(pos)
            elif item == '<Statement> -> <Return>':
                pos = self.ret(pos)
            elif item == '<Statement> -> <Assign>':
                pos = self.assign(pos)
            elif item == '<Statement> -> <If>':
                pos = self.ifstat(pos)
            elif item == '<Statement> -> <While>':
                pos = self.whilestat(pos)
        self.jump(labelpos)
        self.instructions[jump][2] = self.count + 1
        pos += 1
        if self.tokens[pos]['token'] == '$':
            self.label()
        return pos

    def getexpr(self, pos):
        operpos = -1
        while True:
            if self.tokens[pos]['lexeme'] == 'int' or self.tokens[pos]['lexeme'] == 'real':
                self.pushi(self.tokens[pos]['token'])
                if operpos != -1:
                    self.getoper(operpos)
                    operpos = -1
            elif self.tokens[pos]['token'] == 'true':
                self.pushi(1)
                if operpos != -1:
                    self.getoper(operpos)
                    operpos = -1
            elif self.tokens[pos]['token'] == 'false':
                self.pushi(0)
                if operpos != -1:
                    self.getoper(operpos)
                    operpos = -1
            elif self.tokens[pos]['lexeme'] == 'identifier':
                self.pushm(self.getmemloc(self.tokens[pos]['token']))
                # insert test for function
                if operpos != -1:
                    self.getoper(operpos)
                    operpos = -1
            elif self.tokens[pos]['token'] == '(':
                pos += 1
                pos = self.getexpr(pos)
                pos -= 1
                if operpos != -1:
                    self.getoper(operpos)
                    operpos = -1
            elif self.tokens[pos]['token'] in self.expressions:
                operpos = pos
            else:
                pos += 1
                break
            pos += 1
        return pos

    def getoper(self, pos):
        method = self.expressions[self.tokens[pos]['token']]
        method()

    def getrelop(self, pos):
        if self.tokens[pos]['token'] + self.tokens[pos+1]['token'] in self.relop:
            method = self.relop[self.tokens[pos]['token'] + self.tokens[pos + 1]['token']]
            method()
        else:
            method = self.relop[self.tokens[pos]['token']]
            method()

    def getmemloc(self, token):
        for item in self.symbols:
            if item['token'] == token:
                return item['memory']

    def getprod(self, token, pos):
        for item in token['productions']:
            if item == '<Statement> -> <Scan>':
                pos = self.scan(pos)
            elif item == '<Statement> -> <Print>':
                pos = self.print(pos)
            elif item == '<Statement> -> <Return>':
                pos = self.ret(pos)
            elif item == '<Statement> -> <Assign>':
                pos = self.assign(pos)
            elif item == '<Statement> -> <If>':
                pos = self.ifstat(pos)
            elif item == '<Statement> -> <While>':
                pos = self.whilestat(pos)
        return pos

    def find(self, tok, pos):
        val = {}
        if tok == '$':
            for token in self.tokens:
                if token['token'] == '$':
                    val = token
                    break
                pos += 1
        else:
            for token in self.tokens:
                if token['token'] == tok and self.tokens[pos - 1]['token'] == 'function':
                    val = self.tokens[pos - 1]
                    break
                pos += 1
        return val, pos

    def parse(self):
        main = self.find('$', 0)
        self.getprod(main[0], main[1])
