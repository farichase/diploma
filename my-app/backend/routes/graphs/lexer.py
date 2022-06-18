from re import T
import ply.lex as lex

tokens = (
   'TkNode',
   'TkChildren',
   'TkLooped',
   'TkTo',
   'TkAssign',
   'TkCall',
   'TkArg',
   'TkPar',
   'TkE',
   'TkS',
   'TkT',
   'TkLet',
   'TkIn',
   'TkCloseBracket', # )
   'TkOpenBracket', # (,
   'TkMul',
   'TkIdent',
   'TkValue',
   'TkAreEqual',
   'TkOr',
   'TkInequal',
   'TkNotEqual',
   'TkTopCall',
   'TkStatus'
)

t_TkMul   = r'\*'
t_TkOpenBracket  = r'\('
t_TkCloseBracket  = r'\)'

def t_TkStatus(t):
    r'(?:Undriven|Driven|Finished)'
    return t
def t_TkTopCall(t):
    r'topcall'
    return t
def t_TkNotEqual(t):
    r'NotEqual'
    return t
def t_TkInequal(t):
    r'Inequal'
    return t
def t_TkOr(t):
    r'OR'
    return t

def t_TkAreEqual(t):
    r'AreEqual'
    return t
def t_TkNode(t):
    r'Node'
    return t
def t_TkChildren(t):
    r'Children'
    return t
def t_TkLooped(t):
    r'Looped'
    return t
def t_TkTo(t):
    r'to'
    return t
def t_TkAssign(t):
    r'assign'
    return t
def t_TkCall(t):
    r'call'
    return t
def t_TkArg(t):
    r'arg'
    return t
def t_TkPar(t):
    r'par'
    return t
def t_TkLet(t):
    r'let'
    return t
def t_TkIn(t):
    r'in'
    return t
def t_TkE(t):
    r'e'
    return t
def t_TkS(t):
    r's'
    return t
def t_TkT(t):
    r't'
    return t
def t_TkIdent(t):
    r'[A-Za-z0-9\_]+'
    return t
def t_TkValue(t):
    r'[A-Za-z\-\_,!0-9,:;!?\<\>.+\|]+'
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore  = ' \t'

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()

if __name__=="__main__":
    f = open('log.scpgraph', 'r')
    data = f.read()
    lexer.input(data)
    while True:
        tok = lexer.token() 
        if not tok: break     
        print(tok)