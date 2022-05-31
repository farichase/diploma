# coding=utf8

from lexer import tokens
import ply.yacc as yacc
import logging

class Node:
    def parts_str(self):
        st = []
        for part in self.parts:
            st.append( str( part ) )
        return "\n".join(st)

    def __repr__(self):
        return self.type + ":\n\t" + self.parts_str().replace("\n", "\n\t")

    def add_parts(self, parts):
        self.parts += parts
        return self

    def __init__(self, type, parts):
        self.type = type
        self.parts = parts


def p_unit(p):
    '''unit : 
            | declaration body
            | declaration body unit'''
    if len(p) == 1:
        p[0] = None
    if len(p) == 3:
        p[0] = Node('unit', [p[1], p[2]]) 
    if len(p) == 4: 
        if p[3] is None:
            p[3] = Node('unit', [])
        p[0] = p[3].add_parts([p[1], p[2]])

def p_declaration(p):
    '''declaration : TkDirective TkIdentifier
                   | TkIdentifier'''
    if len(p) == 3:
        p[0] = Node('declaration', [p[1], p[2]])
    else: 
        p[0] = Node('declaration', [p[1]])

def p_body(p):
    '''body : TkOpenBlock sentences TkCloseBlock'''
    p[0] = Node('body', [p[2]])

def p_sentences(p):
    '''sentences : sentence TkSemicolon
                 | sentence TkSemicolon sentences'''  
    if len(p) == 4:
        p[0] = p[3].add_parts([p[1]])  
    else: 
        p[0] = Node('sentences', [p[1]])    


def p_sentence(p):
    '''sentence : condExpr
                | condExpr rightpart
                | leftpart rightpart'''
    if len(p) == 3:
        p[0] = Node('sentence', [p[1], p[2]])
    if len(p) == 2:
        p[0] = Node('sentence', [p[1]])

def p_leftpart(p):
    '''leftpart : 
                | pattern'''
    if len(p) == 1:
        p[0] = Node('leftpart', [])
    if len(p) == 2:
        p[0] = Node('leftpart', [p[1]])   

def p_condExpr(p):
    '''condExpr : pattern condition '''
    p[0] = Node('condExpr', [p[1], p[2]])

def p_condition(p):
    '''condition : TkComma result TkColon condPattern'''
    p[0] = Node('condition', [p[2], p[4]])

def p_condPattern(p):
    '''condPattern : TkOpenBlock sentences TkCloseBlock
                   | pattern'''
    if len(p) == 4:
        p[0] = Node('condPattern', [p[2]])
    if len(p) == 2:
        p[0] = Node('condPattern', [p[1]])

def p_pattern(p):
    '''pattern : TkVar 
               | TkValue 
               | TkBool
               | TkBool pattern
               | TkVar pattern
               | bracketArgs
               | bracketArgs pattern
               | TkValue pattern'''
    if len(p) == 2:      
        p[0] = Node('pattern', [p[1]])  
    if len(p) == 3: 
        if p[2] is None:
            p[2] = Node('pattern', [])
        p[0] = p[2].add_parts([p[1]])  

def p_rightpart(p):
    '''rightpart : TkReplace
                 | TkReplace result'''
    if len(p) == 2:
        p[0] = Node('rightpart', [])
    if len(p) == 3:
        p[0] = Node('rightpart', [p[2]])

def p_result(p):
    '''result : 
              | TkVar 
              | TkValue 
              | TkBool
              | TkVar result
              | TkValue result
              | bracketArgs
              | bracketArgs result
              | call result TkCloseCall
              | call result TkCloseCall result'''
    if len(p) == 1:
        p[0] = Node('result', [])
    if len(p) == 2:
        p[0] = Node('result', [p[1]])
    if len(p) == 3:
        if p[2] is None:
            p[2] = Node('result', [])
        p[0] = p[2].add_parts([p[1]])
    if len(p) == 4:
        p[0] = Node('result', [p[1], p[2]])
    if len(p) == 5:
        if p[4] is None:
            p[4] = Node('result', [])
        p[0] = p[4].add_parts([p[1], p[2]])

def p_bracketArgs(p):
    '''bracketArgs : TkOpenBracket arg TkCloseBracket
                   | TkOpenBracket arg TkCloseBracket bracketArgs'''
    if len(p) == 4:
        p[0] = Node('bracketArgs', [p[2]])
    if len(p) == 5:
        if p[4] is None:
            p[4] = Node('bracketArgs', [])
        p[0] = p[4].add_parts([p[2]])

def p_arg(p):
    '''arg : 
           | TkVar
           | TkValue
           | TkVar arg
           | TkValue arg
           | bracketArgs arg
           | argBracketArg arg
           | call arg TkCloseCall
           | call arg TkCloseCall arg'''
    if len(p) == 1:
        p[0] = Node('arg', [])
    if len(p) == 2:
        p[0] = Node('arg', [p[1]])
    if len(p) == 3:
        if p[2] is None:
            p[2] = Node('arg', [])
        p[0] = p[2].add_parts([p[1]])
    if len(p) == 4:
        p[0] = Node('arg', [p[1], p[2]])
    if len(p) == 5:
        if p[4] is None:
            p[4] = Node('arg', [])
        p[0] = p[4].add_parts([p[1], p[2]])

def p_argBracketArg(p):
    '''argBracketArg : arg bracketArgs'''
    p[0] = p[1].add_parts(p[2])

def p_call(p):
    '''call : TkOpenCall TkIdentifier 
               | TkOpenCall ADD
               | TkOpenCall SUB
               | TkOpenCall MUL
               | TkOpenCall DIV
               | TkOpenCall REMOFDIV
               | TkOpenCall QU'''    
    p[0] = Node('call', [p[2]])              

def p_error(p):
    print('Unexpected token:', p)


logging.basicConfig(
    level = logging.DEBUG,
    filename = 'parselog.txt',
    filemode = "w"
)
log = logging.getLogger()
parser = yacc.yacc()

def build_tree(code):
    return parser.parse(code, debug=log)