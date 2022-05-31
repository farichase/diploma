import ply.lex as lex

# List of token names.   This is always required
tokens = (
   'TkComma', # ,
   'TkCloseBlock', # }
   'TkOpenBlock', # {
   'TkOpenCall', # <
   'TkCloseCall', # >
   'TkCloseBracket', # )
   'TkOpenBracket', # (
   'TkColon', # :
   'TkReplace', # =
   'TkSemicolon', # ;
   'ADD',
   'SUB',
   'MUL',
   'DIV',
   'REMOFDIV', # %
   'QU', # ?
   'TkDirective',
   'TkIdentifier',
   'TkVar',
   'TkValue',
   'TkBool',
)

states = (
   ('string','exclusive'),
)
# Regular expression rules for simple tokens
t_ADD    = r'\+'
t_MUL   = r'\*'
t_DIV  = r'/'
t_TkReplace = r'\='
t_TkOpenBracket  = r'\('
t_TkCloseBracket  = r'\)'
t_TkCloseBlock = r'\}'
t_TkOpenBlock = r'\{'
t_TkOpenCall = r'\<'
t_TkCloseCall = r'\>'
t_TkComma = r'\,'
t_TkColon = r'\:'
t_TkDirective = r'(\$ENTRY|\$EXTERN)'

def t_TkVar(t):
    r'(e|s|t)\.[A-Za-z0-9]+'
    if t.value not in t.lexer.vars:
        t.lexer.vars.append(t.value)
    return t 

def t_TkSemicolon(t):
    r'\;'
    t.lexer.vars = []
    return t

def t_TkBool(t):
    r'((True)|(False))'
    return t

def t_SUB(t):
    r'-'
    return t

def t_TkIdentifier(t):
    r'[A-Za-z\-\_0-9]+'
    if t.value not in t.lexer.idents:
        t.lexer.idents.append(t.value)
    return t

# изменили токен TkValue и сделали из него функцию, добавили его во все состояния
def t_ANY_TkValue(t): # нужен в обоих состояниях, потому что двойные кавычки матчатся и там и там.
    r'\''
    if t.lexer.current_state() == 'string':
        t.lexer.begin('INITIAL') # переходим в начальное состояние
    else:
        t.lexer.begin('string') # парсим строку
    pass

t_string_TkValue = r'([^$\'])+' # парсим пока не дойдем до переменной или до кавычки, попутно игнорируем экранки
# говорим что ничего не будем игнорировать
t_string_ignore = '' # это кстати обязательная переменная, без неё нельзя создать новый state

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# игнорируем комментарии
def t_comment(t):
    r'(((/\*(.|\n)*?\*/)|(//.*))|(\*[^\n]*))'
    pass

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# # Build the lexer
lexer = lex.lex()
lexer.vars = []
lexer.idents = []

# if __name__=="__main__":
#     # Test it out
#     f = open('/home/farida/SuperCompiler/my-app/syntaxCompletions/tests/input4.txt','r')
#     data = f.read()
#     # Give the lexer some input
#     lexer.input(data)
#     while True:
#         tok = lexer.token() # читаем следующий токен
#         if not tok: break      # закончились 
#         print(tok)
#     print(lexer.vars)
#     print(lexer.idents)

def build_lexer(data):
    lexer.input(data)
    while True:
        tok = lexer.token() # читаем следующий токен
        if not tok: 
            break # закончились 
    return [lexer.idents, lexer.vars]