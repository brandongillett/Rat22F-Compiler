## KEYWORDS,SEPARTATORS,OPERATORS ##
keywords = ['get','put','return','integer','function','if','else','endif','while','real','boolean','float']
separators = ['(',')','{','}',';',',','$']
operators = ['-','+','/','*','=','<','>','!','|','%']

#FSM for finding if token is an identifier
def is_identifier(token):
    current_state = 0
    for char in token:
        if current_state == 0:
            if char.isalpha():
                current_state = 1
            else:
                return False
        if current_state == 1:
            if char.isalpha():
                pass
            elif char.isnumeric():
                pass
            elif char == '_':
                pass
            else:
                return False
    if current_state == 1:
        return True
    else:
        return False
#FSM for finding if token is integer
def is_int(token):
    current_state = 0
    for char in token:
        if current_state == 0:
            if char.isnumeric():
                current_state = 1
            else:
                return False
        elif current_state == 1:
            if char.isnumeric():
                pass
            else:
                return False
    if current_state == 1:
        return True
    else:
        return False
#Function to find if token is a real
def is_real(token):
    try:
        float(token)
        return True
    except ValueError:
        return False
#function to find if comment starts and ends
def is_comment(state,char,nextchar):
    if state == '' and char == '/' and nextchar == '*':
        return True
    elif state == 'comment' and char != '*' and nextchar != '/':
        return True
    elif state == 'comment' and char == '*' and nextchar == '/':
        return False
#function will find if the next character is blank,separator, or operator so we can seperate words that arent functions
def is_endofword(nextchar):
    if nextchar in separators:
        return True
    elif nextchar in operators:
        return True
    elif nextchar == 'endoffile':
        return True
    elif nextchar == ' ':
        return True
    else:
        return False
#turn file into characters
def characterize(file):
    charlist = []
    linecount = 1
    for line in file:
        for char in line:
            #add character to list with linecount if its not blank
            if char != ' ' and char != '\n':
                newchar = {'char':char,'line':linecount}
                charlist.append(newchar)
            #add blank to list only once
            if char == ' ' or char == '\n':
                if charlist[len(charlist)-1]['char'] != ' ':
                    newchar = {'char':' ','line':linecount}
                    charlist.append(newchar)
        linecount += 1
    #add chatacter for end of file so we know when to stop
    newchar = {'char':'endoffile','line':linecount+1}
    charlist.append(newchar)
    return(charlist)
#lexer class
class Lexer:
    def __init__(self,file):
        self.file = file
        self.tokens = []
    #get tokens and add them token list
    def Tokenize(self):
        characters = characterize(self.file)
        state = ''
        current = []

        count = 0
        for char in characters:
            #add each character to current
            current.append(char['char'])
            #if character is blank ignore it
            if char['char'] == ' ':
                current = []
            #find where comment starts and ends so we can ignore it
            elif state == '' and characters[count]['char'] == '/' and characters[count+1]['char'] == '*':
                state = 'comment'
                current = []
            elif state == 'comment' and characters[count]['char'] == '/' and characters[count-1]['char'] == '*':
                state = ''
                current = []
            elif state == 'comment':
                current = []
            #join the current list and see if its in keywords
            elif ''.join(current) in keywords:
                self.tokens.append({'token':''.join(current),'lexeme':'keyword','line':char['line']})
                current = []
            #checks if char is in separators
            elif char['char'] in separators:
                self.tokens.append({'token':char['char'],'lexeme':'separator','line':char['line']})
                current = []
            #checks if char is in operators
            elif char['char'] in operators:
                self.tokens.append({'token':char['char'],'lexeme':'operator','line':char['line']})
                current = []
            #as long as char isnt at the end we are going to determine everything else
            elif char['char'] != 'endoffile':
                #if the next character is the end of the word determine if its an int
                if is_endofword(characters[count+1]['char']) and is_int(''.join(current)):
                    self.tokens.append({'token':''.join(current),'lexeme':'int','line':char['line']})
                    current = []
                #if the next character is the end of the word determine if its a real
                elif is_endofword(characters[count+1]['char']) and is_real(''.join(current)):
                    self.tokens.append({'token':''.join(current),'lexeme':'real','line':char['line']})
                    current = []
                #if the next character is the end of the word it will automatically be a identifier
                elif is_endofword(characters[count+1]['char']) and is_identifier(''.join(current)):
                    self.tokens.append({'token':''.join(current),'lexeme':'identifier','line':char['line']})
                    current = []
                elif is_endofword(characters[count+1]['char']):
                    self.tokens.append({'token':''.join(current),'lexeme':'undefined','line':char['line']})
                    current = []
            count += 1